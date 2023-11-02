import copy

import geoalchemy2.types

from src.hyper_resource.common_resource import CONTENT_TYPE_TEXT, CONTENT_TYPE_GEOJSON
from src.hyper_resource.context.context_types import PYTHON_SCHEMA_ORG_TYPES

GEOPYTHON_SCHEMA_ORG_TYPES = copy.deepcopy(PYTHON_SCHEMA_ORG_TYPES)
PREFIX_GEOJSONLD = "geojson"
GEOJSONLD_GEOMETRY = "Geometry"
GEOJSONLD_FEATURE_COLLECTION = "FeatureCollection"
GEOJSONLD_FEATURES = "features"

GEOPYTHON_SCHEMA_ORG_TYPES.update({
    geoalchemy2.types.Geometry: f"{PREFIX_GEOJSONLD}:{GEOJSONLD_GEOMETRY}"
})

GEO_MIME_TYPES_FOR_TYPE = {
    geoalchemy2.types.Geometry: [CONTENT_TYPE_TEXT, CONTENT_TYPE_GEOJSON]
}
