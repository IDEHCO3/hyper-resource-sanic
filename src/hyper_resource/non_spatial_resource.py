from sanic import  response
from hyper_resource.abstract_resource import AbstractResource
class NonSpatialResource(AbstractResource):
     async def get_representation(self, id_or_key_value):
        dialect_db = self.request.app.dialect_db_class(self.request.app.db, self.metadata_table(), self.entity_class())
        a_key = self.entity_class().primary_key()
        row = await dialect_db.fetch_one({a_key: id_or_key_value})
        print(row.__str__())
        return response.json(dict(row))