from typing import List
from src.orm.converter import ConverterType
from shapely.geometry import MultiPolygon, Polygon, LineString, MultiLineString, MultiPoint
from shapely.geometry.base import BaseGeometry
from shapely.geometry.point import Point
FUNCTION = 1
ATTRIBUTE = 2

#This dictionary is related to BaseGeometry and subclasses.
# The key is function or attribute name.
# The value is a tuple with a dictionary and int. The dictionary is like __annotations__.
# The int is 1 for FUNCTION or 2 for ATTRIBUTE
class ParamAction:
    def __init__(self, name: str, _type: object, mandatory: bool = True, default: object = None, description: str = None):
        self.name = name
        self._type = _type
        self.mandatory = mandatory
        self.default = default
        self.description = description


class Action:
    def __init__(self, name: str,  answer: object=None, description: str = None, example: str = None):
        self.name = name
        self.answer = answer
        self.description = description
        self.example = example

    def count_params(self):
        return NotImplementedError("'count_params' must be implemented in subclasses")

    def count_mandatory_params(self):
        return NotImplementedError("'count_mandatory_params' must be implemented in subclasses")

    def execute(self, obj, action_names: List[str]) -> object:
        raise NotImplementedError("'execute' must be implemented in subclasses")

class ActionAttribute(Action):
    def __init__(self, name, answer):
        super().__init__(name, answer)

    def count_params(self):
        return 0

    def count_mandatory_params(self):
        return 0

    async def execute(self, obj, action_names: List[str]) -> object:
        return getattr(obj, self.name)

class ActionFunction(Action):
    def __init__(self, name, answer, paramActions: List[ParamAction]=[]):
        super().__init__(name, answer)
        self.paramActions = paramActions

    def count_params(self):
        return len(self.paramActions)

    def count_mandatory_params(self):
        return len([ param for param in self.paramActions if param.mandatory ])

    def has_parameters(self)-> bool:
        return len(self.paramActions) > 0

    def param_types(self)->List[type]:
        return [param._type for param in self.paramActions]

    async def execute(self, obj, action_names: List[str]) -> object:
        if not self.has_parameters():
            return getattr(obj, self.name)()
        if len(action_names) == 0:
            para_text = f" these parameters: {self.paramActions}" if self.count_params() > 1 else f" this parameter: {self.paramActions}"
            raise SyntaxError(f"The operation {self.name} must have at least {para_text}")
        params = action_names.pop(0).split('&')
        if len(params) > self.count_params() or len(params) < self.count_mandatory_params():
            raise SyntaxError(f"Incorrect number of parameters in the operation {self.name}")
        paramets = await ConverterType().convert_parameters(params, self.param_types())
        result = getattr(obj, self.name)(*paramets)
        return result

