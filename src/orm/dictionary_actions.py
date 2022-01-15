
from shapely.geometry import MultiPolygon, Polygon, LineString, MultiLineString, MultiPoint
from shapely.geometry.base import BaseGeometry
from shapely.geometry.point import Point
from geoalchemy2 import Geometry

from src.orm.action_type import ActionAttribute, ActionFunction, ParamAction
from src.orm.dictionary_actions_postgis import dic_spatial_lookup_action


dic_geo_action = {
        'area': ActionAttribute('area', float),
        'boundary': ActionAttribute('boundary', Geometry),
        'bounds': ActionAttribute('bounds', tuple),
        'buffer': ActionFunction('buffer', Geometry, [ParamAction('distance', float), ParamAction('resolution', int, False, 16),ParamAction('cap_style', int, False, 1), ParamAction('join_style', int, False, 1), ParamAction('mitre_limit', float, False, 5.0),ParamAction('single_sided', bool, False, False)]),
        'centroid': ActionAttribute('centroid', Point),
        'contains': ActionFunction('contains', bool, [ParamAction('other', Geometry )]),
        'convex_hull': ActionAttribute('convex_hull', Geometry),
        'covered_by': ActionFunction('covered_by', bool, [ParamAction('other', Geometry )]),
        'covers': ActionFunction('covers', bool, [ParamAction('other', Geometry)]),
        'crosses': ActionFunction('crosses', bool, [ParamAction('other', Geometry)]),
        'difference': ActionFunction('difference', Geometry, [ParamAction('other', Geometry)]),
        'disjoint': ActionFunction('disjoint', Geometry, [ParamAction('other', Geometry)]),
        'distance': ActionFunction('distance', float, [ParamAction('other', Geometry)]),
        'envelope': ActionAttribute('envelope', Geometry),
        'geometryType': ActionFunction('geometryType', str),
        'intersects': ActionFunction('intersects',  bool, [ParamAction('other', Geometry)]),
        'intersection': ActionFunction('intersection',  Geometry, [ParamAction('other', Geometry)]),
        'overlaps': ActionFunction('overlaps',  bool, [ParamAction('other', Geometry)]),
        'relate_pattern': ActionFunction('relate_pattern',  bool, [ParamAction('other', Geometry), ParamAction('pattern', str)]),
        'simplify': ActionFunction('simplify',  Geometry, [ParamAction('tolerance', float), ParamAction('preserve_topology', bool, True, True)]),
        'symmetric_difference': ActionFunction('symmetric_difference',  Geometry, [ParamAction('other', Geometry)]),
        'touches': ActionFunction('touches',  bool, [ParamAction('other', Geometry)]),
        'wkb': ActionFunction('to_wkb', str),
        'wkt': ActionAttribute('wkt', str),
        'union': ActionFunction('union',  Geometry, [ParamAction('other', Geometry)]),
        'within': ActionFunction('within',  bool, [ParamAction('other', Geometry)]),
}
dic_geo_action = {**dic_geo_action, **dic_spatial_lookup_action}
"""
dic_geo_action = {
        'area': ({'return': float }, ATTRIBUTE),
        'boundary': ({'return': Geometry }, ATTRIBUTE),
        'bounds': ({'return': tuple}, ATTRIBUTE),
        'buffer': ({'distance': float, 'resolution': int, 'cap_style': int, 'join_style': int, 'mitre_limit': float, 'single_sided': bool, 'return': Geometry}, FUNCTION),
        'centroid': ({'return': Point}, ATTRIBUTE),
        'contains': ({'other': Geometry, 'return': bool}, FUNCTION),
        'convex_hull': ({'return': Geometry}, ATTRIBUTE),
        'covered_by': ({'other': Geometry, 'return': bool}, FUNCTION),
        'covers': ({'other': Geometry, 'return': bool}, FUNCTION),
        'crosses': ({'other': Geometry, 'return': Geometry}, FUNCTION),
        'difference': ({'other': Geometry, 'return': Geometry}, FUNCTION),
        'disjoint': ({'other': Geometry, 'return': Geometry}, FUNCTION),
        'distance': ({'other': Geometry, 'return': float}, FUNCTION),
        'envelope': ({'return': Geometry }, ATTRIBUTE),
        'geometryType': ({'return': str}, FUNCTION),
        'intersects': ({'other': Geometry, 'return': bool}, FUNCTION),
        'intersection': ({'other': Geometry, 'return': Geometry}, FUNCTION),
        'overlaps': ({'other': Geometry, 'return': bool}, FUNCTION),
        'relate_pattern': ({'other': Geometry, 'pattern': str, 'return': bool}, FUNCTION),
        'simplify': ({'tolerance': float, 'preserve_topology': bool, 'return': Geometry}, FUNCTION),
        'symmetric_difference': ({'other': Geometry, 'return': Geometry}, FUNCTION),
        'touches': ({'other': Geometry, 'return': bool}, FUNCTION),
        'to_wkb': ({'return': str}, FUNCTION),
        'to_wkt': ({'return': str}, FUNCTION),
        'union': ({'other': Geometry, 'return': Geometry}, FUNCTION),
        'within': ({'other': Geometry, 'return': Geometry}, FUNCTION),
}
"""
# dic_action is a Dictionaru where the key is a type/class and value is Dictionary see dic_geo_action.
dic_action = {
    BaseGeometry: dic_geo_action,
    Point: dic_geo_action,
    MultiPoint: dic_geo_action,
    Polygon: dic_geo_action,
    MultiPolygon: dic_geo_action,
    LineString: dic_geo_action,
    MultiLineString: dic_geo_action,
    Geometry: dic_geo_action,
}