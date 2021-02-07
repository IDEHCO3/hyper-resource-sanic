from settings import BASE_DIR, SOURCE_DIR
import sanic

from src.hyper_resource.context.geocontext import GeoCollectionContext
from src.hyper_resource import feature_utils
from src.hyper_resource.spatial_collection_resource import SpatialCollectionResource
from src.orm.database_postgis import DialectDbPostgis
import json, os
MIME_TYPE_JSONLD = "application/ld+json"

class FeatureCollectionResource(SpatialCollectionResource):

    def __init__(self, request):
        super().__init__(request)

    def get_geom_attribute(self):
        for column in self.entity_class().column_names():
            column_type = getattr(self.entity_class(), column).property.columns[0].type
            if hasattr(column_type, "geometry_type"):
                return column

    def rows_as_dict(self, rows):
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
            geometry = json.loads(row_dict[geom_attrubute])
            row_dict.pop(geom_attrubute, None)
            geometry.pop("crs", None)
            feature["geometry"] = geometry

            feature["properties"] = row_dict
            response_data.append(feature)
        feature_collection["features"] = response_data
        return feature_collection

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

    async def get_html_representation(self):
        html_filepath = os.path.join(SOURCE_DIR, "hyper_resource", "templates" ,"basic_geo.html")
        with open(html_filepath, "r") as body:
            html_content = body.read()
            content = self.set_html_variables(html_content)
            return sanic.response.html(content, 200)

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