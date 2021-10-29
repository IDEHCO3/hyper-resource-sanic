import json
from typing import List

from shapely.geometry import shape, GeometryCollection
from shapely.geometry.base import BaseGeometry


def set_html_variables(html_content: str, title:str, jsonld: str) -> str:
    TITLE_VARIABLE = "{{title}}"
    JSONLD_VARIABLE = "{{jsonld}}"
    content = html_content.replace(TITLE_VARIABLE, title)

    content = content.replace( JSONLD_VARIABLE, jsonld )
    return content

def geojson_to_geometry_collection(geoJson) -> GeometryCollection:
    features = geoJson["features"]
    return GeometryCollection([shape(feature["geometry"]).buffer(0) for feature in features])

def geojson_to_geometries(geoJson) -> List[BaseGeometry]:
    features = geoJson["features"]
    return [shape(feature["geometry"]).buffer(0) for feature in features]
