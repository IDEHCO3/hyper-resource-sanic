from sanic import  response
from src.hyper_resource.abstract_resource import AbstractResource
nonspatial_function_names = []
class NonSpatialResource(AbstractResource):
    async def get_representation(self, id_or_key_value):
        if type(id_or_key_value) == dict:
            row = await self.dialect_DB().fetch_one(id_or_key_value)
        else:
            row = await self.dialect_DB().fetch_one({self.entity_class().primary_key(): id_or_key_value})
        print(row.__str__())
        return response.json(dict(row))
    async def get_representation_given_path(self, id_or_key_value, a_path):
           if a_path[-1] == '/':  # Removes trail slash
                a_path = a_path[:-1]
           operation_name_or_atribute_comma = a_path.split('/')[0].strip().lower()
           if operation_name_or_atribute_comma in nonspatial_function_names:
              method_execute_name = "pre_" + operation_name_or_atribute_comma
              return await getattr(self, method_execute_name)(*[a_path])
           else:
              att_names = operation_name_or_atribute_comma.split(',')
              if self.fields_from_path_in_attribute_names(att_names):
                 all_column = self.entity_class().enum_column_names_as_given_attributes(att_names)
                 if type(id_or_key_value) == dict:
                     row = await self.dialect_DB().fetch_one(id_or_key_value, all_column)
                 else:
                     row = await self.dialect_DB().fetch_one({self.entity_class().primary_key(): id_or_key_value}, all_column)
                 print(row)
                 if len(att_names) == 1:
                     val = row[self.entity_class().column_name(att_names[0])]
                     return response.json(val)
                 return response.json(dict(row))
              else:
                 msg = f"Some of these attributes {att_names} does not exists in this resource"
                 return response.json(msg, status=400)

    async def delete(self, id):
        return await self.dialect_DB().delete_one(id)