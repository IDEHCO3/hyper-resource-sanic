import typing
from typing import List, Union

from src.hyper_resource.abstract_resource import AbstractResource
from src.hyper_resource.common_resource import HTTP_GET_METHOD, CONTENT_TYPE_JSON, CONTENT_TYPE_HEADER, STATUS_OK
from src.orm.database import DialectDatabase
from src.hyper_resource.context.context_types import SQLALCHEMY_SCHEMA_ORG_TYPES, PYTHON_SCHEMA_ORG_TYPES, \
    HYPER_RESOURCE_TYPES, MIME_TYPES_FOR_TYPE, ACONTEXT_KEYWORD, ATYPE_KEYWORD, AID_KEYWORD, \
    SUPPORTED_OPERATIONS_KEYWORD, SUPPORTED_PROPERTIES_KEYWORD, OPERATION_KEYWORD, APPEND_PATH_KEYWORD, \
    VARIABLE_PATH_KEYWORD, REQUIRED_PARAMETER_PATH_KEYWORD, OPERATION_PARAMETER_KEYWORD, EXPECTS_KEYWORD_SERIALIZATION, \
    PARAMETERS_KEYWORD, IS_EXTERNAL_KEYWORD, HYDRA_METHOD_KEYWORD, HYDRA_RETURNS_HEADER_KEYWORD, \
    HYDRA_HEADER_NAME_KEYWORD, HYDRA_POSSIBLE_VALUE_KEYWORD, HYDRA_POSSIBLE_STATUS_VALUE_KEYWORD, \
    HYDRA_EXPECTS_HEADER_KEYWORD, HYDRA_EXPECTS_KEYWORD, HYDRA_SUPPORTED_PROPERTY_KEYWORD, HYDRA_PROPERTY_KEYWORD, \
    HYDRA_REQUIRED_KEYWORD, HYDRA_READABLE_KEYWORD, HYDRA_WRITABLE_KEYWORD
import copy
from environs import Env

from src.url_interpreter.interpreter_types import COLLECTION_EXPOSED_OPERATIONS, COLLECTION_TYPES_OPERATIONS, Operator

env = Env()
env.read_env()
port = env.str("PORT", "8002")
host = env.str("HOST", "127.0.0.1")

PREFIX_HYPER_RESOURCE = "hr"
PREFIX_SCHEMA_ORG = "schema"

VOCABS_TEMPLATE = {
    f"{ACONTEXT_KEYWORD}": {
        f"{PREFIX_HYPER_RESOURCE}": f"http://hyper-resource.org/core",
        f"{PREFIX_SCHEMA_ORG}": "http://schema.org/",
        "id": AID_KEYWORD,
    }
}

class AbstractContext(object):
    def __init__(self, db_dialect:DialectDatabase, metadata_table, entity_class):
        self.db_dialect = db_dialect
        self.metadata_table = metadata_table
        self.entity_class = entity_class

    def get_basic_context(self):
        context = copy.deepcopy(VOCABS_TEMPLATE)
        context[ACONTEXT_KEYWORD].update(self.get_properties_term_definition_dict())
        # context.update(self.get_type_by_model_class())
        context.update(AbstractResource.MAP_MODEL_FOR_CONTEXT[self.entity_class].get_type_by_model_class())
        return context

    def get_operation_append_path(self, func) -> str:
        params_list = "/".join(["{" + f"param{val}" + "}" for val in range(0, len(func.__annotations__.items()) - 1)])
        if params_list != "":
            params_list = "/" + params_list

        append_path = f"/{func.__name__}" + params_list
        return append_path

    def get_expects_for_parameter_type(self, parameter_type):
        return HYPER_RESOURCE_TYPES[parameter_type]

    def get_default_returns_header(self):
        returns_header = []
        possibleValue = [CONTENT_TYPE_JSON]
        returns_header.append({HYDRA_HEADER_NAME_KEYWORD: CONTENT_TYPE_HEADER, HYDRA_POSSIBLE_VALUE_KEYWORD: possibleValue})
        return returns_header

    def get_default_geometry_expects_header(self):
        expects_header = []
        possibleValue = [CONTENT_TYPE_JSON]
        expects_header.append({HYDRA_HEADER_NAME_KEYWORD: CONTENT_TYPE_HEADER, HYDRA_POSSIBLE_VALUE_KEYWORD: possibleValue})
        return expects_header

    def get_default_possible_status(self):
        return [STATUS_OK]

    def get_expected_serialization_for_parameter_type(self, parameter_type):
        return MIME_TYPES_FOR_TYPE[parameter_type]

    def get_projection_context(self, attributes: List[str]):
        context = copy.deepcopy(VOCABS_TEMPLATE)
        context[ACONTEXT_KEYWORD].pop(PREFIX_HYPER_RESOURCE)
        filtered_term_def_dict = dict()
        for term, definition in self.get_properties_term_definition_dict().items():
            if term in attributes:
                filtered_term_def_dict.update({term: definition})
        context[ACONTEXT_KEYWORD].update(filtered_term_def_dict)
        context.update(AbstractResource.MAP_MODEL_FOR_CONTEXT[self.entity_class].get_type_by_model_class())
        return context

    def get_foreign_key_context(self, fk_model):
        d = AbstractResource.MAP_MODEL_FOR_CONTEXT[fk_model].get_type_by_model_class()
        fk_context = {ATYPE_KEYWORD: AID_KEYWORD}
        fk_context[AID_KEYWORD] = d[ATYPE_KEYWORD]
        return fk_context

    def get_properties_term_definition_dict(self):
        fk_column_names = self.db_dialect.foreign_keys_names()
        term_definition_dict = {}
        for column in self.metadata_table.columns:
            if column.primary_key:
                continue
            if str(column.name) in fk_column_names:
                fk_col = self.db_dialect.foreign_key_column_by_name(column.name)
                fk_model = self.db_dialect.get_model_by_foreign_key(fk_col)
                term_definition_dict[str(column.name)] = self.get_foreign_key_context(fk_model)
            else:
                term_definition_dict[str(column.name)] = SQLALCHEMY_SCHEMA_ORG_TYPES[type(column.type)]
        return term_definition_dict

    @staticmethod
    def get_type_by_model_class():
        return {ATYPE_KEYWORD: PYTHON_SCHEMA_ORG_TYPES[object]}


