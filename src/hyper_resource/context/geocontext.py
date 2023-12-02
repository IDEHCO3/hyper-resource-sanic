import copy
import typing
from typing import List

from src.hyper_resource.common_resource import HTTP_GET_METHOD, CONTENT_TYPE_HEADER, CONTENT_TYPE_GEOJSON, \
    CONTENT_TYPE_IMAGE_PNG, STATUS_OK, CONTENT_TYPE_TEXT
from src.hyper_resource.context.abstract_context import AbstractContext, ACONTEXT_KEYWORD, VOCABS_TEMPLATE, \
    ATYPE_KEYWORD, OPERATION_KEYWORD, HYDRA_METHOD_KEYWORD, APPEND_PATH_KEYWORD, \
    HYDRA_POSSIBLE_VALUE_KEYWORD, HYDRA_HEADER_NAME_KEYWORD, HYDRA_RETURNS_HEADER_KEYWORD, \
    HYDRA_POSSIBLE_STATUS_VALUE_KEYWORD, HYDRA_EXPECTS_HEADER_KEYWORD, OPERATION_PARAMETER_KEYWORD, \
    HYDRA_EXPECTS_KEYWORD, EXPECTS_KEYWORD_SERIALIZATION, AID_KEYWORD, \
    PARAMETERS_KEYWORD, VARIABLE_PATH_KEYWORD, REQUIRED_PARAMETER_PATH_KEYWORD, \
    HYDRA_PROPERTY_KEYWORD, HYDRA_SUPPORTED_PROPERTY_KEYWORD, HYDRA_REQUIRED_KEYWORD, HYDRA_READABLE_KEYWORD, \
    HYDRA_WRITABLE_KEYWORD, IS_EXTERNAL_KEYWORD
from src.hyper_resource.context.geocontext_types import PREFIX_GEOJSONLD, GEOJSONLD_GEOMETRY, \
    GEOJSONLD_FEATURE_COLLECTION, GEOJSONLD_FEATURES, GEOPYTHON_SCHEMA_ORG_TYPES, GEO_MIME_TYPES_FOR_TYPE
from src.url_interpreter.interpreter_types import GEOALCHEMY_TYPES_OPERATIONS, GEOALCHEMY_COLLECTION_TYPES_OPERATIONS
from src.hyper_resource.context.context_types import SQLALCHEMY_SCHEMA_ORG_TYPES, PYTHON_SCHEMA_ORG_TYPES, \
    ACONTAINER_KEYWORD, ASET_KEYWORD, SUPPORTED_PROPERTY_KEYWORD
from environs import Env

env = Env()
env.read_env()
port = env.str("PORT", "8002")
host = env.str("HOST", "127.0.0.1")

PREFIX_HYPER_RESOURCE = "hr"

SUPPORTED_OPERATIONS_KEYWORD = f"{PREFIX_HYPER_RESOURCE}:supportedOperations"
SUPPORTED_PROPERTIES_KEYWORD = f"{PREFIX_HYPER_RESOURCE}:supportedProperties"

GEOMETRY_CONTEXT_TEMPLATE = {
    f"{ACONTEXT_KEYWORD}": {
        f"{PREFIX_GEOJSONLD}": "https://purl.org/geojson/vocab#",
        "coordinates": {
            "@container": "@list",
            "@id": "geojson:coordinates"
        },
        "type": "@type"
    }
}

FEATURE_CONTEXT_TEMPLATE = {
    f"{ACONTEXT_KEYWORD}": {
        # f"{PREFIX_HYPER_RESOURCE}": f"http://{host}:{port}/core",
        # "schema": "http://schema.org/",
        f"{PREFIX_GEOJSONLD}": "https://purl.org/geojson/vocab#",

        "Feature": "geojson:Feature",
        # "FeatureCollection": "geojson:FeatureCollection",
        # "MultiPolygon": "geojson:MultiPolygon",

        "coordinates": {
            "@container": "@list",
            "@id": "geojson:coordinates"
        },
        # "features": {
        #     "@container": "@set",
        #     "@id": "geojson:features"
        # },
        "type": "@type",
        "id": "@id",
        "geometry": "geojson:geometry",
        "properties": "geojson:properties"
    }
}
FEATURE_CONTEXT_TEMPLATE_VOCABS = copy.deepcopy(FEATURE_CONTEXT_TEMPLATE)
FEATURE_CONTEXT_TEMPLATE_VOCABS[ACONTEXT_KEYWORD].update(VOCABS_TEMPLATE[ACONTEXT_KEYWORD])
FEATURE_COLLECTION_KEYWORD = "FeatureCollection"

