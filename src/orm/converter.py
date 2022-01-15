import json
from datetime import datetime, date
from decimal import Decimal
from time import time

import aiohttp
import shapely
from aiohttp.web_exceptions import HTTPNotAcceptable
from shapely import wkb

from src.aiohttp_client import ClientIOHTTP
from src.hyper_resource.common_resource import *
from src.hyper_resource import util
from src.hyper_resource.util import a_request
from shapely.geometry import GeometryCollection, shape, Polygon, LineString, Point, MultiPolygon, MultiLineString, \
    MultiPoint
from shapely.geometry.base import BaseGeometry
from sqlalchemy import ForeignKey, String, Integer, SmallInteger, Float
from geoalchemy2 import Geometry

class ConverterType():

    _instance = None

    def __new__(cls, *args, **kwargs):
        if not cls._instance:
            cls._instance = super(ConverterType, cls).__new__(cls, *args, **kwargs)
        return cls._instance

    async def request_content(self, url: str, accept: str = CONTENT_TYPE_JSON):
        # aiohttp_session = aiohttp.ClientSession(loop=asyncio.get_event_loop())
        headers = {'accept': accept}
        async with aiohttp.ClientSession() as session:
            async with session.get(url) as resp:
                if 400 <= resp.status <= 599:
                    raise HTTPNotAcceptable()
                content_type = resp.content_type
                if content_type in [CONTENT_TYPE_JSON, CONTENT_TYPE_GEOJSON]:
                    return await resp.json()

    def value_has_url(self, value_str):
        return (value_str.find('http:') > -1) or (value_str.find('https:') > -1) or (value_str.find('www.') > -1)

    def value_seems_json(self, value_str : str) -> bool:
        return value_str.startswith('{') and value_str.endswith('}')

    def value_seems_wkt(self, value_as_str):
        wkts = ['point', 'Linestring', 'polygon', 'multipoint', 'multilinestring', 'muiltpolygon', 'geometrycollection']
        value_from_path = value_as_str[0:20].lower()
        for wkt in wkts:
            if value_from_path.startswith(wkt):
                return True
        return False

    def path_is_feature_collection(self, path):
        try:
            path_as_json = json.loads(path)
        except json.decoder.JSONDecodeError:
            return False

        if 'type' in path_as_json.keys():
            return path_as_json['type'].lower() == 'featurecollection'
        else:
            return False

    def path_is_geometry_collection(self, path):
        try:
            path_as_json = json.loads(path)
        except json.decoder.JSONDecodeError:
            return False

        if 'type' in path_as_json:
            return path_as_json['type'].lower() == 'geometrycollection'
        else:
            return False

    def path_is_feature(self, path: str) -> bool:
        try:
            path_as_json = json.loads(path)
        except json.decoder.JSONDecodeError:
            return False

        if 'type' in path_as_json:
            return path_as_json['type'].lower() == 'feature'
        else:
            return False

    '''
    def path_is_wkt(self, path):
        geos_subclasses = [geom_subcls.capitalize() for geom_subcls in GEOSGEOMETRY_SUBCLASSES]
        joined_geos_subclasses = "|".join(geos_subclasses)
        regex = r"(" + joined_geos_subclasses + ")\(.+\)$"
        return True if re.search(regex, path) is not None else False
    '''

    def make_geometrycollection_from_featurecollection(self, feature_collection):
        geoms = []
        #features = json.loads(feature_collection)
        coordinates = []
        for feature in feature_collection['features']:
            feature_geom = json.dumps(feature['geometry'])
            coordinates.append(feature_geom)

        return shape({"type": "GeometryCollection", "geometries": [{"type": "MultiPolygon", "coordinates": coordinates}]})

    """
    def make_geometrycollection_from_dict(self, geom_collection_dict):
        gc = GeometryCollection()
        for geometry in geom_collection_dict['geometries']:
            geom_coordinates = json.dumps(geometry)
            geos_geom = (GEOSGeometry(geom_coordinates))
            gc.append(geos_geom)
        return gc
        
    """

    async def get_geos_geometry_from_request(self, url: str, accept: str = CONTENT_TYPE_JSON):
        try:
            headers = {'accept': accept}
            async with ClientIOHTTP().session.get(url, headers=headers) as resp:
                if resp.content_type == CONTENT_TYPE_OCTET_STREAM:
                    return shape(await resp.read())
                elif resp.content_type == CONTENT_TYPE_WKB:
                    return wkb.loads(await resp.read())
                elif resp.content_type in [CONTENT_TYPE_JSON, CONTENT_TYPE_GEOJSON]:  # ['application/json', 'application/geojson', 'application/vnd.geo+json']:
                    js = await resp.json()
                    if (js.get("type") and js["type"].lower() == 'feature'):
                        return shape(js["geometry"])
                    elif (js.get("type") and js["type"].lower() == 'featurecollection'):
                        return self.make_geometrycollection_from_featurecollection(js)
                    else:
                        # _json = json.dumps(js)
                        return shape(js)
                return shape(await resp.text())

        except (Exception, RuntimeError, TypeError, NameError) as error:
            print(error)
            raise error



    async def convert_to_string(self, value_as_str):
        return str(value_as_str)

    async def convert_to_int(self, value_as_str):
        return int(value_as_str)

    async def convert_to_float(self, value_as_str):
        return float(value_as_str)

    async def convert_to_decimal(self, value_as_str):
        return Decimal(value_as_str)

    async def convert_to_date(self, value_as_str):
        return datetime.strptime(value_as_str, "%Y-%m-%d").date()

    async def convert_to_datetime(self, value_as_str):
        return datetime.strptime(value_as_str, "%Y-%m-%d %H:%M:%S")

    async def convert_to_time(self, value_as_str):
        return datetime.time.strptime(value_as_str, "%Y-%m-%d %H:%M:%S")

    async def convert_to_geometry(self, value_as_str):
        try:
            if self.value_seems_json(value_as_str):
                jgeo = json.loads(value_as_str)
                return shape(jgeo)
            elif self.value_seems_wkt(value_as_str):
                return shapely.wkt.loads(value_as_str)
            elif self.value_has_url(value_as_str):
                return await self.get_geos_geometry_from_request(value_as_str)
            else:
                return shapely.wkb.loads(bytes.fromhex(value_as_str))

        except (ValueError, ConnectionError) as err:
            print('Error: '.format(err))

    async def convert_in_args(self, in_arg: str, a_type: type) -> str:
        if a_type in (str, String):
            args = in_arg.split(',')
            args_str = [ f"'{arg}'" for arg in args]
            return ','.join(args_str)
        else:
            return in_arg
    async def operation_to_convert_value(self, a_type):
        d = {}
        d[str] = self.convert_to_string
        d[String] = self.convert_to_string
        d[int] = self.convert_to_int
        d[Integer] = self.convert_to_int
        d[SmallInteger] = self.convert_to_int
        d[float] = self.convert_to_float
        d[Float] = self.convert_to_float
        d[date] = self.convert_to_date
        d[datetime] = self.convert_to_datetime
        d[time] = self.convert_to_time
        d[Geometry] = self.convert_to_geometry
        d[BaseGeometry] = self.convert_to_geometry
        d[Polygon] = self.convert_to_geometry
        d[LineString] = self.convert_to_geometry
        d[Point] = self.convert_to_geometry
        d[MultiPolygon] = self.convert_to_geometry
        d[MultiLineString] = self.convert_to_geometry
        d[MultiPoint] = self.convert_to_geometry
        d[ForeignKey] = self.convert_to_int

        return d[a_type]

    async def value_converted(self, param_value, a_type: type) -> object:
        object_method = await self.operation_to_convert_value(a_type)
        return await object_method(param_value)

    async def convert_parameters(self, params: List[object], param_types: List[type] ) -> List:
        #[param_type_arr[idx][1](param_value) for idx, param_value in enumerate(params)]
        print(param_types)
        return [ await self.value_converted(param, param_types[idx]) for idx, param in enumerate(params) ]

