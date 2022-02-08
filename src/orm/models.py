# from __future__ import annotations
from typing import Dict, Tuple, Sequence, List, Any, Optional

from sqlalchemy import ForeignKey
from sqlalchemy.orm import ColumnProperty, RelationshipProperty
from sqlalchemy.orm.attributes import InstrumentedAttribute

from src.hyper_resource.basic_route import BasicRoute
from src.orm.action_type import FUNCTION, Action
from src.orm.dictionary_actions import *
from src.orm.converter import ConverterType
from sqlalchemy.orm import declarative_base

Base = declarative_base()

class AlchemyBase(Base):
    dialect_db = None
    _dic = None
    __abstract__ = True

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
        elif isinstance(inst_attr.prop, RelationshipProperty) and list(inst_attr.prop._user_defined_foreign_keys)[0] is not None:
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
    def has_attribute(cls, attribute_name: str) -> bool:
        return attribute_name in cls.all_attribute_names()
    @classmethod
    def attribute_name_given(cls, attribute: InstrumentedAttribute)-> str:
        return attribute.prop.key
    @classmethod
    def attribute_column_type(cls, attribute_name) -> Tuple[str, str, str]:
        lst_a_c_t = cls.list_attribute_column_type()
        return next(a_c_t for a_c_t in lst_a_c_t if a_c_t[0] == attribute_name)
        #next((x for x in lst if ...), [default value])

    @classmethod
    def attribute_type_given(cls, attribute_name: str) -> Optional[type]:
        cols = cls.__table__.c
        if attribute_name not in cols:
            return None
        col = cols[attribute_name]
        return type(col.type)

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
    def attribute_names_with_dereferenceable(cls, attrib: InstrumentedAttribute = None) -> List[str]:
        """
        in sqlalchemy relationship is created with Relationship class and frequently
        with ForeignKey attribute too. But it is not necessary show both attributes.
        attribute_names_with_dereferenceable get attributes (InstrumentedAttribute) of type:
         ColumnProperty, PrimaryKey and Relationship
        :param attrib:
        :return:
        """
        items = cls.__dict__.items() if attrib is None else attrib.__dict__.items()
        return [key for key, value in items if
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
    def model_class_for_relationship_attribute(cls, instrumentedAttribute : InstrumentedAttribute):
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
    def list_attribute_column_type(cls) -> List[Tuple[str, str, str]]:
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
    def column_names_given_attributes(cls, attributes_from_path: List[str]) -> List[str]:
        return [ col for att, col in cls.list_attribute_column() if att in attributes_from_path]

    @classmethod
    def enum_column_names_alias_attribute_given(cls, list_attrib_column: List[Tuple], prefix_col_val: str = None) -> str:
        res = ','.join(( col + ' as ' + att) for att, col in list_attrib_column)
        return res
    @classmethod
    def enum_column_names_as_given_attributes(cls, attributes_from_path: List[str]) -> str:
        return ','.join(cls.column_names_given_attributes(attributes_from_path))

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

    @classmethod
    def action_dic(cls) -> Dict[type, Dict]:
        """
        :return: This method returns a dictionary to get function/attribute supported in a request.
        The key is a type/class and value is a dictionary(key: operation/attribute name, value: Action instance
        """

        _dic = {'projection': ActionFunction('projection', cls, [ ParamAction('string_enum', str)]),}
        return {cls: _dic}

    @classmethod
    def validate_path(cls, a_path: str):
        if cls.is_projection_from_path(a_path):
            attrib_names = [att.strip() for att in a_path.split('/')[0].split(',')]
            dif_set = (set(attrib_names) - set(cls.attribute_names_with_dereferenceable()))
            if len(dif_set) > 0:
                raise AttributeError(f"The list of attribute not exists: {dif_set.__str__()}")
            return 'is_projection'

    @classmethod
    def is_attribute_from_path(cls, path: str) -> bool:
        pass

    @classmethod
    def path_has_url(cls, path: str)-> bool:
        return '/(/http:' in path or '/(/https:' in path

    @classmethod
    def path_with_url_splitted(cls, path : str)-> List[str]:
        """
        :param path must have an url> example: geom/contains/(/http://unidade-federacao/rj/geom/)/
        :return: List[str]
        """
        idx_ini = path.find('/(/http')
        if idx_ini == -1:
            raise SyntaxError(f"Problem with {path}. Verify if path has balanced parentheses and http")
        first_part_lst = (path[0:idx_ini]).split('/')
        idx_midst = path.find('/)', idx_ini)
        if idx_midst == -1:
            raise SyntaxError(f"Problem with {path}. Verify if path has balanced parentheses ---'/(/'---'/)/'---  and http")
        middle_part_lst = (path[idx_ini + 3:idx_midst])
        return first_part_lst + [middle_part_lst]
    @classmethod
    def path_as_list(cls, path: str) -> List[str]:
        if path[-1] == '/':  # Removes trail slash
            path = path[:-1]
        if cls.path_has_url(path):
            return cls.path_with_url_splitted(path)
        return path.split('/')
    @classmethod
    def is_only_attribute_list_from_path(cls, path: str) -> bool:
        """
            :param path is a string and should be this format  /attribute1,attribute12  ...

            :return: True if path has only attributes otherwise False. Raise exception if any attribute does not exists
        """
        arr_str = cls.path_as_list(path)
        if len(arr_str) > 1:
            return False
        attri_names = [att.strip() for att in arr_str[0].split(',')]
        diff_set = set(attri_names) - set(cls.attribute_names_with_dereferenceable())
        if len(diff_set) > 0:
            return False
            #raise AttributeError(f"The list of attribute {diff_set.__str__()} is not supported")
        else:
            return True
    @classmethod
    def starts_by_one_attribute_with_functions(cls, path: str) -> bool:
        """
        :param path must have only one attribute and functions after it.
        :return:
        """
        arr_str = cls.path_as_list(path)
        return len(arr_str) > 1 and len(arr_str[0].split(',')) == 1 and cls.has_attribute(arr_str[0])
    @classmethod
    def is_projection_from_path(cls, path: str) -> bool:
        """
        :param path is a string and should be this format  /attribute1,attribute12  ...
        :return: True if path has only attributes otherwise False
        """
        arr_str = cls.path_as_list(path)
        if len(arr_str) > 1:
            return False
        attri_names = [att.strip() for att in arr_str[0].split(',')]
        return len(set(attri_names) - set(cls.attribute_names_with_dereferenceable()))== 0

    def projection(self, string_enum: str) -> object:
        enum = string_enum.split(',')
        dic_attr = {}
        if len(enum) == 1:
            return getattr(self, enum[0])
        for att_name in enum:
            dic_attr[att_name] = getattr(self, att_name)
        return dic_attr
    def object_has_action(self, a_type: type, action_name: str) -> object:

        if a_type not in dic_action:
            return False

        return action_name in dic_action[a_type]

    def is_projection_with_operation_from_path(self, path: str) -> bool:
        """
        :param path is a string and should be this format  /attribute1,attribute12  ...
        :return: True if path has only attributes otherwise False
        """
        pass

    async def converter_parameters(self, params: List[str], param_type_arr: List[tuple]) -> List:
        return await ConverterType().convert_parameters(params, param_type_arr)

    def get_action(self, a_type: type, action_name: str) -> Action:
        return self.__class__.action_dic()[a_type][action_name]

    async def execute_action(self, obj, action_names: List[str]) -> object:
        action_name = action_names.pop(0)
        if not self.object_has_action(type(obj), action_name):
            raise NotImplementedError(f"The function {action_name} is not implemented in {type(obj)}")
        action = self.get_action(type(obj), action_name)
        return await action.execute(obj, action_names)

    async def execute_actionOLD(self, obj, arr_actions: List[str]) -> object:
        action = arr_actions.pop(0)
        if not self.object_has_action(type(obj), action):
            raise NotImplementedError(f"The function {action} is not implemented in {type(obj)}")
        tuple_dic_int = self.__class__.action_dic()[type(obj)][action]
        if tuple_dic_int[1] == FUNCTION:
            annotation_dic = tuple_dic_int[0]
            param_type_arr = [ (key, value) for key, value in annotation_dic.items() if key != 'return']
            if len(param_type_arr) == 0:
                result = getattr(obj, action)()
            else:
                if len(arr_actions) == 0:
                    para_text = f" these parameters: {param_type_arr}" if len(param_type_arr) > 1 else f" this parameter: {param_type_arr}"
                    raise SyntaxError(f"The operation {action} must have at least {para_text}")
                params = arr_actions.pop(0).split('&')
                paramets = await self.converter_parameters(params, param_type_arr)
                result = getattr(obj, action)(*paramets)
        else:
            result = getattr(obj, action)
        return result

    async def execute_attribute_given(self, path: str):
        """
        :param path is a string and have to start with one attribute
        :return: dictionary with result
        """
        arr_actions = self.__class__.path_as_list(path)
        obj = getattr(self, arr_actions[0])
        arr_actions = arr_actions[1:]
        while len(arr_actions) > 0:
            obj = await self.execute_action(obj, arr_actions)
        return obj
    async def execute_function_given(self, path: str) -> object:
        """
        :param path is a string and have to start with one function
        :return: object. It could be any thing. For instance: int, str, float, geometry etc
        """
        arr_actions = self.__class__.path_as_list(path)
        obj = self
        while len(arr_actions) > 0:
            obj = await self.execute_action(obj, arr_actions)
        return obj

    def properties_dict(self, attrib_names: List[str] = None) -> Dict:
        dic = {}
        attrs = attrib_names if attrib_names is not None else self.__class__.attribute_names_with_dereferenceable()
        for attr_name in attrs:
            dic[attr_name] = getattr(self, attr_name)
        return dic

    def json_dict(self, attrib_names: List[str] = None) -> dict:
        return self.properties_dict(attrib_names)