class GeoContext(AbstractContext):
    def get_properties_term_definition_dict(self):
        term_definition_dict = {}
        for column in self.metadata_table.columns:
            if not hasattr(column.type, "geometry_type") and not column.primary_key:
                term_definition_dict[str(column.name)] = SQLALCHEMY_SCHEMA_ORG_TYPES[type(column.type)]
        return term_definition_dict

    def get_geometry_type(self) -> str:
        # for column in self.metadata_table.columns:
        #     if hasattr(column.type, "geometry_type"):
        #         return column.type.geometry_type.capitalize()
        return self.get_geometry_attribute().type.geometry_type.capitalize()

    def get_geometry_attribute(self):
        for column in self.metadata_table.columns:
            if hasattr(column.type, "geometry_type"):
                return column

class GeoCollectionContext(GeoContext):

    def get_operation_append_path(self, func) -> str:
        params_list = "/".join(["{" + f"param{val}" + "}" for val in range(0, len(func.__annotations__.items()) - 1)])
        if params_list != "":
            params_list = "/" + params_list

        append_path = f"/{func.__name__}" + params_list
        return append_path

    def get_operation_parameters(self, operation):
        return [val for val in operation.__annotations__.items()][:-1]

    def get_operation_returns(self, operation):
        return [val for val in operation.__annotations__.items()][-1]

    def get_default_geometry_returns_header(self):
        returns_header = []
        possibleValue = [CONTENT_TYPE_GEOJSON, CONTENT_TYPE_IMAGE_PNG]
        returns_header.append({HYDRA_HEADER_NAME_KEYWORD: CONTENT_TYPE_HEADER, HYDRA_POSSIBLE_VALUE_KEYWORD: possibleValue})
        return returns_header
        # operation_dict.update({HYDRA_RETURNS_HEADER_KEYWORD: returns_header})

    def get_default_geometry_expects_header(self):
        expects_header = []
        possibleValue = [CONTENT_TYPE_GEOJSON, CONTENT_TYPE_IMAGE_PNG]
        expects_header.append({HYDRA_HEADER_NAME_KEYWORD: CONTENT_TYPE_HEADER, HYDRA_POSSIBLE_VALUE_KEYWORD: possibleValue})
        return expects_header
        # operation_dict.update({HYDRA_EXPECTS_HEADER_KEYWORD: expects_header})

    def get_default_geometry_possible_status(self):
        return [STATUS_OK]
        # operation_dict.update(possible_status)

    def get_basic_supported_properties(self) -> dict:
        supported_properties = []
        for column in self.metadata_table.columns:
             # WARNING: must check if the property is a dereferencable
            is_fk = column.name in self.db_dialect.foreign_keys_names()
            property_dict = {
                ATYPE_KEYWORD: SUPPORTED_PROPERTY_KEYWORD,
                HYDRA_PROPERTY_KEYWORD: column.name,
                HYDRA_REQUIRED_KEYWORD: not column.nullable,
                HYDRA_READABLE_KEYWORD: True,
                HYDRA_WRITABLE_KEYWORD: not column.primary_key,
                IS_EXTERNAL_KEYWORD: is_fk
            }
            supported_properties.append(property_dict)
        d = {SUPPORTED_PROPERTIES_KEYWORD: supported_properties}
        return d

    def get_expects_for_parameter_type(self, parameter_type):
        return GEOPYTHON_SCHEMA_ORG_TYPES[parameter_type]

    def get_expected_serialization_for_parameter_type(self, parameter_type):
        return GEO_MIME_TYPES_FOR_TYPE[parameter_type]

    def get_basic_supported_operations(self) -> dict:
        supported_operations = []
        for _type, operations in GEOALCHEMY_COLLECTION_TYPES_OPERATIONS.items():
            for op in operations:

                append_path = self.get_operation_append_path(op)
                operation_dict = {
                    ATYPE_KEYWORD: OPERATION_KEYWORD,
                    HYDRA_METHOD_KEYWORD: HTTP_GET_METHOD,
                    APPEND_PATH_KEYWORD: append_path,
                    PARAMETERS_KEYWORD: []
                }

                operation_dict.update({HYDRA_RETURNS_HEADER_KEYWORD: self.get_default_geometry_returns_header()})
                operation_dict.update({HYDRA_EXPECTS_HEADER_KEYWORD: self.get_default_geometry_expects_header()})
                operation_dict.update({HYDRA_POSSIBLE_STATUS_VALUE_KEYWORD: self.get_default_geometry_possible_status()})

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
        d =  {SUPPORTED_OPERATIONS_KEYWORD: supported_operations}
        return d

    def get_basic_context(self):
        context = copy.deepcopy(FEATURE_CONTEXT_TEMPLATE_VOCABS)
        context[ACONTEXT_KEYWORD][self.get_geometry_type()] = f"{PREFIX_GEOJSONLD}:{self.get_geometry_type()}"
        context[ACONTEXT_KEYWORD].update(self.get_properties_term_definition_dict())
        context[ACONTEXT_KEYWORD].update({
                                             GEOJSONLD_FEATURE_COLLECTION: f"{PREFIX_GEOJSONLD}:{GEOJSONLD_FEATURE_COLLECTION}"})
        context[ACONTEXT_KEYWORD].update({GEOJSONLD_FEATURES: {ACONTAINER_KEYWORD: ASET_KEYWORD, AID_KEYWORD: f"{PREFIX_GEOJSONLD}:{GEOJSONLD_FEATURES}"}})
        context.update(self.get_basic_supported_operations())
        context.update(self.get_basic_supported_properties())
        context.update({ATYPE_KEYWORD: FEATURE_COLLECTION_KEYWORD})
        return context

