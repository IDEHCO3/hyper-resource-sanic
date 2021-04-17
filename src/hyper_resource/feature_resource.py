import json
import os

from sanic import response

from settings import SOURCE_DIR
from src.hyper_resource import feature_utils
from src.hyper_resource.common_resource import *
from src.hyper_resource.context.geocontext import GeoDetailContext
from src.hyper_resource.spatial_resource import SpatialResource
import sanic

from src.orm.database_postgis import DialectDbPostgis
MIME_TYPE_JSONLD = "application/ld+json"

class FeatureResource(SpatialResource):
    def __init__(self, request):
        super().__init__(request)

    def dialect_DB(self):
          return DialectDbPostgis(self.request.app.db, self.metadata_table(), self.entity_class())

    def serialize_as_geojson(self, raw_data) -> dict:
        geometry = raw_data[self.dialect_DB().get_geom_column()]
        del raw_data[self.dialect_DB().get_geom_column()]
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

    def set_html_variables(self, html_content:str)-> str:
        return feature_utils.set_html_variables(
            html_content, self.metadata_table().name,
            json.dumps(
                self.context_class(
                    self.dialect_DB(),
                    self.metadata_table(),
                    self.entity_class()
                ).get_basic_context(),
                indent=2
            )
        )

    async def get_html_representation(self, id_or_key_value):
        html_filepath = os.path.join(SOURCE_DIR, "hyper_resource", "templates", "basic_geo.html")
        with open(html_filepath, "r") as body:
            html_content = body.read()
            content = self.set_html_variables(html_content)
            return sanic.response.html(content, 200)

    async def get_json_representation(self, id_or_key_value):
        model = await self.dialect_DB().fetch_one_model(id_or_key_value)
        if model is None:
            return sanic.response.json("The resource was not found.", status=404)
        j_d = model.json_dict(model.__class__.attribute_names())
        return sanic.response.json(j_d)

    async def get_representation(self, id):
        try:
            accept = self.request.headers['accept']
            if 'text/html' in accept:
                return await self.get_html_representation(id)
            elif 'application/vnd.ogc.wkb' in accept:
                return await self.get_wkb_representation(id)
            else:
                return await self.get_json_representation(id)
        except (Exception, SyntaxError, NameError) as err:
            print(err)
            return sanic.response.json({"Error": f"{err}"})

    async def get_representation_given_path(self, id_or_key_value, a_path:str):
        try:
            accept = self.request.headers['accept']
            if 'text/html' in accept:
                return await self.get_html_representation_given_path(id_or_key_value, a_path)
            elif 'application/octet-stream' in accept:
                return await self.get_geobuf_representation_given_path(id_or_key_value, a_path)
            elif 'application/json' in accept:
                return await self.get_json_representation_given_path(id_or_key_value, a_path)
            elif 'application/vnd.ogc.wkb' in accept:
                return await self.get_wkb_representation(id_or_key_value)

            return await self.get_json_representation_given_path(id_or_key_value, a_path)
        except (Exception, SyntaxError, NameError) as err:
            print(err)
            return sanic.response.json({"Error": f"{err}"})

    async def get_html_representation_given_path(self, id_or_key_value, a_path):
        html_filepath = os.path.join(SOURCE_DIR, "hyper_resource", "templates", "basic_geo.html")
        with open(html_filepath, "r") as body:
            html_content = body.read()
            content = self.set_html_variables(html_content)
            return sanic.response.html(content, 200)

    async def get_json_representation_given_path(self, id_or_key_value, a_path):

        try:
            action = self.entity_class().validate_path(a_path)
            if self.entity_class().is_only_attribute_list_from_path(a_path):
                model = await self.dialect_DB().fetch_one_model(id_or_key_value)
                attributes_from_path = [ att.strip() for att in a_path.split('/')[0].split(',')]
                dic = model.json_dict(attributes_from_path)
                res = dic if len(dic) > 1 else dic.popitem()[1]
                return sanic.response.json(res)
            elif self.entity_class().starts_by_one_attribute_with_functions(a_path):
                model = await self.dialect_DB().fetch_one_model(id_or_key_value)
                result = await model.execute_attribute_given(a_path)
                if isinstance(result, bytes):
                    return sanic.response.raw(result, content_type='application/vnd.ogc.wkb')
                res = convert_to_json(result)
                return sanic.response.json(res)
            else:
                model = await self.dialect_DB().fetch_one_model(id_or_key_value)
                res = await model.execute_function_given(a_path)
                return sanic.response.json(res)

        except (Exception, SyntaxError, NameError) as err:
            print(err)
            return sanic.response.json({"Error": f"{err}"})

    async def get_wkb_representation(self, id_or_key_value):

        try:
            model = await self.dialect_DB().fetch_one_model(id_or_key_value)
            result = model.get_geom()
            return sanic.response.raw(result, content_type='application/vnd.ogc.wkb')
        except (Exception, SyntaxError, NameError) as err:
            print(err)
            return sanic.response.json({"Error": f"{err}"}, status=400)

    async def options(self, *args, **kwargs):
        context = self.context_class(self.dialect_DB(), self.metadata_table(), self.entity_class())
        return response.json(context.get_basic_context(), content_type=MIME_TYPE_JSONLD)