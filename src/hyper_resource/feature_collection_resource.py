from sanic import response

from settings import BASE_DIR, SOURCE_DIR
from src.hyper_resource.abstract_collection_resource import AbstractCollectionResource
from src.orm.database_postgis import DialectDbPostgis
import json, os


class FeatureCollectionResource(AbstractCollectionResource):

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

    async def get_representation(self):
        html_filepath = os.path.join(SOURCE_DIR, "static", self.metadata_table().name + ".html")
        with open(html_filepath, "r") as body:
            return response.html(body.read(), 200)

    async def get_json_representation(self):
        rows = await self.dialect_DB().fetch_all()
        res = self.rows_as_dict(rows)
        return response.json(res)

    def dialect_DB(self):
          return DialectDbPostgis(self.request.app.db, self.metadata_table(), self.entity_class())