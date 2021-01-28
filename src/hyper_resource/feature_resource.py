import os
from settings import SOURCE_DIR
from src.hyper_resource.context.geocontext import GeoDetailContext
from src.hyper_resource.spatial_resource import SpatialResource
import sanic

from src.orm.database_postgis import DialectDbPostgis
MIME_TYPE_JSONLD = "application/ld+json"

class FeatureResource(SpatialResource):
    def __init__(self, request):
        super().__init__(request)
        self.context_class = GeoDetailContext

    def dialect_DB(self):
          return DialectDbPostgis(self.request.app.db, self.metadata_table(), self.entity_class())

    def serialize_as_geojson(self, raw_data) -> dict:
        geometry = raw_data[self.dialect_DB().get_geom_attribute()]
        del raw_data[self.dialect_DB().get_geom_attribute()]
        serialized = {
            "type": "Feature",
            "geometry": geometry,
            "properties": raw_data
        }
        return serialized

    async def get_representation_old(self, id_or_key_value):
        data = await self.dialect_DB().fetch_one_as_json(id_or_key_value)
        serialized = self.serialize_as_geojson(data)
        return sanic.response.json(serialized)
    """"
    async def get_html_representation(self, id_or_key_value):
        row = await self.dialect_DB().fetch_one_as_json(id_or_key_value)
        if row is None:
            return sanic.response.json("The resource was not found.", status=404)
        return sanic.response.text(row, content_type='application/json')
    """
    async def get_html_representation(self, id_or_key_value):
        html_filepath = os.path.join(SOURCE_DIR, "static", "basic_geo.html")
        with open(html_filepath, "r") as body:
            return sanic.response.html(body.read(), 200)

    async def get_json_representation(self, id_or_key_value):
        row = await self.dialect_DB().fetch_one_as_json(id_or_key_value)
        if row is None:
            return sanic.response.json("The resource was not found.", status=404)
        return sanic.response.text(row, content_type='application/json')

    async def get_representation(self, id_or_key_value):
        try:
            accept = self.request.headers['accept']
            if 'text/html' in accept:
                return await self.get_html_representation(id_or_key_value)
            else:
                return await self.get_json_representation(id_or_key_value)
        except (Exception, SyntaxError, NameError) as err:
            print(err)
            return sanic.response.json({"Error": f"{err}"})


    async def options(self, *args, **kwargs):
        context = self.context_class(self.dialect_DB(), self.metadata_table(), self.entity_class())
        return response.json(context.get_basic_context(), content_type=MIME_TYPE_JSONLD)