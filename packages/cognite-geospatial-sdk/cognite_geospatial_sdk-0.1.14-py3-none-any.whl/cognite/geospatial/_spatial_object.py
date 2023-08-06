# Copyright 2020 Cognite AS
from typing import Dict

import numpy as np
from cognite.geospatial._client import FullSpatialItemDTO
from cognite.geospatial.types import Geometry

try:
    from collections.abc import Mapping  # noqa
    from collections.abc import MutableMapping  # noqa
except ImportError:
    from collections import Mapping  # noqa
    from collections import MutableMapping  # noqa


class SpatialObject(FullSpatialItemDTO, Geometry):
    def __init__(self, client=None, spatial_item: FullSpatialItemDTO = None):
        self.client = client
        self.__dict__.update(spatial_item.__dict__)

        self._layer_info = None
        self._coverage: Dict[str, str] = {}

        self.double_vector = {}
        self.integer_vector = {}
        self.boolean_vector = {}
        self.text_vector = {}

    def _set_layer_info(self, layer):
        self._layer_info = layer

    def layer_info(self):
        """Get spatial item layer.
        """
        if self._layer_info is None:
            self._layer_info = self.client.get_layer(name=self.layer)
        return self._layer_info

    def _add_double(self, name: str, vector):
        self.double_vector[name] = np.array(vector, dtype=np.double)

    def _add_integer(self, name: str, vector):
        self.integer_vector[name] = np.array(vector, dtype=np.int32)

    def _add_boolean(self, name: str, vector):
        self.boolean_vector[name] = np.array(vector, dtype=np.bool)

    def _add_text(self, name: str, value):
        self.text_vector[name] = value

    def __getitem__(self, name: str):
        if name in self.double_vector:
            return self.double_vector[name]

        if name in self.integer_vector:
            return self.integer_vector[name]

        if name in self.boolean_vector:
            return self.boolean_vector[name]

        if name in self.text_vector:
            return self.text_vector[name]

        return None

    def coverage(self, dimensional_space: str = "2d", output_crs: str = None):
        """Retrieve the coverage of the spatial object.
        Args:
            dimensional_space (str): The geometry projection of the coverage. Valid values are "2d" (default), "3d"
        """
        if output_crs is None:
            output_crs = self.crs

        coverage_key = dimensional_space + "_" + output_crs
        if coverage_key not in self._coverage:
            coverage_obj = self.client.get_coverage(
                output_crs=output_crs, id=self.id, dimensional_space=dimensional_space
            )
            if coverage_obj is not None:
                self._coverage[coverage_key] = coverage_obj.wkt
        return self._coverage[coverage_key]

    def delete(self) -> bool:
        """Delete spatial item.
        """
        item = self.client.delete_spatial(id=self.id)
        return item is not None

    def get(self):
        """ Get numpy arrays of x,y,z if the layer is raster/seismic/horizon. Otherwise, get geometry in the form of wkt
        """
        if self.layer == "raster" or self.layer == "seismic" or self.layer == "horizon":
            active = self.__getitem__("active")
            x = self.__getitem__("x")
            y = self.__getitem__("y")
            z = self.__getitem__("z")
            if z is None:
                data = np.stack((x, y), axis=-1)
            else:
                data = np.stack((x, y, z), axis=-1)
            if active is None:
                return data
            active = active[: len(data)]
            return data[active]
        else:
            return self.geometry.wkt

    def height(self):
        """ Get the difference between maximum and minimum inline
        """
        min_ = self.__getitem__("iline_min")
        max_ = self.__getitem__("iline_max")
        if min_ is not None and max_ is not None:
            return int(max_) - int(min_) + 1

        return None

    def width(self):
        """ Get the difference between maximum and minimum cross-line
        """
        min_ = self.__getitem__("xline_min")
        max_ = self.__getitem__("xline_max")
        if min_ is not None and max_ is not None:
            return int(max_) - int(min_) + 1

    def grid(self):
        """ Get the grid representation if the layer is raster/seismic/horizon
        """
        if self.layer == "raster" or self.layer == "seismic" or self.layer == "horizon":
            active = self.__getitem__("active")
            x = self.__getitem__("x")
            y = self.__getitem__("y")
            z = self.__getitem__("z")
            if z is None:
                points = np.stack((x, y), axis=-1)
            else:
                points = np.stack((x, y, z), axis=-1)

            if active is None:
                rows = self.__getitem__("row")
                columns = self.__getitem__("column")
                if rows is None or columns is None:
                    return None
                height = rows.max() - rows.min() + 1
                width = columns.max() - columns.min() + 1
                data = np.ndarray(shape=(height, width, points.shape[1]), dtype=np.double)
                for i in range(len(points)):
                    r = rows[i] - rows.min()
                    c = columns[i] - columns.min()
                    data[r, c] = points[i]
            else:
                width = self.width()
                height = self.height()
                data = np.ndarray(shape=(width, height, points.shape[1]), dtype=np.double)
                size = min(len(active), len(points))
                active_indx = np.argwhere(active[:size] is True)
                for i in active_indx:
                    r = int(i % height)
                    c = int((i - r) / height)
                    data[c, r] = points[i]

            return data
        return None

    def __str__(self):
        return f"id: {self.id}\nexternal_id: {self.external_id}\nname: {self.id}\nlayer: {self.layer}\ncrs: {self.crs}"
