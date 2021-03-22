from typing import Dict, Tuple, Sequence, List, Any

from sqlalchemy import ForeignKey
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import ColumnProperty, RelationshipProperty
from sqlalchemy.orm.attributes import InstrumentedAttribute
from sqlalchemy.orm.decl_api import DeclarativeMeta

from src.hyper_resource.basic_route import BasicRoute

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
    def is_primary_key(cls, attribute: InstrumentedAttribute) -> bool:
        return isinstance(attribute.prop, ColumnProperty) and attribute.prop.columns[0].primary_key
    @classmethod
    def is_foreign_key_attribute(cls, attribute) -> bool:
        return isinstance(attribute, InstrumentedAttribute) and isinstance(attribute.prop, ColumnProperty) and (len(attribute.prop.columns[0].foreign_keys) > 0)

    @classmethod
    def is_not_foreign_key_attribute(cls, attribute) -> bool:
        return isinstance(attribute, InstrumentedAttribute) and isinstance(attribute.prop, ColumnProperty) and (len(attribute.prop.columns[0].foreign_keys) == 0)
    @classmethod
    def is_relationship_attribute(cls, attribute):
        return isinstance(attribute, InstrumentedAttribute) and isinstance(attribute.prop, RelationshipProperty)

    @classmethod
    def is_relationship_fk_attribute(cls, attribute):
        return cls.is_relationship_attribute(attribute) and attribute.prop._user_defined_foreign_keys is not None

    @classmethod
    def column_name_or_None(cls, inst_attr: InstrumentedAttribute):
        if isinstance(inst_attr.prop, ColumnProperty):
            return inst_attr.prop.columns[0].name
        elif isinstance(inst_attr.prop, RelationshipProperty) and inst_attr.prop._user_defined_foreign_keys[0] is not None:
            return inst_attr.prop._user_defined_foreign_keys[0].name
        return None
    @classmethod
    def class_given_relationship_fk(cls, inst_attr: InstrumentedAttribute):
        return inst_attr.prop.entity.class_
    @classmethod
    def is_attribute_without_relationship(cls, attribute):
        return isinstance(attribute, InstrumentedAttribute) and isinstance(attribute.prop, ColumnProperty)
    @classmethod
    def attribute_names(cls) ->List[str]:
        return [ key for key, value in cls.__dict__.items() if cls.is_attribute_without_relationship(value)]
    @classmethod
    def all_attribute_names(cls) -> List[str]:
        return [key for key, value in cls.__dict__.items() if isinstance(value, InstrumentedAttribute)]
    @classmethod
    def has_attribute(cls, attribute_name) -> bool:
        return attribute_name in cls.attribute_names()
    @classmethod
    def attribute_name_given(cls, attribute: InstrumentedAttribute)-> str:
        return attribute.prop.key
    @classmethod
    def attribute_column_type(cls, attribute_name) -> tuple:
        lst_a_c_t = cls.list_attribute_column_type()
        return next(a_c_t for a_c_t in lst_a_c_t if a_c_t[0] == attribute_name)
        #next((x for x in lst if ...), [default value])
    @classmethod
    def attributes_from_path_not_exist(cls, enum_attr_from_path) -> List[str]:
        set_atts_from_path = set(enum_attr_from_path.split(','))
        set_result = set_atts_from_path.difference(set(cls.attribute_names()))
        if len(set_result) == 0:
            return []
        list_attrib = []
        #for att_name in set_result:
    @classmethod
    def relationship_attributes(cls) -> List[InstrumentedAttribute]:
        return [ value for key, value in cls.__dict__.items() if cls.is_relationship_attribute(value)]

    @classmethod
    def attributes_with_dereferenceable(cls, attrib=None) -> List[tuple]:
        items = cls.__dict__.items() if attrib is None else attrib.__dict__.items()
        return [(key, value) for key, value in items if
                         cls.is_not_foreign_key_attribute(value) or cls.is_relationship_attribute(value)]
    @classmethod
    def model_class_given(cls, relationship_attribute : RelationshipProperty):
        return relationship_attribute.prop.mapper.class_

    @classmethod
    def all_attributes_with_dereferenceable(cls, level=1) -> List[str]:
        if level > 3:
            return []
        list_name_attrib = cls.attributes_with_dereferenceable()
        arr = []
        for name, attrib in list_name_attrib:
            arr.append(name)
            if cls.is_relationship_attribute(attrib):
                arr.append(name + '.*')
                arr = arr + cls.model_class_given(attrib).all_attributes_with_dereferenceable(level + 1)
        return arr
    @classmethod
    def model_class_for_relationship_attribute(cls, instrumentedAttribute : InstrumentedAttribute) -> DeclarativeMeta:
        return instrumentedAttribute.prop.entity.class_
    @classmethod
    def fk_or_none_n_relationship_given(cls, attribute_name : str) -> str:
        prop = cls.__dict__[attribute_name].prop
        if not isinstance(prop, RelationshipProperty):
            return None
        cols = prop.mapper.columns
        for col in cols: #pessoa.gastos => ForeignKey('pessoal.gasto.id_pessoa')
            if len(col.foreign_keys) > 0 and col.foreign_keys.pop().target_fullname.split('.')[-1] == cls.primary_key():
                return col.key
        return None
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
        attribute = cls.__dict__[attribute_name]
        return cls.column_name_or_None(attribute)
    @classmethod
    def column_names_given_attributes(cls, attributes_from_path) -> List[str]:
        return [ col for att, col in cls.list_attribute_column() if att in attributes_from_path]

    @classmethod
    def enum_column_names_alias_attribute_given(cls, list_attrib_column: List[Tuple], prefix_col_val: str = None) -> str:
        res = ','.join(( col + ' as ' + att) for att, col in list_attrib_column)
        return res
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

    @classmethod
    def router_id(cls):
        return BasicRoute.router_id(cls.model_class)

    @classmethod
    def router_id_path(cls):
        return BasicRoute.router_id_path(cls)

    @classmethod
    def router_list(cls):
        return BasicRoute.router_list(cls)

    @classmethod
    def router_list_path(cls):
        return BasicRoute.router_list_path(cls)

class AlchemyGeoBase(AlchemyBase):
    @classmethod
    def geo_column_name(cls) -> str:
        return next((tuple_name_type[0] for tuple_name_type in cls.list_attribute_column_type() if tuple_name_type[2].startswith('geometry(')), None)
