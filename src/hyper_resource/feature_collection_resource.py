from sanic import response

from src.hyper_resource.abstract_collection_resource import AbstractCollectionResource
from src.orm.database_postgis import DialectDbPostgis


class FeatureCollectionResource(AbstractCollectionResource):
    async def get_representation(self):
        rows = await self.dialect_DB().fetch_all()
        res = self.rows_as_dict(rows)
        return response.json(res)

    def dialect_DB(self):
          return DialectDbPostgis(self.request.app.db, self.metadata_table(), self.entity_class())