class GeoDetailContext(GeoContext):

    def get_operation_append_path(self, func) -> str:
        params_list = "/".join(["{" + f"param{val}" + "}" for val in range(0, len(func.__annotations__.items()) - 1)])
        if params_list != "":
            params_list = "/" + params_list

        append_path = f"/{func.__name__}" + params_list
        return append_path

    def get_basic_supported_operations(self) -> dict:
        supported_operations = []
        for _type, operations in GEOALCHEMY_TYPES_OPERATIONS.items():
            for op in operations:

                append_path = self.get_operation_append_path(op)
                operation_dict = {
                    "@type": "hr:Operation",
                    "hydra:method": "GET",
                    "hr:appendPath": append_path,
                    "hr:parameters": []
                }

                for operation_meta in op.__annotations__.items():

                    if not operation_meta[0] == "return":
                        operation_dict["hr:parameters"].append({
                            "@type": ["hr:OperationParameter", PYTHON_SCHEMA_ORG_TYPES[operation_meta[1]]]
                        })
                supported_operations.append(operation_dict)
        d =  {SUPPORTED_OPERATIONS_KEYWORD: supported_operations}
        return d

    def get_basic_supported_properties(self) -> dict:
        supported_properties = []
        for column in self.metadata_table.columns:
             # WARNING: must check if the property is a dereferencable
            is_fk = column.name in self.db_dialect.foreign_keys_names()
            property_dict = {
                "@type": "hr:SupportedProperty",
                "hr:property": column.name,
                "hr:required": not column.nullable,
                "hr:readable": True,
                "hr:writable": True,
                "hr:external": is_fk
            }
            supported_properties.append(property_dict)
        d = {SUPPORTED_PROPERTIES_KEYWORD: supported_properties}
        return d

    def get_basic_context(self):
        context = copy.deepcopy(FEATURE_CONTEXT_TEMPLATE_VOCABS)
        context[ACONTEXT_KEYWORD][self.get_geometry_type()] = f"{PREFIX_GEOJSONLD}:{self.get_geometry_type()}"
        context[ACONTEXT_KEYWORD].update(self.get_properties_term_definition_dict())

        context.update(self.get_basic_supported_operations())
        context.update(self.get_basic_supported_properties())
        return context

    # todo: check geometric attribute existence. If not exists call super
    def get_projection_context(self, attributes:List[str]):
        geometry_attribute = self.get_geometry_attribute().name
        if geometry_attribute not in attributes:
            return super().get_projection_context(attributes)

        if len(attributes) == 1 and attributes[0] == geometry_attribute:
            context = copy.deepcopy(GEOMETRY_CONTEXT_TEMPLATE)
        else:
            context = copy.deepcopy(FEATURE_CONTEXT_TEMPLATE)

        context[ACONTEXT_KEYWORD][self.get_geometry_type()] = f"{PREFIX_GEOJSONLD}:{self.get_geometry_type()}"
        filtered_term_def_dict = dict()
        for term, definition in self.get_properties_term_definition_dict().items():
            if term in attributes:
                filtered_term_def_dict.update({term: definition})
        context[ACONTEXT_KEYWORD].update(filtered_term_def_dict)
        return context