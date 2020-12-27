from sanic import  response
from typing import Dict

from src.hyper_resource.abstract_resource import AbstractResource
from ..url_interpreter.interpreter import Interpreter
collection_function_names = [
  "filter",
  "projection",
  "filterandcollect",
  "filterandcount",
  "projectionandfilter",
  "collect",
  "offsetlimit",
  "count",
  "distinct",
  "offsetlimitandcollect",
  "join",
  "has",
  "orderby",
  "groupbycount",
  "groupbysum",
]
class AbstractCollectionResource(AbstractResource):
    def __init__(self, request):
        super().__init__(request)
    
    def rows_as_dict(self, rows):
        return [dict(row) for row in rows]
    async def get_representation(self):
        dialect_db = self.request.app.dialect_db_class(self.request.app.db, self.metadata_table(), None)
        rows = await dialect_db.fetch_all()
        res = self.rows_as_dict(rows)
        return response.json(res)
        
    async def get_representation_given_path(self, path):
        #result = getattr(foo, 'bar')(*params)
        if path[-1] == '/': #Removes trail slash
            path = path[:-1]
        try:
            operation_name_or_atribute_comma = path.split('/')[0].strip().lower()
            if operation_name_or_atribute_comma in collection_function_names:
                method_execute_name = "pre_" + operation_name_or_atribute_comma
                return await getattr(self, method_execute_name)(*[path])
            else:
                att_names = operation_name_or_atribute_comma.split(',')
                for att_name in att_names:
                    if att_name not in self.attribute_names():
                        return response.json(f"The operation or attribute {att_name} does not exists", status=400)        
                return await self.pre_projection(path)
                
        except (RuntimeError, TypeError, NameError):
            raise
            return response.json("error: Error no banco")

    async def pre_offsetlimit(self, path):
        arguments_from_url_by_slash = path.split('/')
        arguments_from_url = arguments_from_url_by_slash[1].split('&')
        #offsetlimit with 2 arguments. Ex.: offsetlimit/1&10
        if len(arguments_from_url_by_slash) == 2:
            return await self.offsetlimit(int(arguments_from_url[0]), int(arguments_from_url[1]))
        #offsetlimit with 4 arguments. Ex.: offsetlimit/1&10/orderby/name,sexo&desc
        if len(arguments_from_url_by_slash) == 4:
            arr_off_and_limit = arguments_from_url_by_slash[1].split('&')
            arr_order_asc = arguments_from_url_by_slash[3].split('&')
            arr_order_asc = arr_order_asc if len(arr_order_asc) == 2 else [arr_order_asc[0], 'asc']
            return await self.offsetlimit(int(arr_off_and_limit[0]), int(arr_off_and_limit[1]), arr_order_asc[0], arr_order_asc[1])
        raise SyntaxError("The operation offsetlimit has two integer arguments.")
        
    async def offsetlimit(self, offset: int, limit: int, str_lst_attribute_comma = None, asc = None):
        dialect_db = self.request.app.dialect_db_class(self.request.app.db, self.metadata_table(), None)
        rows = await dialect_db.offset_limit(offset, limit, str_lst_attribute_comma, asc)
        res =  self.rows_as_dict(rows)
        return response.json(res)
        
    async def pre_count(self, path):
        return await self.count()
    async def count(self):
        dialect_db = self.request.app.dialect_db_class(self.request.app.db, self.metadata_table(), None)
        result = await dialect_db.count()
        return response.json(result['count'])
    
    async def pre_orderby(self, path):
        return await self.orderby(path)
    async def orderby(self, path):
        dialect_db = self.request.app.dialect_db_class(self.request.app.db, self.metadata_table(), None)
        str_attribute_as_comma_list = path.split('/')[1]
        att_names =  str_attribute_as_comma_list.split(',')
        for att_name in att_names:
            if att_name not in self.attribute_names():
                return response.json(f"The attribute {att_name} does not exists", status=400)
        rows = await dialect_db.order_by(str_attribute_as_comma_list)
        res = self.rows_as_dict(rows)
        return response.json(res)
    
    async def pre_projection(self, path):
        str_att_names_as_comma = path.split('/')[0] # /projection/attri or /attri
        if str_att_names_as_comma == "projection":
            str_att_names_as_comma = path.split('/')[1]
        return await self.projection(str_att_names_as_comma)
    
    async def projection(self, str_att_names_as_comma):
        rows = await self.dialect_DB().projection(str_att_names_as_comma, None)
        res = self.rows_as_dict(rows)
        return response.json(res)
         
    async def pre_groupbycount(self, path):
        str_atts = path.split('/')[1] #groupbycount/departamento
        return await self.groupbycount(str_atts)

    async def groupbycount(self, str_att_names_as_comma):
        rows = await self.dialect_DB().group_by_count(str_att_names_as_comma)
        res = self.rows_as_dict(rows)
        return response.json(res)
    
    async def pre_groupbysum(self, path):
        str_atts = path.split('/')[1]  #empolyees/name&salary
        fields_from_path = str_atts[1].split('&')
        if self.fields_from_path_not_in_attribute_names(fields_from_path):
            return response.json(f"The attribute {str_atts} does not exists", status=400)
        
        return await self.groupbysum(self, path)

    async def groupbysum(self, str_att_names_as_comma, att_to_sum):
        rows = await self.dialect_DB().group_by_sum(str_att_names_as_comma, att_to_sum)
        res = self.rows_as_dict(rows)
        return response.json(res)
    
    async def pre_filter(self, path):
        return await self.filter(path[6:]) #len('filter') = 6

    def dict_name_operation(self) -> Dict[str, 'function']:
        return {'filter': self.filter}

    async def filter(self, path: str) -> "AbstractCollectionResource":
        """
        :param path: expression
        :return: self
        :description: Filter a collection given an expression
        :example: http://server/api/drivers/filter/license/eq/valid
        """
        interp = Interpreter(path, self.entity_class(), self.dialect_DB())
        try:
            whereclause = await interp.translate()
        except  (Exception, SyntaxError):
            print(f"path: {path}")
            raise
        print(f'whereclause: {whereclause}')
        rows =  await self.dialect_DB().filter(whereclause)
        return response.json(self.rows_as_dict(rows))