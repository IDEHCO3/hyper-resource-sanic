import copy
from typing import List

from src.hyper_resource.context.abstract_context import AbstractContext, ACONTEXT_KEYWORK, VOCABS_TEMPLATE, \
    PREFIX_SCHEMA_ORG
from src.orm.database import DialectDatabase
from src.url_interpreter.interpreter_types import GEOALCHEMY_TYPES_OPERATIONS
from src.hyper_resource.context.context_types import SQLALCHEMY_SCHEMA_ORG_TYPES, PYTHON_SCHEMA_ORG_TYPES
from environs import Env

env = Env()
env.read_env()
port = env.str("PORT", "8002")
host = env.str("HOST", "127.0.0.1")

PREFIX_GEOJSONLD = "geojson"
PREFIX_HYPER_RESOURCE = "hr"

SUPPORTED_OPERATIONS_KEYWORD = f"{PREFIX_HYPER_RESOURCE}:supportedOperations"
SUPPORTED_PROPERTIES_KEYWORD = f"{PREFIX_HYPER_RESOURCE}:supportedProperties"

GEOMETRY_CONTEXT_TEMPLATE = {
    f"{ACONTEXT_KEYWORK}": {
        f"{PREFIX_GEOJSONLD}": "https://purl.org/geojson/vocab#",
        "coordinates": {
            "@container": "@list",
            "@id": "geojson:coordinates"
        },
        "type": "@type"
    }
}

FEATURE_CONTEXT_TEMPLATE = {
    f"{ACONTEXT_KEYWORK}": {
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
FEATURE_CONTEXT_TEMPLATE_VOCABS[ACONTEXT_KEYWORK].update(VOCABS_TEMPLATE[ACONTEXT_KEYWORK])

class GeoContext(AbstractContext):
    def get_properties_term_definition_dict(self):
        term_definition_dict = {}
        for column in self.metadata_table.columns:
            if not hasattr(column.type, "geometry_type"):
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
    def get_basic_context(self):
        context = copy.deepcopy(FEATURE_CONTEXT_TEMPLATE_VOCABS)
        context[ACONTEXT_KEYWORK][self.get_geometry_type()] = f"{PREFIX_GEOJSONLD}:{self.get_geometry_type()}"
        context[ACONTEXT_KEYWORK].update(self.get_properties_term_definition_dict())
        context[ACONTEXT_KEYWORK].update({"FeatureCollection": f"{PREFIX_GEOJSONLD}:FeatureCollection"})
        context[ACONTEXT_KEYWORK].update( {"features": {"@container": "@set", "@id": f"{PREFIX_GEOJSONLD}:features"}} )
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
        context[ACONTEXT_KEYWORK][self.get_geometry_type()] = f"{PREFIX_GEOJSONLD}:{self.get_geometry_type()}"
        context[ACONTEXT_KEYWORK].update(self.get_properties_term_definition_dict())

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

        context[ACONTEXT_KEYWORK][self.get_geometry_type()] = f"{PREFIX_GEOJSONLD}:{self.get_geometry_type()}"
        filtered_term_def_dict = dict()
        for term, definition in self.get_properties_term_definition_dict().items():
            if term in attributes:
                filtered_term_def_dict.update({term: definition})
        context[ACONTEXT_KEYWORK].update(filtered_term_def_dict)
        return context