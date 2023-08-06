# Copyright 2020 Cognite AS
"""Cognite Geospatial API store and query spatial data.

 Spatial objects represent a revision of an object present in a geographic position at a point
 in time (or for all time if no time is specified). The object has a position according to a
 specific coordinate reference system and can be a point, linestring, polygon, or surface
 defined by a position in 3-dimensional space. Within the defined area, the object can have
 attributes or values associated with more specific points or areas.

"""
import asyncio
import base64
import concurrent
import json
import os
import sys
import tempfile
import threading
from functools import lru_cache, partial
from json.decoder import JSONDecodeError
from typing import Any, Callable, Dict, List, Optional

import cognite.geospatial._client
import numpy as np
import pyarrow as pa
from cognite import geospatial as geospatial
from cognite.geospatial._client.rest import ApiException
from cognite.geospatial._spatial_filter_object import SpatialFilterObject
from cognite.geospatial._spatial_object import SpatialObject
from cognite.geospatial.types import DataExtractor, Geometry, SpatialRelationship
from pyarrow import parquet as pq
from tornado import ioloop
from tornado.concurrent import Future, future_set_exc_info, is_future

from ._console import in_interactive_session

from cognite.geospatial._client import (  # GeometryProjectionDTO,; SpatialItemsProjectionDTO,
    AttributeTypeDTO,
    CoreGeometrySpatialItemDTO,
    CreateSpatialItemsDTO,
    DataExtractorDTO,
    EitherIdDTO,
    ExternalIdDTO,
    FeatureLayersFilterDTO,
    InternalIdDTO,
    IntersectionQueryDTO,
    SpatialCoverageRequestDTO,
    SpatialDataDTO,
    SpatialDataRequestDTO,
    SpatialDatasDTO,
    SpatialIdsDTO,
    SpatialRelationshipDTO,
    SpatialSearchRequestDTO,
)


TORNADO_TIMEOUT_ERROR = 599
TORNADO_MESSAGE = "Could not get a response from the server. The server is down or timeout happens."


class GeospatialError(Exception):
    """Geospatial reised for internal errors.
    Attributes:
        message: explanation of the error
    """

    def __init__(self, message):
        super().__init__(message)


def _check_id(id: int):
    if id is not None and id > 9007199254740991:
        raise ValueError("Invalid value for `id`, must be a value less than or equal to `9007199254740991`")
    if id is not None and id < 1:
        raise ValueError("Invalid value for `id`, must be a value greater than or equal to `1`")


def _check_external_id(external_id: str):
    if external_id is None:
        raise ValueError("Invalid value for `external_id`, must not be `None`")
    if external_id is not None and len(external_id) > 255:
        raise ValueError("Invalid value for `external_id`, length must be less than or equal to `255`")


def _throw_exception(ex: ApiException):
    # check for tornado timout exception code
    if ex.status == TORNADO_TIMEOUT_ERROR:
        raise GeospatialError(message=TORNADO_MESSAGE)

    if ex.body:
        try:
            error_json = json.loads(ex.body)
        except JSONDecodeError:
            # not a json
            raise ex
        if "error" in error_json:
            error = error_json["error"]
            raise GeospatialError(message=error["message"])
    raise ex


def _check_id_geometry(id: int = None, external_id: str = None, wkt=None, crs=None):
    if id is None and external_id is None and wkt is None:
        raise ValueError("Either id or external_id or wkt must be provided")
    if wkt is not None and crs is None:
        raise ValueError("crs must be provided")


def _check_either_external_id(id: int = None, external_id: str = None):
    if id is None and external_id is None:
        raise ValueError("Either id or external_id must be provided")


def _first_item(response):
    if response is None or response.items is None or len(response.items) == 0:
        return None
    return response.items[0]


def _create_spatial_ids(id: int = None, external_id: str = None):
    _check_either_external_id(id, external_id)
    if id is not None:
        item = InternalIdDTO(id=id)
    elif external_id is not None:
        item = ExternalIdDTO(external_id=external_id)
    return SpatialIdsDTO(items=[item])


def _is_primitive(obj: object):
    return isinstance(obj, str) or isinstance(obj, int) or isinstance(obj, float)


