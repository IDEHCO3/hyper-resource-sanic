from typing import List

from src.hyper_resource.abstract_resource import AbstractResource
from src.orm.database import DialectDatabase
from src.hyper_resource.context.context_types import SQLALCHEMY_SCHEMA_ORG_TYPES, PYTHON_SCHEMA_ORG_TYPES
import copy
from environs import Env
from sqlalchemy.inspection import inspect

ACONTEXT_KEYWORD = "@context"
ATYPE_KEYWORD = "@type"
AID_KEYWORD = "@id"
ASET_KEYWORD = "@set"
ACONTAINER_KEYWORD = "@container"
HYPER_RESOURCE_VOCAB_KEY = "hr"
SUPPORTED_OPERATIONS_KEYWORD = f"{HYPER_RESOURCE_VOCAB_KEY}:supportedOperations"
SUPPORTED_PROPERTIES_KEYWORD = f"{HYPER_RESOURCE_VOCAB_KEY}:supportedProperty"
OPERATION_KEYWORD = f"{HYPER_RESOURCE_VOCAB_KEY}:Operation"
APPEND_PATH_KEYWORD = f"{HYPER_RESOURCE_VOCAB_KEY}:appendPath"
VARIABLE_PATH_KEYWORD = f"{HYPER_RESOURCE_VOCAB_KEY}:variable"
REQUIRED_PARAMETER_PATH_KEYWORD = f"{HYPER_RESOURCE_VOCAB_KEY}:requiredParameter"
OPERATION_PARAMETER_KEYWORD = f"{HYPER_RESOURCE_VOCAB_KEY}:OperationParameter"
EXPECTS_KEYWORD_SERIALIZATION = f"{HYPER_RESOURCE_VOCAB_KEY}:expectsSerialization"
PARAMETERS_KEYWORD = f"{HYPER_RESOURCE_VOCAB_KEY}:parameters"
IS_EXTERNAL_KEYWORD = f"{HYPER_RESOURCE_VOCAB_KEY}:isExternal"

HYDRA_VOCAB_KEY = "hydra"
HYDRA_METHOD_KEYWORD = f"{HYDRA_VOCAB_KEY}:method"
HYDRA_RETURNS_HEADER_KEYWORD = f"{HYDRA_VOCAB_KEY}:returnsHeader"
HYDRA_HEADER_NAME_KEYWORD = f"{HYDRA_VOCAB_KEY}:headerName"
HYDRA_POSSIBLE_VALUE_KEYWORD = f"{HYDRA_VOCAB_KEY}:possibleValue"
HYDRA_POSSIBLE_STATUS_VALUE_KEYWORD = f"{HYDRA_VOCAB_KEY}:possibleStatus"
HYDRA_EXPECTS_HEADER_KEYWORD = f"{HYDRA_VOCAB_KEY}:expectsHeader"
HYDRA_EXPECTS_KEYWORD = f"{HYDRA_VOCAB_KEY}:expects"
HYDRA_SUPPORTED_PROPERTIES_KEYWORD = f"{HYDRA_VOCAB_KEY}:supportedProperty"
HYDRA_SUPPORTED_PROPERTY_KEYWORD = f"{HYDRA_VOCAB_KEY}:SupportedProperty"
HYDRA_PROPERTY_KEYWORD = f"{HYDRA_VOCAB_KEY}:property"
HYDRA_REQUIRED_KEYWORD = f"{HYDRA_VOCAB_KEY}:required"
HYDRA_READABLE_KEYWORD = f"{HYDRA_VOCAB_KEY}:readable"
HYDRA_WRITABLE_KEYWORD = f"{HYDRA_VOCAB_KEY}:writable"

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

    def get_basic_context(self):
        context = copy.deepcopy(VOCABS_TEMPLATE)
        context[ACONTEXT_KEYWORD].update(self.get_properties_term_definition_dict())
        context.update(AbstractResource.MAP_MODEL_FOR_CONTEXT[self.entity_class].get_type_by_model_class())
        context.update(self.get_basic_supported_properties())
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