dic_geo_action = {
        'area': ActionAttribute('area', float),
        'boundary': ActionAttribute('boundary', BaseGeometry),
        'bounds': ActionAttribute('bounds', tuple),
        'buffer': ActionFunction('buffer', BaseGeometry, [ParamAction('distance', float), ParamAction('resolution', int, False, 16),ParamAction('cap_style', int, False, 1), ParamAction('join_style', int, False, 1), ParamAction('mitre_limit', float, False, 5.0),ParamAction('single_sided', bool, False, False)]),
        'centroid': ActionAttribute('centroid', Point),
        'contains': ActionFunction('contains', bool, [ParamAction('other', BaseGeometry )]),
        'convex_hull': ActionAttribute('convex_hull', BaseGeometry),
        'covered_by': ActionFunction('covered_by', bool, [ParamAction('other', BaseGeometry )]),
        'covers': ActionFunction('covers', bool, [ParamAction('other', BaseGeometry)]),
        'crosses': ActionFunction('crosses', bool, [ParamAction('other', BaseGeometry)]),
        'difference': ActionFunction('difference', BaseGeometry, [ParamAction('other', BaseGeometry)]),
        'disjoint': ActionFunction('disjoint', BaseGeometry, [ParamAction('other', BaseGeometry)]),
        'distance': ActionFunction('distance', float, [ParamAction('other', BaseGeometry)]),
        'envelope': ActionAttribute('envelope', BaseGeometry),
        'geometryType': ActionFunction('geometryType', str),
        'intersects': ActionFunction('intersects',  bool, [ParamAction('other', BaseGeometry)]),
        'intersection': ActionFunction('intersection',  BaseGeometry, [ParamAction('other', BaseGeometry)]),
        'overlaps': ActionFunction('overlaps',  bool, [ParamAction('other', BaseGeometry)]),
        'relate_pattern': ActionFunction('relate_pattern',  bool, [ParamAction('other', BaseGeometry), ParamAction('pattern', str)]),
        'simplify': ActionFunction('simplify',  BaseGeometry, [ParamAction('tolerance', float), ParamAction('preserve_topology', bool, True, True)]),
        'symmetric_difference': ActionFunction('symmetric_difference',  BaseGeometry, [ParamAction('other', BaseGeometry)]),
        'touches': ActionFunction('touches',  bool, [ParamAction('other', BaseGeometry)]),
        'wkb': ActionFunction('to_wkb', str),
        'wkt': ActionFunction('to_wkt', str),
        'union': ActionFunction('union',  BaseGeometry, [ParamAction('other', BaseGeometry)]),
        'within': ActionFunction('within',  bool, [ParamAction('other', BaseGeometry)]),
}
"""
dic_geo_action = {
        'area': ({'return': float }, ATTRIBUTE),
        'boundary': ({'return': BaseGeometry }, ATTRIBUTE),
        'bounds': ({'return': tuple}, ATTRIBUTE),
        'buffer': ({'distance': float, 'resolution': int, 'cap_style': int, 'join_style': int, 'mitre_limit': float, 'single_sided': bool, 'return': BaseGeometry}, FUNCTION),
        'centroid': ({'return': Point}, ATTRIBUTE),
        'contains': ({'other': BaseGeometry, 'return': bool}, FUNCTION),
        'convex_hull': ({'return': BaseGeometry}, ATTRIBUTE),
        'covered_by': ({'other': BaseGeometry, 'return': bool}, FUNCTION),
        'covers': ({'other': BaseGeometry, 'return': bool}, FUNCTION),
        'crosses': ({'other': BaseGeometry, 'return': BaseGeometry}, FUNCTION),
        'difference': ({'other': BaseGeometry, 'return': BaseGeometry}, FUNCTION),
        'disjoint': ({'other': BaseGeometry, 'return': BaseGeometry}, FUNCTION),
        'distance': ({'other': BaseGeometry, 'return': float}, FUNCTION),
        'envelope': ({'return': BaseGeometry }, ATTRIBUTE),
        'geometryType': ({'return': str}, FUNCTION),
        'intersects': ({'other': BaseGeometry, 'return': bool}, FUNCTION),
        'intersection': ({'other': BaseGeometry, 'return': BaseGeometry}, FUNCTION),
        'overlaps': ({'other': BaseGeometry, 'return': bool}, FUNCTION),
        'relate_pattern': ({'other': BaseGeometry, 'pattern': str, 'return': bool}, FUNCTION),
        'simplify': ({'tolerance': float, 'preserve_topology': bool, 'return': BaseGeometry}, FUNCTION),
        'symmetric_difference': ({'other': BaseGeometry, 'return': BaseGeometry}, FUNCTION),
        'touches': ({'other': BaseGeometry, 'return': bool}, FUNCTION),
        'to_wkb': ({'return': str}, FUNCTION),
        'to_wkt': ({'return': str}, FUNCTION),
        'union': ({'other': BaseGeometry, 'return': BaseGeometry}, FUNCTION),
        'within': ({'other': BaseGeometry, 'return': BaseGeometry}, FUNCTION),
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
}