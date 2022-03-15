from typing import List, Tuple, Dict

from shapely.geometry import mapping
from shapely.geometry.base import BaseGeometry
from xml.dom.minidom import parseString
from dicttoxml import dicttoxml

HTTP_IF_NONE_MATCH = 'HTTP_IF_NONE_MATCH'
HTTP_IF_MATCH = 'HTTP_IF_MATCH'
HTTP_IF_UNMODIFIED_SINCE = 'HTTP_IF_UNMODIFIED_SINCE'
HTTP_IF_MODIFIED_SINCE = 'HTTP_IF_MODIFIED_SINCE'
HTTP_ACCEPT = 'HTTP_ACCEPT'
CONTENT_TYPE = 'CONTENT_TYPE'
ETAG = 'Etag'
CONTENT_TYPE_HTML = 'text/html'
CONTENT_TYPE_GEOJSON = "application/geo+json"
CONTENT_TYPE_JSON = "application/json"
CONTENT_TYPE_LD_JSON = "application/ld+json"
CONTENT_TYPE_OCTET_STREAM = "application/octet-stream"
CONTENT_TYPE_IMAGE_PNG = "image/png"
CONTENT_TYPE_IMAGE_TIFF = "image/tiff"
CONTENT_TYPE_WKT = 'application/x-wkt'
CONTENT_TYPE_GEOBUF = 'application/x-geobuf'
CONTENT_TYPE_WKB = 'application/x-wkb'
CONTENT_TYPE_EWKB ='application/x-ewkb'
CONTENT_TYPE_VECTOR_TILE = 'application/vnd.mapbox-vector-tile'
CONTENT_TYPE_XML = 'application/xml'
#Default mimetype for WFS 2.0 responses should be "application/gml+xml; version=3.2"
CONTENT_TYPE_GML = 'application/gml+xml; version=3.2'
CONTENT_TYPE_FLATBUFFERS = 'application/x-flatbuffers' #application/x-flatbuffers;schema = x.y.z
CONTENT_TYPE_FLATGEOBUFFERS = 'application/x-flatgeobuffers' #application/x-flatbuffers;schema = x.y.z

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


def list_type_name_wkt()->List[str]:
    return ['geometry', 'point', 'linestring', 'polygon', 'multipoint', 'multilinestring', 'multipolygon', 'geometrycollection', 'circularstring', 'compoundcurve', 'curvepolygon', 'multicurve', 'multisurface', 'curve', 'surface', 'polyhedralsurface', 'tin', 'triangle', 'circle']


def dict_to_xml(dict_or_list_dict) -> str:
    xml = dicttoxml(dict_or_list_dict, attr_type=False)
    return parseString(xml).toprettyxml()


def normalize_path_as_list( path: str, splitter: str) -> List[str]:
        paths: List[str] = path.split(splitter)
        return paths if paths[-1] != '' else paths[:-1]