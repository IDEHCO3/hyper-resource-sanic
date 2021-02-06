import sanic
from sanic import response

from src.hyper_resource.abstract_resource import AbstractResource, MIME_TYPE_JSONLD
from src.hyper_resource.context.abstract_context import AbstractDetailContext

nonspatial_function_names = []
class NonSpatialResource(AbstractResource):
    def __init__(self, request):
        super().__init__(request)
        self.context_class = AbstractDetailContext

    async def get_html_representation(self, id_or_key_value):
        row = await self.dialect_DB().fetch_one_as_json(id_or_key_value)
        if row is None:
            return sanic.response.json("The resource was not found.", status=404)
        return sanic.response.text(row, content_type='application/json')

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
                     return sanic.response.json(val)
                 return sanic.response.json(dict(row))
              else:
                 msg = f"Some of these attributes {att_names} does not exists in this resource"
                 return sanic.response.json(msg, status=400)

    async def delete(self, an_id: int):
        try:
            await self.dialect_DB().delete_one(an_id)
        except (Exception, SyntaxError, NameError) as err:
            print(err)
            return sanic.response.json({"Error": f"{err}"}, status=400)
        return sanic.response.json(an_id, status=200)

    async def put(self, an_id: int):
        return await self.patch(an_id)

    async def patch(self, an_id: int):
        data = self.request.json
        print(f"Dados enviados para atualizar: {data}")
        try:
            self.validate_data(data)
            await self.dialect_DB().update_one(an_id, data)
        except (Exception, SyntaxError, NameError) as err:
            print(err)
            return sanic.response.json({"Error": f"{err}"}, status=400)

        return sanic.response.json(an_id, status=200)

    async def options(self, *args, **kwargs):
        context = self.context_class(self.dialect_DB(), self.metadata_table(), self.entity_class())
        return response.json(context.get_basic_context(), content_type=MIME_TYPE_JSONLD)
