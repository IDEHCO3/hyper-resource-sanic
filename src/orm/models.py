from typing import Dict, Tuple, Sequence, List, Any

from sqlalchemy import ForeignKey
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import ColumnProperty
from sqlalchemy.orm.attributes import InstrumentedAttribute
Base = declarative_base()

class AlchemyBase:
    dialect_db = None
    @classmethod     
    def schema(cls) -> str:
        return cls.__table_args__ ['schema']
    @classmethod
    def table_name(cls) -> str:
        return cls.__table__.name
    @classmethod
    def primary_key(cls) -> str:
        return cls.__table__.primary_key.columns[0].name

    @classmethod
    def is_attribute_without_relationship(cls, attribute):
        return isinstance(attribute, InstrumentedAttribute) and isinstance(attribute.prop, ColumnProperty)
    @classmethod
    def attribute_names(cls) ->List[str]:
        return [ key for key, value in cls.__dict__.items() if cls.is_attribute_without_relationship(value)]
    @classmethod
    def has_attribute(cls, attribute_name) -> bool:
        return attribute_name in cls.attribute_names()
    @classmethod
    def attribute_column_type(cls, attribute_name) -> tuple:
        lst_a_c_t = cls.list_attribute_column_type()
        return next(a_c_t for a_c_t in lst_a_c_t if a_c_t[0] == attribute_name)
        #next((x for x in lst if ...), [default value])
    @classmethod
    def list_attribute_column(cls) -> List[Tuple]:
        return [ (key, value.prop.columns[0].name) for key, value in cls.__dict__.items() if cls.is_attribute_without_relationship(value)]
    @classmethod
    def list_attribute_column_given(cls,attributes_from_path: Tuple[str]) -> List[Tuple]:
        if attributes_from_path is None:
            return cls.list_attribute_column_type()
        return [(attrib_name, column_name) for (attrib_name, column_name) in cls.list_attribute_column() if attrib_name in attributes_from_path]
    @classmethod
    def list_attribute_column_type(cls) -> List[Tuple]:
        return [(key, value.prop.columns[0].name, value.prop.columns[0].type.__str__()) for key, value in cls.__dict__.items() if cls.is_attribute_without_relationship(value)]
    @classmethod
    def list_attribute_column_type_given(cls, attributes : List[str]) -> List[Tuple]:
        return [(key, value.prop.columns[0].name, value.prop.columns[0].type.__str__()) for key, value in
                cls.__dict__.items() if cls.is_attribute_without_relationship(value) and (key in attributes)]
    @classmethod
    def column_names(cls)-> List[str]:
        return [col.name for col in cls.__table__.columns if not isinstance(col, ForeignKey)]
    @classmethod
    def column_name(cls, attribute_name: str) -> str:
        return next(att for att, col in cls.list_attribute_column() if att == attribute_name)
    @classmethod
    def column_names_given_attributes(cls, attributes_from_path) -> List[str]:
        return [ col for att, col in cls.list_attribute_column() if att in attributes_from_path]
    @classmethod
    def enum_column_names_alias_attribute_given(cls, list_attrib_column: List[Tuple]) -> str:
        return ','.join((col + ' as ' + att for att, col in list_attrib_column))
    @classmethod
    def enum_column_names_as_given_attributes(cls, attributes_from_path) -> str:
        return ','.join(cls.column_names_given_attributes(attributes_from_path))
    @classmethod
    def dict_name_operation(cls) -> Dict:
        return {
            "attribute_starts_with" : AlchemyBase.attribute_starts_with
        }
    @classmethod
    def reflection_operation(cls, operation_name) -> str:
        if operation_name not in cls.dict_name_operation():
            raise LookupError(f'This {operation_name} is not supported')
        return cls.dict_name_operation()[operation_name].__annotations__
    def attribute_starts_with(self, attribute: str) -> 'AlchemyBase':
        return None

class AlchemyGeoBase(AlchemyBase):
    @classmethod
    def geo_column_name(cls) -> str:
        return next((tuple_name_type[0] for tuple_name_type in cls.list_attribute_column_type() if tuple_name_type[2].startswith('geometry(')), None)
