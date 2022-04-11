from typing import List, Dict, Tuple, Optional

import pyproj
from geoalchemy2 import Geometry
from shapely import wkb
from shapely.geometry.base import BaseGeometry
from shapely.geometry import mapping
from shapely.ops import transform
from sqlalchemy.orm import InstrumentedAttribute, ColumnProperty
from src.orm.dictionary_actions import  ActionFunction, ActionAttribute ,ParamAction,  dic_action
from src.orm.action_type import FUNCTION, ATTRIBUTE, Action
from src.orm.models import AlchemyBase

class AlchemyGeoBase(AlchemyBase):
    base_geom = None
    __abstract__ = True

    @classmethod
    def get_geo_attribute_or_column(cls, ttype: int = 0) -> str:
        # ttype = 0 => attribute. ttype = 1 => column
        return next((tuple_name_type[ttype] for tuple_name_type in cls.list_attribute_column_type() if
                     tuple_name_type[2].lower().startswith('geometry(')), None)

    @classmethod
    def is_geometry(cls, value: object) -> bool:
        return isinstance(value, InstrumentedAttribute) and type(value.property.columns[0].type) == Geometry

    @classmethod
    def geo_attribute_name(cls) -> Optional[str]:
        return next((key for key, value in cls.__dict__.items() if cls.is_geometry(value)), None)

    @classmethod
    def geo_attribute_type(cls) -> Optional[type]:
        return next((type(value.property.columns[0].type) for key, value in cls.__dict__.items() if cls.is_geometry(value)), None)

    @classmethod
    def geo_column_name(cls) -> str:
        return cls.get_geo_attribute_or_column(1)

    @classmethod
    def is_geometry_attribute(cls, inst_attr: InstrumentedAttribute) -> bool:
        return isinstance(inst_attr.prop, ColumnProperty) and cls.attribute_name_given(
            inst_attr) == cls.geo_attribute_name()

    @classmethod
    def srid(cls) -> int:
        return 4326

    def properties_dict_without_geom(self, attrib_names: List[str] = None) -> dict:
        attrs = attrib_names if attrib_names is not None else self.__class__.attributes_with_dereferenceable()
        attrs.remove(self.geo_attribute_name())
        return self.properties_dict(attrs)

    def json_dict(self, attrib_names: List[str] = None) -> dict:
        attrib_names = attrib_names if attrib_names is not None else self.__class__.attributes_with_dereferenceable()
        if self.geo_attribute_name() in attrib_names:
            if len(attrib_names) > 1:
                dic = {
                    "type": "Feature",
                    "id": getattr(self, self.primary_key()),
                    "geometry": mapping(self.get_base_geom()),
                    "properties": self.properties_dict_without_geom(attrib_names)
                }
            else:
                dic = mapping(self.get_base_geom())
            return dic
        return super().json_dict(attrib_names)

    def get_geom(self) -> str:
        return getattr(self, self.__class__.geo_attribute_name(), None)

    def get_base_geom(self) -> BaseGeometry:
        if self.base_geom is None:
            geo = self.get_geom()
            self.base_geom = wkb.loads(geo, hex=True) if type(geo) == str else wkb.loads(geo)
        return self.base_geom

    def transform(self, srid_dest: int = None) -> BaseGeometry:
        crs_orig = pyproj.CRS(f'EPSG:{self.__class__.srid()}')
        crs_dest = pyproj.CRS(f'EPSG:{srid_dest}')
        project = pyproj.Transformer.from_crs(crs_orig, crs_dest, always_xy=True).transform
        return transform(project, self.get_base_geom())

    def buffer(self, distance: float) -> float:
        return self.get_base_geom().buffer(distance)

    def area(self, epsg: int = None) -> float:
        """
        Returns the area (float) of the object.
        :param epsg:
        :return: float
        """
        if epsg is None:
            return self.get_base_geom().area
        temp_geom = self.transform(3005)
        return temp_geom.area

    def bound(self) -> Tuple[float, float, float, float]:
        """
        Returns a (minx, miny, maxx, maxy) tuple (float values) that bounds the object.
        :return: tuple[float,float,float,float]
        """
    def projection(self, string_enum: str) -> object:
        enum = string_enum.split(',')
        dic_attr = {}
        if len(enum) == 1:
            att_name = enum[0]
            return self.get_base_geom() if (self.geo_attribute_name() == att_name) else getattr(self, att_name)
        for att_name in enum:
            dic_attr[att_name] = self.get_base_geom() if (self.geo_attribute_name() == att_name) else getattr(self, att_name)
            #dic_attr[att_name] =  getattr(self, att_name)
        return dic_attr

    def bbox(self):
        return self.get_base_geom().bounds

    async def execute_attribute_given(self, path: str) -> object:
        """
        :param path is a string and have to start with one attribute
        :return: object. It could be anything, for example: an instance of int, float,str,BaseGeometry, etc
        """
        arr_actions = self.__class__.path_as_list(path)
        #attrib = self.get_base_geom() if arr_actions[0] == self.__class__.geo_attribute_name() else arr_actions[0]
        obj = self.get_base_geom() if arr_actions[0] == self.__class__.geo_attribute_name() else getattr(self, arr_actions[0])
        arr_actions = arr_actions[1:]
        while len(arr_actions) > 0:
            obj = await self.execute_action(obj, arr_actions)
        return obj

    @classmethod
    def actions_to_dissemination(cls) -> Dict[str, Action]:
        """
        :return: This method returns a dictionary with actions to dissemination.
        The key is a operation or attribute name. The value is a an action.
        """
        dic = {
            'transform': ActionFunction('transform','transform' , BaseGeometry, [ ParamAction('srid_dest', int)]),
            'srid': ActionFunction('srid','srid', int),
            'area': ActionAttribute('area', float),
            'buffer': ActionFunction('buffer','buffer', BaseGeometry, [ParamAction('buf_dest', float)]),
            'wkt': ActionAttribute('wkt', BaseGeometry),
        }
        return dic
    @classmethod
    def action_dic(cls) -> Dict[object, Dict]:
        """
        :return: This method returns a dictionary to get function/attribute supported in a request.
        The key is a type/class and value is a dictionary(key: operation/attribute name, value: Action instance
        """
        dic = dic_action #{cls: cls.actions_to_dissemination()}
        dic.update(super().action_dic())
        return dic
    def yourself_action(self):
        return {
            'transform': ActionFunction('transform','transform', Geometry, [ParamAction('srid', int)]),
            'buffer': ActionFunction('transform','transform', Geometry, [ParamAction('srid', int)]),
            'area': ActionFunction('area', 'area',float, [ParamAction('srid', int, False)]),
            'bbox': ActionFunction('bbox', 'bbox', [], []),

        }
    @classmethod
    def instances_operation(cls) -> Dict:
        return dic_action