class AbstractCollectionContext(AbstractContext):

    def get_basic_supported_operations(self) -> dict:
        supported_operations = []
        for _type, operations in COLLECTION_TYPES_OPERATIONS.items():
            for op in operations:

                append_path = self.get_operation_append_path(op)
                operation_dict = {
                    ATYPE_KEYWORD: OPERATION_KEYWORD,
                    HYDRA_METHOD_KEYWORD: HTTP_GET_METHOD,
                    APPEND_PATH_KEYWORD: append_path,
                    PARAMETERS_KEYWORD: []
                }

                operation_dict.update({HYDRA_RETURNS_HEADER_KEYWORD: self.get_default_returns_header()})
                operation_dict.update({HYDRA_EXPECTS_HEADER_KEYWORD: self.get_default_geometry_expects_header()})
                operation_dict.update({HYDRA_POSSIBLE_STATUS_VALUE_KEYWORD: self.get_default_possible_status()})

                key = 0
                for parameter_name, parameter_type in op.__annotations__.items():

                    if not parameter_name == "return":

                        types_in_union = typing.get_args(parameter_type)
                        if len(types_in_union) > 0:
                            for _type in types_in_union:
                                param_dict = self.get_operation_parameter(key, _type)
                                operation_dict[PARAMETERS_KEYWORD].append(param_dict)
                        else:
                            param_dict = self.get_operation_parameter(key, parameter_type)
                            operation_dict[PARAMETERS_KEYWORD].append(param_dict)
                        key = key + 1
                supported_operations.append(operation_dict)
        return {SUPPORTED_OPERATIONS_KEYWORD: supported_operations}

    def get_operation_parameter(self, key, parameter_type):
        return {
            ATYPE_KEYWORD: OPERATION_PARAMETER_KEYWORD,
            VARIABLE_PATH_KEYWORD: f"param{key}",
            REQUIRED_PARAMETER_PATH_KEYWORD: True,  # todo: hardcoded
            HYDRA_EXPECTS_KEYWORD: self.get_operation_parameter_expects(parameter_type),
            EXPECTS_KEYWORD_SERIALIZATION: self.get_expected_serialization_for_parameter_type(parameter_type)
        }

    def get_operation_parameter_expects(self, parameter_type):
        try:
            if issubclass(parameter_type, Operator):
                _expects = parameter_type.build().symbol
            else:
                _expects = self.get_expects_for_parameter_type(parameter_type)
        except TypeError:
            _expects = self.get_expects_for_parameter_type(parameter_type)
        return _expects

    def get_basic_context(self):
        context = copy.deepcopy(VOCABS_TEMPLATE)
        context[ACONTEXT_KEYWORD].update(self.get_properties_term_definition_dict())
        context.update(AbstractResource.MAP_MODEL_FOR_CONTEXT[self.entity_class].get_type_by_model_class())
        context.update(self.get_basic_supported_properties())
        context.update(self.get_basic_supported_operations)
        return context

    def get_basic_supported_properties(self) -> dict:
        supported_properties = []
        for column in self.metadata_table.columns:
            # WARNING: must check if the property is a dereferencable
            is_fk = column.name in self.db_dialect.foreign_keys_names()
            property_dict = {
                ATYPE_KEYWORD: HYDRA_SUPPORTED_PROPERTY_KEYWORD,
                HYDRA_PROPERTY_KEYWORD: column.name,
                HYDRA_REQUIRED_KEYWORD: not column.nullable,
                HYDRA_READABLE_KEYWORD: True,
                HYDRA_WRITABLE_KEYWORD: not column.primary_key,
                IS_EXTERNAL_KEYWORD: is_fk
            }
            supported_properties.append(property_dict)
        d = {SUPPORTED_PROPERTIES_KEYWORD: supported_properties}
        return d

class AbstractDetailContext(AbstractContext):
    pass