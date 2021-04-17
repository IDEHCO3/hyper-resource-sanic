from typing import List, Tuple

from shapely.geometry import mapping
from shapely.geometry.base import BaseGeometry

HTTP_IF_NONE_MATCH = 'HTTP_IF_NONE_MATCH'
HTTP_IF_MATCH = 'HTTP_IF_MATCH'
HTTP_IF_UNMODIFIED_SINCE = 'HTTP_IF_UNMODIFIED_SINCE'
HTTP_IF_MODIFIED_SINCE = 'HTTP_IF_MODIFIED_SINCE'
HTTP_ACCEPT = 'HTTP_ACCEPT'
CONTENT_TYPE = 'CONTENT_TYPE'
ETAG = 'Etag'
CONTENT_TYPE_GEOJSON = "application/geo+json"
CONTENT_TYPE_JSON = "application/json"
CONTENT_TYPE_LD_JSON = "application/ld+json"
CONTENT_TYPE_OCTET_STREAM = "application/octet-stream"
CONTENT_TYPE_IMAGE_PNG = "image/png"
CONTENT_TYPE_IMAGE_TIFF = "image/tiff"

HYPER_RESOURCE_CONTEXT = 'http://www.w3.org/ns/json-hr#context'
HYPER_RESOURCE_CONTENT_TYPE = 'application/hr+json'
HYPER_RESOURCE_EXTENSION = '.jsonhr'

SUPPORTED_CONTENT_TYPES = (CONTENT_TYPE_GEOJSON, CONTENT_TYPE_JSON,CONTENT_TYPE_LD_JSON, CONTENT_TYPE_OCTET_STREAM, CONTENT_TYPE_IMAGE_PNG, CONTENT_TYPE_IMAGE_TIFF, HYPER_RESOURCE_CONTENT_TYPE)

IMAGE_RESOURCE_TYPE = "Image"

class CommomResource:
    @classmethod
    def list_attribute_column_type(cls) -> List[Tuple]:
        pass

def convert_to_json(obj : object):
    if type(obj) in (int, float, str):
        return obj
    if isinstance(obj,BaseGeometry):
        return mapping(obj)
    return obj
