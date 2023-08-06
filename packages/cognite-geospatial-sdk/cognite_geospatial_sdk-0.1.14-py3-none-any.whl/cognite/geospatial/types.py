# Copyright 2019 Cognite AS

from enum import Enum
from typing import NamedTuple

from cognite.geospatial._client import SpatialRelationshipNameDTO


class SpatialRelationship(Enum):
    within = SpatialRelationshipNameDTO.WITHIN
    within_distance = SpatialRelationshipNameDTO.WITHINDISTANCE
    within_completely = SpatialRelationshipNameDTO.WITHINCOMPLETELY
    intersect = SpatialRelationshipNameDTO.INTERSECT
    within_3d = SpatialRelationshipNameDTO.WITHIN3D
    within_distance_3d = SpatialRelationshipNameDTO.WITHINDISTANCE3D
    within_completely_3d = SpatialRelationshipNameDTO.WITHINCOMPLETELY3D
    intersect_3d = SpatialRelationshipNameDTO.INTERSECT3D


class Geometry:
    def __init__(self, id: int = None, external_id: str = None, wkt: str = None, crs: str = None):
        self.id = id
        self.external_id = external_id
        self.wkt = wkt
        self.crs = crs


class DataExtractor(NamedTuple):
    attribute: str
    min_val: str
    max_val: str
