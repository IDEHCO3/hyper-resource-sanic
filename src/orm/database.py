import datetime
import json
from datetime import datetime, date
from numbers import Number
from typing import List, Tuple, Optional, Any, Dict

from src.hyper_resource.util import value_has_url, a_request
from src.orm.converter import ConverterType
from geoalchemy2 import Geometry
from shapely.geometry import Polygon, LineString, MultiPolygon, MultiLineString, MultiPoint
from shapely.geometry.base import BaseGeometry
from sqlalchemy import Column, ForeignKey, Integer, SmallInteger, String, Float, Numeric
from sqlalchemy.inspection import inspect
from sqlalchemy.orm.attributes import InstrumentedAttribute
from sqlalchemy.orm import sessionmaker

from src.orm.dictionary_actions import ActionFunction
from src.orm.models import AlchemyBase, Base, Point

from src.orm.models import AlchemyBase


class AbstractDialectDatabase():
    def __init__(self, db):
        self.db = db


class DialectDatabase(AbstractDialectDatabase):
    def __init__(self, db, metadata_table=None, entity_class: AlchemyBase = None):
        super().__init__(db)
        self.metadata_table = metadata_table if metadata_table is not None else entity_class.__table__
        self.entity_class = entity_class

    def schema(self) -> str:
        return self.metadata_table.schema

    def table_name(self) -> str:
        return self.metadata_table.name

    def primary_key(self) -> str:
        # return self.metadata_table.primary_key.columns[0].name
        return list(self.metadata_table.primary_key.columns)[0].name

    def foreign_keys_columns(self):
        attrs = [attribute for attribute in list(self.entity_class.__table__.c) if isinstance(attribute, Column)]
        fk_columns = [att for att in attrs if len(att.foreign_keys) > 0]
        return fk_columns

    def foreign_key_column_by_name(self, column_name: str):
        fk_columns = self.foreign_keys_columns()
        col = [column for column in fk_columns if column.key == column_name]
        if (len(col) == 0):
            raise NameError(f"The attribute is not existent or does not represent a foreign key: {column_name}")
        else:
            return col[0]

    def get_model_by_foreign_key(self, fk_column: Column):
        refered_model_name = list(fk_column.foreign_keys)[0].column.table.name
        for c in Base._decl_class_registry.values():
            if hasattr(c, '__tablename__') and c.__tablename__ == refered_model_name:
                return c

    def foreign_keys_names(self):
        fk_columns = self.foreign_keys_columns()
        return [col.key for col in fk_columns]

    def schema_table_name(self) -> str:
        return f'{self.schema()}.{self.table_name()}'

    # todo: hardcoded
    def sequence_name(self) -> str:
        # return 's_' + self.table_name()
        return self.table_name() + "_seq"

    def schema_sequence(self) -> str:
        return f'{self.schema()}.{self.sequence_name()}'

    def columns_as_enum_column_names(self, columns: List[Column]) -> str:
        return ','.join([column.name for column in columns])

    def enum_column_names(self, column_names: List[str] = None) -> str:
        if column_names is not None:
            return ','.join(column_names)
        return ','.join(self.entity_class.column_names())

    def enum_colon_column_names(self, column_names: List[str] = None) -> str:
        if column_names is not None:
            return ','.join((':' + s for s in column_names))

        return ','.join((':' + s for s in self.entity_class.column_names()))

    def enum_equal_column_names(self, column_value: dict) -> str:
        return (','.join((key + ' = :' + key for key, value in column_value.items())))

    def column_names_given_attributes(self, attributes_from_path) -> List[str]:
        return self.entity_class.column_names_given_attributes(attributes_from_path)

    def column_names_alias(self, attrib_names: Optional[List[str]], prefix_col_val: str = None) -> str:
        raise NotImplementedError("'column_names_alias' must be implemented in subclasses")

    def enum_column_names_alias_attribute_given(self, list_attrib: Tuple[InstrumentedAttribute],
                                                prefix_col_val: str = None) -> str:
        list_attrib_column = self.list_attribute_column_given(list_attrib)
        return self.entity_class.enum_column_names_alias_attribute_given(list_attrib_column)

    def list_attribute_column_given(self, attributes_from_path: Optional[Tuple[str]]) -> List[Tuple]:
        return self.entity_class.list_attribute_column_given(attributes_from_path)

    def list_attribute_column_type(self) -> List[tuple]:
        return self.entity_class.list_attribute_column_type()

    def list_attribute_column_type_given(self, attributes: List[str]) -> List[tuple]:
        return self.entity_class.list_attribute_column_type_given(attributes)

    def attribute_names(self) -> List[str]:
        return [key for key, value in self.entity_class.attributes_with_dereferenceable()]

    def query_build_by(self, enum_fields: str = '', enum_schema_table: str ='', enum_join: str ='', enum_order_by:str = '', offsetlimit: str = '') -> str:
        raise NotImplementedError("'query_build_by' must be implemented in subclasses")

    def basic_select(self, list_attrib: List[str] = None, prefix_col_val: str = None) -> str:
        raise NotImplementedError("'basic_select' must be implemented in subclasses")

    def basic_select_by_id(self, pk, tuple_attrib: Tuple[str] = None, prefix_col_val: str = None):
        raise NotImplementedError("'basic_select_by_id' must be implemented in subclasses")

    def alias_column(self, inst_attr: InstrumentedAttribute, prefix_col: str = None):
        raise NotImplementedError("'alias_column' must be implemented in subclasses")

    @classmethod
    def dict_action(cls) -> Dict[str, ActionFunction]:
        """
        this dict has a function's name as key and value as ActionFunction
        :return: dict[str, ActionFunction]
        """
        return {}

    async def next_val(sequence_name: str):
        raise NotImplementedError("'next_val' must be implemented in subclasses")

    async def offset_limit(self, offset, limit, orderby=None, asc=None, format_row=None):
        raise NotImplementedError("'offset_limit' must be implemented in subclasses")

    async def fetch_all(self, list_attribute: Optional[List] = None, where: Optional[str] = None,
                        order_by: Optional[str] = None, prefix: Optional[str] = None):
        raise NotImplementedError("'fetch_all' must be implemented in subclasses")

    async def fetch_all_by(self, query: str):
        raise NotImplementedError("'fetch_all_by' must be implemented in subclasses")

    async def fetch_one(self, dic: dict, all_column: str = None, prefix_col_val: str = None):
        raise NotImplementedError("'fetch_one' must be implemented in subclasses")

    async def fetch_one_by(self, query: str):
        raise NotImplementedError("'fetch_one_by' must be implemented in subclasses")

    async def fetch_one_as_json(self, id_dict, prefix_col_val: str = None):
        raise NotImplementedError("'fetch_one_as_json' must be implemented in subclasses")

    async def fetch_all_as_json(self, tuple_attrib: Tuple[str] = None, a_query: str = None, prefix_col_val: str = None):
        raise NotImplementedError("'fetch_all_as_json' must be implemented in subclasses")

    async def count(self, where: str) -> int:
        raise NotImplementedError("'count' must be implemented in subclasses")

    async def sum(self, where: str) -> float:
        raise NotImplementedError("'sum' must be implemented in subclasses")

    async def avg(self, where: str) -> float:
        raise NotImplementedError("'avg' must be implemented in subclasses")

    async def min(self, column_name: str) -> Number:
        raise NotImplementedError("'min' must be implemented in subclasses")

    async def max(self, column_name: str) -> Number:
        raise NotImplementedError("'max' must be implemented in subclasses")

    def predicate_order_by(self, column_names: List[str], orders: List[str] = []) -> str:
        raise NotImplementedError("'order_by_predicate' must be implemented in subclasses")

    def predicate_offset_limit(self, offset: int, limit: int) -> str:
        raise NotImplementedError("'predicate_offset_limit' must be implemented in subclasses")

    def predicate_collect(self, column_names: List[str], predicate: str, prefix: str) -> str:
        raise NotImplementedError("'predicate_collect' must be implemented in subclasses")

    async def order_by(self, column_names: List[str], orders: List[str] = []):
        raise NotImplementedError("'order_by' must be implemented in subclasses")

    async def projection(self, str_attribute_as_comma_list, orderby=None):
        raise NotImplementedError("'projection' must be implemented in subclasses")

    async def group_by_count(enum, enum_attribute: str, orderby=None, format_row=None):
        raise NotImplementedError("'groupbycount' must be implemented in subclasses")

    async def group_by_sum(enum, enum_attribute: str, attr_to_sum, orderby=None, format_row=None):
        raise NotImplementedError("'groupbycount' must be implemented in subclasses")

    async def filter(self, a_filter: str):
        raise NotImplementedError("'filter' must be implemented in subclasses")

    async def filter_as_json(self, a_filter, e_column_names: str = None, prefix_col_val: str = None):
        raise NotImplementedError("'filter_as_json' must be implemented in subclasses")

    async def delete(self, id_or_dict):
        raise NotImplementedError("'delete' must be implemented in subclasses")

    async def update(self, id_dict: dict, field_value: dict):
        raise NotImplementedError("'update' must be implemented in subclasses")

    async def insert(self, field_value: dict) -> Any:
        raise NotImplementedError("'insert' must be implemented in subclasses")

    async def fetch_one_model(self, pk_or_key_value_tuple, key_value: Dict = None, tuple_attrib: Tuple[str] = None,
                              prefix_col_val: str = None) -> Optional[AlchemyBase]:
        raise NotImplementedError("'fetch_one_model' must be implemented in subclasses")

    async def convert_row_to_dict(self, row) -> Dict:
        raise NotImplementedError("'convert_row_to_dict' must be implemented in subclasses")

    async def convert_to_db_string(self, string: str) -> str:
        if string[0] == "'" and string[-1] == "'":
            return f'{string}'

        return f"'{string}'"

    async def convert_to_db_int(self, string: str) -> int:
        return int(string)

    async def convert_to_db_float(self, string: str) -> float:
        return float(string)

    async def convert_to_db_date(self, string: str) -> str:
        dt: datetime.date = await ConverterType().convert_to_date(string)
        return dt.isoformat()

    async def convert_to_db_datetime(self, string: str) -> str:
        dt: datetime.datetime = await ConverterType().convert_to_datetime(string)
        return dt.isoformat()

    async def convert_to_db_time(self, string: str) -> str:
        t: datetime.time = await ConverterType().convert_to_time(string)
        return t.isoformat()

    def value_has_url(self, value_str: str) -> bool:
        return (value_str.find('http:') > -1) or (value_str.find('https:') > -1) or (value_str.find('www.') > -1)

    def value_seems_json(self, value_str: str) -> bool:
        return value_str.startswith('{') and value_str.endswith('}')

    async def convert_to_db_geometry(self, value_as_str: str) -> str:
        raise NotImplementedError("'convert_to_db_geometry' must be implemented in subclasses")

    def last_action_in_chain(self,a_type: type, action_names: List[str]) -> ActionFunction:
        raise NotImplementedError("'last_action_in_chain' must be implemented in subclasses")

    def type_of_last_action_in_chain(self,a_type: type, action_names: List[str]) -> object:
        raise NotImplementedError("'type_of_last_action_in_chain' must be implemented in subclasses")


    async def operation_to_convert_db_value(self, a_type) -> object:
        d = dict()
        d[str] = self.convert_to_db_string
        d[String] = self.convert_to_db_string
        d[int] = self.convert_to_db_int
        d[Integer] = self.convert_to_db_int
        d[SmallInteger] = self.convert_to_db_int
        d[float] = self.convert_to_db_float
        d[Float] = self.convert_to_db_float
        d[Numeric] = self.convert_to_db_float
        d[date] = self.convert_to_db_date
        d[datetime] = self.convert_to_db_datetime
        d[datetime.time] = self.convert_to_db_time
        d[Geometry] = self.convert_to_db_geometry
        d[BaseGeometry] = self.convert_to_db_geometry
        d[Polygon] = self.convert_to_db_geometry
        d[LineString] = self.convert_to_db_geometry
        d[Point] = self.convert_to_db_geometry
        d[MultiPolygon] = self.convert_to_db_geometry
        d[MultiLineString] = self.convert_to_db_geometry
        d[MultiPoint] = self.convert_to_db_geometry

        d[ForeignKey] = self.convert_to_db_int

        return d[a_type]

    async def value_db_converted(self, param_value: str, a_type: type) -> object:
        object_method = await self.operation_to_convert_db_value(a_type)
        return await object_method(param_value)

    async def convert_in_db_args(self, in_arg: str, a_type: type) -> str:
        if a_type in (str, String):
            args = in_arg.split(',')
            args_str = [f"'{arg}'" for arg in args]
            return ','.join(args_str)
        else:
            return f'{in_arg}'

    async def convert_db_args(self, args: List[str], types: List[type]) -> str:
        converted_params: List[str] = []
        for idx, arg in enumerate(args):
            a_type = types[idx]
            obj = await self.value_db_converted(arg, a_type)
            converted_params.append(f'{obj}')

        return ','.join(converted_params)
