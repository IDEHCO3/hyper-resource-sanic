import copy
from src.orm.database import DialectDatabase
from src.url_interpreter.interpretertypes import SQLALCHEMY_SCHEMA_ORG_TYPES, GEOALCHEMY_TYPES_OPERATIONS, \
    PYTHON_SCHEMA_ORG_TYPES
from environs import Env

env = Env()
env.read_env()
port = env.str("PORT", "8002")
host = env.str("HOST", "127.0.0.1")

PREFIX_GEOJSONLD = "geojson"
PREFIX_HYPER_RESOURCE = "hr"
ACONTEXT_KEYWORK = "@context"
SUPPORTED_OPERATIONS_KEYWORD = f"{PREFIX_HYPER_RESOURCE}:supportedOperations"

GEOCONTEXT_TEMPLATE = {
    "@context": {
        f"{PREFIX_HYPER_RESOURCE}": f"http://{host}:{port}/core",
        "schema": "http://schema.org/",
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
        "geometry": "geojson:geometry",
        "properties": "geojson:properties"
    }
}

class GeoContext(object):
    def __init__(self, db_dialect:DialectDatabase, metadata_table, entity_class):
        self.db_dialect = db_dialect
        self.metadata_table = metadata_table
        self.entity_class = entity_class

    def get_basic_context(self):
        raise NotImplementedError("'get_basic_context' must be implemented in subclasses")

    def get_properties_term_definition_dict(self):
        term_definition_dict = {}
        for column in self.metadata_table.columns:
            if not hasattr(column.type, "geometry_type"):
                term_definition_dict[str(column.name)] = SQLALCHEMY_SCHEMA_ORG_TYPES[type(column.type)]
        return term_definition_dict

    def get_geometry_type(self) -> str:
        for column in self.metadata_table.columns:
            if hasattr(column.type, "geometry_type"):
                return column.type.geometry_type.capitalize()


class GeoCollectionContext(GeoContext):
    def get_basic_context(self):
        context = copy.deepcopy(GEOCONTEXT_TEMPLATE)
        context[ACONTEXT_KEYWORK][self.get_geometry_type()] = f"{PREFIX_GEOJSONLD}:{self.get_geometry_type()}"
        context[ACONTEXT_KEYWORK].update(self.get_properties_term_definition_dict())
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

    def get_basic_context(self):
        context = copy.deepcopy(GEOCONTEXT_TEMPLATE)
        context[ACONTEXT_KEYWORK][self.get_geometry_type()] = f"{PREFIX_GEOJSONLD}:{self.get_geometry_type()}"
        context[ACONTEXT_KEYWORK].update(self.get_properties_term_definition_dict())

        context.update(self.get_basic_supported_operations())
        return context