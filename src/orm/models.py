from typing import Dict, Tuple, Sequence, List
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm.attributes import InstrumentedAttribute

Base = declarative_base()


class AlchemyBase:
    @classmethod     
    def schema(cls) -> str:
        return cls.__table_args__ ['schema']
    @classmethod
    def table_name(cls) -> str:
        return cls.__table__.name

    @classmethod
    def primary_key(cls) -> str:
        return next(c.key for c in cls.__table__.columns if c.primary_key)

    @classmethod
    def attribute_names(cls) ->List[str]:
        return [ value.key for key, value in cls.__dict__.items() if isinstance(value, InstrumentedAttribute)]
    
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
        return [ (key, value.prop.columns[0].name) for key, value in cls.__dict__.items() if isinstance(value, InstrumentedAttribute)]

    @classmethod
    def list_attribute_column_type(cls) -> List[Tuple]:
        return [(key, value.prop.columns[0].name, value.prop.columns[0].type.__str__()) for key, value in cls.__dict__.items() if isinstance(value, InstrumentedAttribute)]

    @classmethod
    def column_names(cls)-> List[str]:
        return [col.name for col in cls.__table__.columns]

    @classmethod
    def column_name(cls, attribute_name) -> str:
        return next(att for att, col in cls.list_attribute_column() if att == attribute_name)

    @classmethod
    def column_names_given_attributes(cls, attributes_from_path) -> List[str]:
        return [ col for att, col in cls.list_attribute_column() if att in attributes_from_path]

    @classmethod
    def column_names_as_enum_given_attributes(cls, attributes_from_path) -> str:
        return ','.join(cls.column_names_given_attributes(attributes_from_path))

    @classmethod
    def column_names_as_enum(cls) -> str:
        return ','.join(cls.column_names())