def _write_parquet(file, field_name: str, values, data_type):
    schema = pa.schema([pa.field(field_name, pa.list_(data_type))])
    records = list()
    records.append({field_name: values})
    columns = list()

    for column in schema.names:
        filed_type = schema.types[schema.get_field_index(column)]
        field_data = pa.array([v[column] for v in records], type=filed_type)
        columns.append(field_data)

    table = pa.Table.from_arrays(columns, schema=schema)
    with pq.ParquetWriter(file, schema, compression="zstd", use_byte_stream_split=True) as writer:
        writer.write_table(table)


class CogniteGeospatialClient:
    """
    Main class for the seismic client
    """

    def __init__(
        self,
        api_key: str = None,
        base_url: str = None,
        port: int = None,
        api_token: str = None,
        project: str = None,
        timeout: int = 600,  # seconds
    ):
        # configure env
        api_key = api_key or os.getenv("COGNITE_API_KEY")
        if (api_key is None or not api_key.strip()) and api_token is None:
            raise ValueError(
                "You have either not passed an api key or not set the COGNITE_API_KEY environment variable."
            )
        self.configuration = cognite.geospatial._client.Configuration()
        self.configuration.client_side_validation = False
        if api_token is None and api_key is not None:
            self.configuration.api_key["api-key"] = api_key.strip()
        self.configuration.access_token = api_token

        base_url = base_url or "api.cognitedata.com"
        base_url = base_url.strip("/")
        port = port or 443

        if not base_url.startswith("http://") and not base_url.startswith("https://"):
            if port == 443:
                base_url = "https://" + base_url
            else:
                base_url = "http://" + base_url

        self.configuration.host = base_url + ":" + str(port)

        self.project = project or os.getenv("COGNITE_PROJECT")
        if self.project is None:
            raise ValueError("Project must be provided")

        api_client = cognite.geospatial._client.ApiClient(self.configuration)
        api_client.user_agent = "Cognite-Geospatial-SDK_" + geospatial.__version__ + "/python"
        self.api = cognite.geospatial._client.SpatialApi(api_client)
        self.timeout = timeout
        self.file_timeout = 21600

        self._interactive_session = in_interactive_session()

        if self._interactive_session:
            self._make_new_loop()

    def _make_new_loop(self):
        alt_ioloop_fut = concurrent.futures.Future()

        def run_alt_loop():
            asyncio.set_event_loop(asyncio.SelectorEventLoop())
            loop = ioloop.IOLoop()
            alt_ioloop_fut.set_result(loop)
            loop.start()

        alt_thread = threading.Thread(target=run_alt_loop)
        alt_thread.daemon = True
        alt_thread.start()
        self.loop = alt_ioloop_fut.result()

    def _run_sync(self, func: Callable, timeout: Optional[float] = None) -> Any:
        if not self._interactive_session:
            return ioloop.IOLoop.current().run_sync(func, timeout)

        loop = self.loop
        future_cell = [None]
        await_future = concurrent.futures.Future()

        async def run():
            try:
                result = await func()
                # if result is not None:
                #     from tornado.gen import convert_yielded

                #     result = convert_yielded(result)
                await_future.set_result(result)
            except Exception as e:
                fut = Future()  # type: Future[Any]
                future_cell[0] = fut
                future_set_exc_info(fut, sys.exc_info())
                await_future.set_exception(e)
            else:
                if is_future(result):
                    future_cell[0] = result
                else:
                    fut = Future()
                    future_cell[0] = fut
                    fut.set_result(result)
            assert future_cell[0] is not None
            loop.add_future(future_cell[0], lambda future: await_future.cancel())

        self.loop.add_callback(run)
        if timeout is not None:

            def timeout_callback() -> None:
                # If we can cancel the future, do so and wait on it. If not,
                # Just stop the loop and return with the task still pending.
                # (If we neither cancel nor wait for the task, a warning
                # will be logged).
                assert future_cell[0] is not None
                future_cell[0].cancel()

            timeout_handle = self.loop.add_timeout(self.loop.time() + timeout, timeout_callback)

        await_future.result()

        if timeout is not None:
            self.loop.remove_timeout(timeout_handle)
        assert future_cell[0] is not None
        if future_cell[0].cancelled() or not future_cell[0].done():
            raise TimeoutError("Operation timed out after %s seconds" % timeout)
        return future_cell[0].result()

    def _first_spatial_item(self, response) -> Optional[SpatialObject]:
        if response is None or response.items is None or len(response.items) == 0:
            return None
        return SpatialObject(client=self, spatial_item=response.items[0])

    async def get_spatial_info_async(self, id: int = None, external_id: str = None) -> Optional[SpatialObject]:
        """Retrieves spatial item information by internal ids or external ids.
        """
        spatial_by_ids = _create_spatial_ids(id, external_id)
        try:
            response = await self.api.by_ids_spatial_items(self.project, spatial_by_ids, _request_timeout=self.timeout)
            return self._first_spatial_item(response)
        except ApiException as e:
            return _throw_exception(e)

    def get_spatial_info(self, id: int = None, external_id: str = None) -> Optional[SpatialObject]:
        """Retrieves spatial item information by internal ids or external ids.

        Args:
            id (int): the id of the spatial object
            external_id (str): the external_id reference of the spatial object

        Returns:
            FullSpatialItemDTO: A spatial object
        """
        run_func = partial(self.get_spatial_info_async, id, external_id)
        item = self._run_sync(run_func, self.timeout)
        return item

    async def delete_spatial_async(self, id: int = None, external_id: str = None) -> Optional[SpatialObject]:
        """Delete spatial item by internal ids or external ids.
        """
        spatial_delete_ids = _create_spatial_ids(id, external_id)
        try:
            response = await self.api.delete_spatial(self.project, spatial_delete_ids, _request_timeout=self.timeout)
            return self._first_spatial_item(response)
        except ApiException as e:
            return _throw_exception(e)

    def delete_spatial(self, id: int = None, external_id: str = None) -> Optional[SpatialObject]:
        """Delete spatial item by internal ids or external ids.

        Args:
            id (int): the id of the spatial object
            external_id (str): the external_id reference of the spatial object

        Returns:
            FullSpatialItemsDTO: spatial object
        """
        run_func = partial(self.delete_spatial_async, id, external_id)
        item = self._run_sync(run_func, self.timeout)
        return item

    async def get_spatial_async(self, id: int = None, external_id: str = None) -> Optional[SpatialObject]:
        """Retrieves spatial item data by internal ids or external ids.
        """
        _check_either_external_id(id, external_id)
        if id is not None:
            item = InternalIdDTO(id=id)
        else:
            item = ExternalIdDTO(external_id=external_id)

        spatial_item = await self.get_spatial_info_async(id=id, external_id=external_id)
        if spatial_item is None:
            return None

        try:
            layer = await self.get_layer_async(name=spatial_item.layer)
            if layer is not None:
                spatial_item._set_layer_info(layer)

                for layer_attribute in layer.attributes:
                    data_request = SpatialDataRequestDTO(spatial_id=item, attributes=[layer_attribute.name])
                    data = await self.api.get_spatial_item_data(
                        self.project, data_request, _request_timeout=self.timeout
                    )
                    if data is not None and len(data) > 0:
                        for key, value in data.items():
                            if not layer_attribute.is_array:
                                spatial_item._add_text(layer_attribute.name, value)
                            elif layer_attribute.type == AttributeTypeDTO.DOUBLE:
                                byte_buffer = base64.urlsafe_b64decode(value)
                                vector = np.frombuffer(byte_buffer, dtype=">d")
                                spatial_item._add_double(layer_attribute.name, vector)
                            elif layer_attribute.type == AttributeTypeDTO.INT:
                                byte_buffer = base64.urlsafe_b64decode(value)
                                vector = np.frombuffer(byte_buffer, dtype=">i")
                                spatial_item._add_integer(layer_attribute.name, vector)
                            elif layer_attribute.type == AttributeTypeDTO.BOOLEAN:
                                byte_buffer = base64.urlsafe_b64decode(value)
                                vector = np.frombuffer(byte_buffer, dtype=np.uint8)
                                bit_array = np.unpackbits(vector, bitorder="little")
                                spatial_item._add_boolean(layer_attribute.name, np.array(bit_array, dtype=bool))

        except ApiException as e:
            _throw_exception(e)

        return spatial_item

    def __decode_attribute(self, value, type: AttributeTypeDTO):
        byte_buffer = base64.urlsafe_b64decode(value)
        if type == AttributeTypeDTO.DOUBLE:
            return np.frombuffer(byte_buffer, dtype=">d")
        elif type == AttributeTypeDTO.INT:
            return np.frombuffer(byte_buffer, dtype=">i")
        elif type == AttributeTypeDTO.BOOLEAN:
            vector = np.frombuffer(byte_buffer, dtype=np.uint8)
            bit_array = np.unpackbits(vector, bitorder="little")
            return np.array(bit_array, dtype=bool)
        elif type == AttributeTypeDTO.STRING:
            return str(byte_buffer, "utf-8")

        return value

    def get_spatial(self, id: int = None, external_id: str = None) -> Optional[SpatialObject]:
        """Retrieves spatial item data by internal ids or external ids.

        Args:
            id (int): the id of the spatial object
            external_id (str): the external_id reference of the spatial object

        Returns:
            SpatialObject: spatial object's data
        """
        run_func = partial(self.get_spatial_async, id, external_id)
        result = self._run_sync(run_func, self.timeout)
        return result

    async def find_spatial_async(
        self,
        layer: str,
        spatial_relationship: SpatialRelationship = None,
        geometry: Geometry = None,
        distance: float = None,
        name: str = None,
        asset_ids: List[int] = None,
        attributes: List[str] = None,
        metadata: Dict[str, str] = None,
        source: str = None,
        external_id_prefix: str = None,
        output_crs: str = None,
        limit: int = 10,
        offset: int = 0,
    ) -> List[SpatialObject]:
        """Searches and returns the spatial items based on resource type content or coordinates.
        """

        def _create_geometry(geometry: Geometry):
            _check_id_geometry(geometry.id, geometry.external_id, geometry.wkt, geometry.crs)
            if geometry.id is not None:
                _check_id(geometry.id)
            if geometry.external_id is not None:
                _check_external_id(geometry.external_id)
            return cognite.geospatial._client.GeometryDTO(
                id=geometry.id,
                external_id=geometry.external_id,
                wkt=geometry.wkt,
                crs=geometry.crs,
                local_vars_configuration=self.configuration,
            )

        spatial_filter = None
        if spatial_relationship is not None:
            geometry = _create_geometry(geometry)
            spatial_relationship = SpatialRelationshipDTO(
                name=spatial_relationship.value, distance=distance, local_vars_configuration=self.configuration
            )
            spatial_filter = SpatialFilterObject(
                spatial_relationship, geometry, local_vars_configuration=self.configuration
            )
        spatial_search_request = SpatialSearchRequestDTO(
            name=name,
            asset_ids=asset_ids,
            metadata=metadata,
            source=source,
            external_id_prefix=external_id_prefix,
            spatial_filter=spatial_filter,
            layer=layer,
            attributes=attributes,
            output_crs=output_crs,
            limit=limit,
            offset=offset,
        )

        try:
            response = await self.api.search_spatial(
                self.project, spatial_search_request_dto=spatial_search_request, _request_timeout=self.timeout
            )
            if response is not None:
                return [SpatialObject(client=self, spatial_item=item) for item in response.items]
            return []
        except ApiException as e:
            return _throw_exception(e)

    def find_spatial(
        self,
        layer: str,
        spatial_relationship: SpatialRelationship = None,
        geometry: Geometry = None,
        distance=None,
        name: str = None,
        asset_ids: List[int] = None,
        attributes: List[str] = None,
        metadata: Dict[str, str] = None,
        source: str = None,
        external_id_prefix: str = None,
        output_crs: str = None,
        limit: int = 10,
        offset: int = 0,
    ) -> List[SpatialObject]:
        """Search the spatial objects based on metadata or spatial relationships.

        Args:
            layer (str): the layer to which objects belong
            spatial_relationship (SpatialRelationship): the spatial relationship between looking objects and the input geometry
            geometry (Geometry): the input geometry
            name (str): the name of returned objects
            asset_ids (List[int]): the list of asset ids which spatial objects must link to
            attributes (List[str]): the list of attribute names are returned together with spatial objects
            metadata (dict): a set of metadata pairs which spatial objects must have
            source (str): the source of spatial objects
            external_id_prefix (str): the prefix of external_id reference which spatial objects must have
            output_crs (str): the crs of the output geometry attribute in case `geometry` attributes are queried
            limit (int): number of objects to be returned
            offset (int): the starting offset of objects in the results
        Returns:
            List[SpatialObject]: spatial object's data

        Example:
                >>> # search within the geometry of another spatial item
                >>> client.find_spatial(layer="polygon", spatial_relationship=SpatialRelationship.within,
                ...        geometry=Geometry(external_id="external_id"),
                ...    )
                >>> # search within a specific area defined by user
                >>> items = client.find_spatial(
                ...     layer="polygon",
                ...     spatial_relationship=SpatialRelationship.within,
                ...     geometry=Geometry(
                ...         wkt="POLYGON ((289999 5999999, 290006 5999999, 290006 6000006, 289999 6000006, 289999 5999999))",
                ...         crs="epsg:23031",
                ...         ),
                ...     )

        """
        run_func = partial(
            self.find_spatial_async,
            layer,
            spatial_relationship,
            geometry,
            distance,
            name,
            asset_ids,
            attributes,
            metadata,
            source,
            external_id_prefix,
            output_crs,
            limit,
            offset,
        )
        result = self._run_sync(run_func, self.timeout)
        return result

    async def get_coverage_async(
        self, output_crs: str, id: int = None, external_id: str = None, dimensional_space: str = "2d"
    ):
        """Retrieves the coverage of the spatial object by internal ids or external ids.
        """
        dimensional_space = dimensional_space.lower()
        if dimensional_space not in ["2d", "3d"]:
            raise GeospatialError("dimensional_space - must be 2d or 3d only")

        item_id = EitherIdDTO(id, external_id, local_vars_configuration=self.configuration)
        spatial_coverage_request = SpatialCoverageRequestDTO(
            items=[item_id],
            dimensional_space=dimensional_space,
            output_crs=output_crs,
            local_vars_configuration=self.configuration,
        )
        try:
            response = await self.api.get_spatial_coverage(
                self.project, spatial_coverage_request, _request_timeout=self.timeout
            )
            return _first_item(response)
        except ApiException as e:
            _throw_exception(e)

    def get_coverage(self, output_crs: str, id: int = None, external_id: str = None, dimensional_space: str = "2d"):
        """Retrieve the coverage of the spatial object by internal ids or external ids.

        Args:
            id (int): the id of the spatial object
            external_id (str): the external_id reference of the spatial object
            dimensional_space (str): The spatial dimension of the coverage. Valid values are "2d", "3d"
            output_crs (str): the crs of the output coverage

        Returns:
            SpatialItemsCoveragesDTO: spatial object's data
        """
        run_func = partial(self.get_coverage_async, output_crs, id, external_id, dimensional_space)
        item = self._run_sync(run_func, self.timeout)
        return item

    async def list_layers_async(self):
        layer_filter = FeatureLayersFilterDTO(names=[])
        try:
            response = await self.api.find_feature_layer(self.project, layer_filter, _request_timeout=self.timeout)
            return response.items
        except ApiException as e:
            _throw_exception(e)

    def list_layers(self):
        """List all available layers.

        Returns:
            list[FeatureLayerDTO]: list of layers
        """
        run_func = partial(self.list_layers_async)
        items = self._run_sync(run_func, self.timeout)
        return items

    async def get_layer_async(self, name: str):
        layer_filter = FeatureLayersFilterDTO(names=[name])
        try:
            response = await self.api.find_feature_layer(self.project, layer_filter, _request_timeout=self.timeout)
            return _first_item(response)
        except ApiException as e:
            _throw_exception(e)

    @lru_cache(maxsize=128)
    def get_layer(self, name: str):
        """Get layer by name.

        Args:
            name (str): name of the layer

        Returns:
            FeatureLayerDTO: layer information
        """
        run_func = partial(self.get_layer_async, name)
        layer = self._run_sync(run_func, self.timeout)
        return layer

    def get_attributes(
        self,
        layer_name: str,
        attributes: List[str],
        id: int = None,
        external_id: str = None,
        extractors: List[DataExtractor] = None,
    ):
        async def get_attributes(
            layer_name: str, item_id: EitherIdDTO, attributes: List[str], extractors: List[DataExtractor] = None
        ):
            layer = await self.get_layer_async(name=layer_name)
            if layer is None:
                raise ValueError("layer does not exist")

            extractors_dto = (
                [DataExtractorDTO(e.attribute, e.min_val, e.max_val) for e in extractors]
                if extractors is not None
                else None
            )
            data_request = SpatialDataRequestDTO(spatial_id=item_id, attributes=attributes, extractors=extractors_dto)
            response = await self.api.get_spatial_item_data(self.project, spatial_data_request_dto=data_request)
            layer_types = {la.name: la.type for la in layer.attributes}
            result = {}
            for attribute, value in response.items():
                val = self.__decode_attribute(value, layer_types[attribute])
                result[attribute] = val
            return result

        item_id = EitherIdDTO(id, external_id, local_vars_configuration=self.configuration)
        run_func = partial(get_attributes, layer_name, item_id, attributes, extractors)
        return self._run_sync(run_func, self.timeout)

    # def has_spatial(
    #     self,
    #     layer: str,
    #     spatial_relationship: SpatialRelationship = None,
    #     geometry: Geometry = None,
    #     distance=None,
    #     name: str = None,
    #     asset_ids: List[int] = None,
    #     metadata: Dict[str, str] = None,
    #     source: str = None,
    #     external_id_prefix: str = None,
    # ):
    #     """Test if spatial objects exist based on metadata or spatial relationships.

    #     Args:
    #         layer (str): the layer to which objects belong
    #         spatial_relationship (SpatialRelationship): the spatial relationship between looking objects and the input geometry
    #         geometry (Geometry): the input geometry
    #         name (str): the name of returned objects
    #         asset_ids (List[int]): the list of asset ids which spatial objects must link to
    #         metadata (dict): a set of metadata pairs which spatial objects must have
    #         source (str): the source of spatial objects
    #         external_id_prefix (str): the prefix of external_id reference which spatial objects must have
    #     Returns:
    #         bool: True - if data exists, otherwise False

    #     Example:
    #             >>> # has spatial items within the geometry of another spatial item
    #             >>> client.has_spatial(layer="polygon", spatial_relationship=SpatialRelationship.within,
    #             ...        geometry=Geometry(external_id="external_id"),
    #             ...    )
    #             >>> # has spatial items within a specific area defined by user
    #             >>> has_polygons = client.has_spatial(
    #             ...     layer="polygon",
    #             ...     spatial_relationship=SpatialRelationship.within,
    #             ...     cognite=Geometry(
    #             ...         wkt="POLYGON ((289999 5999999, 290006 5999999, 290006 6000006, 289999 6000006, 289999 5999999))",
    #             ...         crs="epsg:23031",
    #             ...         ),
    #             ...     )

    #     """
    #     items = self.find_spatial(
    #         layer=layer,
    #         spatial_relationship=spatial_relationship,
    #         geometry=geometry,
    #         distance=distance,
    #         name=name,
    #         asset_ids=asset_ids,
    #         attributes=None,
    #         metadata=metadata,
    #         source=source,
    #         external_id_prefix=external_id_prefix,
    #         limit=1,
    #     )
    #     return len(items) == 1

    def get_layer_items(self, layer: str, attributes: List[str] = None, output_crs: str = None):
        """Get all spatial items belong to layer.
        WARNING: This method will load all spatial items into memory and has a risk to get memory overflow.

        Args:
            layer (str): the layer to which objects belong
            attributes (List[str]): the list of attribute names are returned together with spatial objects
            output_crs (str): the crs of the output geometry attribute in case `geometry` attributes are queried

        Returns:
            DenseSpatialItemDTO: spatial object's data
        """
        items = []
        offset = 0
        limit = 100
        while True:
            bucket = self.find_spatial(
                layer=layer, attributes=attributes, limit=limit, offset=offset, output_crs=output_crs
            )
            items.extend(bucket)
            offset += limit
            if limit != len(bucket):
                break

        return items

    def create_geometry(
        self,
        name: str = None,
        external_id: str = None,
        description: str = None,
        metadata=None,
        layer: str = None,
        source: str = None,
        crs: str = None,
        geometry: str = None,
        asset_ids: List[int] = None,
    ):
        """ Create a geometry with its metadata

        Args:
            name (str): geometry name
            external_id (str): external_id reference
            description (str): the description
            metadata (dict): metadata of geometry
            layer (str): the layer to which the geometry belongs
            source (str): the source of geometry
            crs (str): the crs on which the geometry is defined
            geometry (str): wkt form of the geometry
            asset_ids (List[int]): a list of associated asset ids

        Returns:
            FullSpatialItemDTO: A spatial object
        """
        attributes = {"geometry": geometry}
        run_func = partial(
            self.create_spatial_async,
            name,
            external_id,
            description,
            metadata,
            layer,
            source,
            crs,
            attributes,
            asset_ids,
        )
        result = self._run_sync(run_func, self.timeout)
        return result

    async def create_spatial_async(
        self,
        name: str = None,
        external_id: str = None,
        description: str = None,
        metadata: dict = None,
        layer: str = None,
        source: str = None,
        crs: str = None,
        attributes: dict = None,
        asset_ids: List[int] = None,
    ):
        spatial_item = CoreGeometrySpatialItemDTO(
            name=name,
            external_id=external_id,
            description=description,
            metadata=metadata,
            asset_ids=asset_ids,
            layer=layer,
            source=source,
            attributes=attributes,
            crs=crs,
        )

        create_spatial_items = CreateSpatialItemsDTO(items=[spatial_item])
        try:
            response = await self.api.create_spatial(self.project, create_spatial_items, _request_timeout=self.timeout)
            return _first_item(response)
        except ApiException as e:
            _throw_exception(e)

    def create_spatial(
        self,
        name: str = None,
        external_id: str = None,
        description: str = None,
        metadata=None,
        layer: str = None,
        source: str = None,
        crs: str = None,
        attributes: dict = None,
        asset_ids: List[int] = None,
    ):
        run_func = partial(
            self.create_spatial_async,
            name,
            external_id,
            description,
            metadata,
            layer,
            source,
            crs,
            attributes,
            asset_ids,
        )
        result = self._run_sync(run_func, self.timeout)
        return result

    async def add_spatial_item_data_async(self, id: int, name: str, value, attribute_type: str):
        value_buff = None
        if attribute_type == "int":
            value_buff = value.astype(">i4").tobytes()
        elif attribute_type == "long":
            value_buff = value.astype(">i8").tobytes()
        elif attribute_type == "float":
            value_buff = value.astype(">f4").tobytes()
        elif attribute_type == "double":
            value_buff = value.astype(">f8").tobytes()
        elif attribute_type == "string":
            value_buff = bytearray(value, encoding="utf-8")
        elif attribute_type == "boolean":
            end_value = np.append(value.astype(np.uint8), 1)
            pack_int = np.packbits(end_value, bitorder="little")  # uint8
            value_buff = pack_int.tobytes()

        if value_buff is not None:
            value_data = str(base64.urlsafe_b64encode(value_buff), "utf-8")
        else:
            value_data = value
        spatial_data = SpatialDatasDTO(
            items=[SpatialDataDTO(item_id=InternalIdDTO(id=id), name=name, value=value_data)]
        )
        try:
            response = await self.api.add_spatial_item_data(self.project, spatial_data, _request_timeout=self.timeout)
            if response is not None:
                return response.items
            return None
        except ApiException as e:
            _throw_exception(e)

    async def store_spatial_item_data_async(self, id: int, name: str, value, attribute_type: str):
        if np.isscalar(value) or value.size <= 100 or attribute_type == "string" or attribute_type == "boolean":
            await self.add_spatial_item_data_async(id, name, value, attribute_type)
        else:
            pa_type = None
            if attribute_type == "int":
                pa_type = pa.int32()
            elif attribute_type == "long":
                pa_type = pa.int64()
            elif attribute_type == "float":
                pa_type = pa.float32()
            elif attribute_type == "double":
                pa_type = pa.float64()
            with tempfile.NamedTemporaryFile() as fp:
                _write_parquet(fp.name, name, value, pa_type)
                await self.parquet_file_save_async(file=fp.name, id=id, attributes=[])

    async def parquet_file_save_async(self, file, id: int = -1, external_id: str = "", attributes=[]):
        try:
            response = await self.api.file_save(
                self.project,
                file_type="parquet",
                file=file,
                id=id,
                external_id=external_id,
                attributes=attributes,
                _request_timeout=self.file_timeout,
            )
            return response
        except ApiException as e:
            _throw_exception(e)

    async def shape_file_save_async(self, file, layer: str, create_layer: bool = False, attributes=None):
        """Shapefile save as spatial items.
        """
        try:
            response = await self.api.file_save(
                self.project,
                file_type="shp",
                file=file,
                layer=layer,
                create_layer=create_layer,
                attributes=attributes,
                _request_timeout=self.file_timeout,
            )
            return response
        except ApiException as e:
            _throw_exception(e)

    def shape_file_save(self, file, layer: str, create_layer: bool = False, attributes=None):
        """Extract spatial items from shapefile and save it into geospatial.

        Args:
            file (str): file location on local drive
            layer (str): the layer name to save
            create_layer (bool): create layer if not exists
            attributes Optional(List[str]): attributes to save (if None save all attributes)
        """
        run_func = partial(self.shape_file_save_async, file, layer, create_layer, attributes)
        result = self._run_sync(run_func, self.file_timeout)
        return result

    async def interpret_async(self, id: int = None, external_id: str = None):
        """Interpret attributes from spatial item by internal ids or external ids.
        """
        spatial_by_ids = _create_spatial_ids(id, external_id)
        try:
            response = await self.api.interpret(self.project, spatial_by_ids, _request_timeout=self.timeout)
            return response
        except ApiException as e:
            _throw_exception(e)

    def interpret(self, id: int = None, external_id: str = None):
        """Interpret attributes from spatial item by internal ids or external ids.

        Args:
            id (int): the id of the spatial object
            external_id (str): the external_id reference of the spatial object

        """
        run_func = partial(self.interpret_async, id, external_id)
        result = self._run_sync(run_func, self.timeout)
        return result

    async def save_spatial_async(
        self,
        name: str = None,
        external_id: str = None,
        description: str = None,
        metadata=None,
        layer: str = None,
        source: str = None,
        crs: str = None,
        attributes: Dict = None,
        asset_ids: List[int] = None,
    ):
        item = None
        if external_id is not None:
            spatial_by_ids = _create_spatial_ids(external_id=external_id)
            response = await self.api.by_ids_spatial_items(self.project, spatial_by_ids)
            item = _first_item(response)

        name_attribute_map = {}
        if attributes is not None:
            layer_data = await self.get_layer_async(name=layer)
            if layer_data is None:
                raise ValueError(f"layer {layer} does not exist")

            name_attribute_map = {att.name: att for att in layer_data.attributes}
            if not set(attributes).issubset(set(name_attribute_map)):
                raise ValueError("invalid list of attributes")

        if item is None:
            simple_attr = None
            if attributes is not None:
                simple_attr = {k: v for k, v in attributes.items() if _is_primitive(v)}

            item = await self.create_spatial_async(
                name, external_id, description, metadata, layer, source, crs, simple_attr, asset_ids
            )

        if attributes is not None:
            for name, value in attributes.items():
                if name in name_attribute_map and not _is_primitive(value):
                    attribute = name_attribute_map.get(name)

                    await self.store_spatial_item_data_async(item.id, name, value, attribute.type)

                    item.attributes[name] = value

        await self.interpret_async(id=item.id)
        return item

    def save_spatial(
        self,
        name: str = None,
        external_id: str = None,
        description: str = None,
        metadata: Dict[str, str] = None,
        layer: str = None,
        source: str = None,
        crs: str = None,
        attributes: dict = None,
        asset_ids: List[int] = None,
    ):
        """ Create spatial object with additional attributes

        Args:
            name (str): object name
            external_id (str): external_id reference
            description (str): the description
            metadata (dict): metadata of the object
            layer (str): the layer to which the object belongs
            source (str): the source of the object
            crs (str): the crs where geometry attributes are defined
            attributes (dict): a map of attribute's name and value
            asset_ids (List[int]): a list of associated asset ids
        Returns:
            FullSpatialItemDTO: A spatial object
        """
        run_func = partial(
            self.save_spatial_async, name, external_id, description, metadata, layer, source, crs, attributes, asset_ids
        )
        result = self._run_sync(run_func, self.timeout)
        return result

    def get_intersections(self, geometry: Geometry, geometries: List[Geometry], output_crs):
        """ Find intersection between an array of geometries and another geometry

        Args:
            geometry (Geometry): a single geometry
            geometries (List[Geometry]): an array of geometries
            output_crs (str): the crs of intersection geometries
        Returns:
            List[str]: a list of intersections, each in the form of wkt

        Example:
                >>> intersections = client.get_intersections(
                ...         output_crs="epsg:4326",
                ...         geometry=Geometry(external_id="external_id_1"),
                ...         geometries=[
                ...             Geometry(external_id="external_id_2"),
                ...             Geometry(external_id="external_id_3"),
                ...             Geometry(external_id="external_id_4"),
                ...         ],
                ...     )

        """

        async def get_intersections_async(geometry: Geometry, geometries: List[Geometry], output_crs):
            geometry_dto = EitherIdDTO(
                id=geometry.id, external_id=geometry.external_id, local_vars_configuration=self.configuration
            )
            geometries_dto = [
                EitherIdDTO(id=geom.id, external_id=geom.external_id, local_vars_configuration=self.configuration)
                for geom in geometries
            ]
            intersection_query_dto = IntersectionQueryDTO(
                geometry=geometry_dto, geometries=geometries_dto, output_crs=output_crs
            )
            try:
                response = await self.api.find_intersection(
                    self.project, intersection_query_dto, _request_timeout=self.timeout
                )
                if response is None:
                    return None
                return [short_wkt.wkt for short_wkt in response.geometries]
            except ApiException as e:
                _throw_exception(e)

        run_func = partial(get_intersections_async, geometry, geometries, output_crs)
        result = self._run_sync(run_func, self.timeout)
        return result
