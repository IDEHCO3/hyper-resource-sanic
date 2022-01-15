import time

from settings import BASE_DIR, SOURCE_DIR
import sanic

from src.hyper_resource.context.geocontext import GeoCollectionContext
from src.hyper_resource import feature_utils
from src.hyper_resource.spatial_collection_resource import SpatialCollectionResource
from src.orm.database_postgis import DialectDbPostgis
import json, os

from src.url_interpreter.interpreter import Interpreter

MIME_TYPE_JSONLD = "application/ld+json"
from geoalchemy2.shape import to_shape
class FeatureCollectionResource(SpatialCollectionResource):

    def __init__(self, request):
        super().__init__(request)

    def get_geom_attribute(self):
        for column in self.entity_class().column_names():
            column_type = getattr(self.entity_class(), column).property.columns[0].type
            if hasattr(column_type, "geometry_type"):
                return column

    async def rows_as_dict(self, rows):
        response_data = []
        geom_attrubute = self.get_geom_attribute()
        feature_collection = {
            "type": "FeatureCollection",
            # 'crs': {
            #     'type': 'name',
            #     'properties': {
            #         'name': 'EPSG:4326' # todo: crs hardcoded
            #     }
            # }
        }

        for row in rows:
            row_dict = dict(row)
            feature = {"type": "Feature"}
            geometry = to_shape(row_dict[geom_attrubute]).__geo_interface__ #json.loads(row_dict[geom_attrubute])
            row_dict.pop(geom_attrubute, None)
            #geometry.pop("crs", None)
            feature["geometry"] = geometry

            feature["properties"] = row_dict
            response_data.append(feature)
        feature_collection["features"] = response_data
        return feature_collection

    async def get_json_representation(self):

        start = time.time()
        print(f"time: {start} start rows in python")

        rows = await self.dialect_DB().fetch_all()
        rows_from_db = await self.rows_as_dict(rows)
        res = sanic.response.json(rows_from_db or [])
        #rows = await self.dialect_DB().fetch_all_as_json(prefix_col_val=self.protocol_host())
        #res = sanic.response.text(rows or [], content_type='application/json')
        end = time.time()
        print(f"time: {end - start} end rows in python")
        return res

    async def get_html_representation(self):
        html_filepath = os.path.join(SOURCE_DIR, "hyper_resource", "templates" ,"basic_geo.html")
        with open(html_filepath, "r") as body:
            html_content = body.read()
            content = self.set_html_variables(html_content)
            return sanic.response.html(content, 200)

    async def get_geobuf_representation(self):
        start = time.time()
        print(f"time: {start} start rows in python")
        rows = await self.dialect_DB().fetch_all_as_geobuf(prefix_col_val=self.protocol_host())
        res = sanic.response.raw(rows or [], content_type='application/octet-stream')
        end = time.time()
        print(f"time: {end - start} end rows in python")
        return res


    async def get_representation(self):
        accept = self.request.headers['accept']
        if 'text/html' in accept:
            return await self.get_html_representation()
        elif 'application/octet-stream' in accept:
            return await self.get_geobuf_representation()
        else:
            return await self.get_json_representation()

    async def get_mvt_representation_given_path(self, path):
        #application/vnd.mapbox-vector-tile
        params = path.split('&')
        rows = await self.dialect_DB().fetch_as_mvt_tiles(params)
        res = sanic.response.raw(rows or [], content_type='application/vnd.mapbox-vector-tile')
        return res

    async def get_representation_given_path(self, path):
        accept = self.request.headers['accept']
        if 'application/vnd.mapbox-vector-tile' in accept:
            return await self.get_mvt_representation_given_path(path)
        return await super().get_representation_given_path(path)

    def dialect_DB(self):
          return DialectDbPostgis(self.request.app.db, self.metadata_table(), self.entity_class())

    async def projection(self, enum_attribute_name: str):
        attr_names = tuple(a.strip() for a in enum_attribute_name.split(','))
        if self.get_geom_attribute() in attr_names and ('text/html' in self.request.headers['accept']):
            return await self.get_representation()
        rows = await self.dialect_DB().fetch_all_as_json(attr_names)
        return sanic.response.text(rows, content_type='application/json')

    async def options(self, *args, **kwargs):
        context = self.context_class(self.dialect_DB(), self.metadata_table(), self.entity_class())
        return sanic.response.json(context.get_basic_context(), content_type=MIME_TYPE_JSONLD)

    async def filter(self, path: str):  # -> "AbstractCollectionResource":
        """
        params: path
        return: self
        description: Filter a collection given an expression
        example: http://server/api/drivers/filter/license/eq/valid
        """
        if self.is_content_type_in_accept('text/html'):
            return await self.get_html_representation()
        return await super(FeatureCollectionResource, self).filter(path)