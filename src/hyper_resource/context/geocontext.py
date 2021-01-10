import copy

from src.orm.database import DialectDatabase
from src.url_interpreter.interpretertypes import SQLALCHEMY_SCHEMA_ORG_TYPES


PREFIX_GEOJSONLD = "geojson"
ACONTEXT_KEYWORK = "@context"
GEOCONTEXT_TEMPLATE = {
    "@context": {
        "schema": "http://schema.org/",
        "geojson": "https://purl.org/geojson/vocab#",

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

    def get_basic_context(self):
        context = copy.deepcopy(GEOCONTEXT_TEMPLATE)
        context[ACONTEXT_KEYWORK][self.get_geometry_type()] = f"{PREFIX_GEOJSONLD}:{self.get_geometry_type()}"
        context[ACONTEXT_KEYWORK].update(self.get_properties_term_definition_dict())
        return context