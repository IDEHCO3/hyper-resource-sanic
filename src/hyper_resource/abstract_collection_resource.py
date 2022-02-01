import time

from asyncpg import UniqueViolationError, DataError

from settings import BASE_DIR, SOURCE_DIR
import sanic
from typing import Dict, List, Optional
import json, os

from src.hyper_resource.abstract_resource import AbstractResource, MIME_TYPE_JSONLD
from src.hyper_resource.context.abstract_context import AbstractCollectionContext
from src.hyper_resource.common_resource import CONTENT_TYPE_HTML, CONTENT_TYPE_JSON, CONTENT_TYPE_XML, dict_to_xml
from ..url_interpreter.interpreter import Interpreter
from ..url_interpreter.interpreter_error import PathError
from ..url_interpreter.interpreter_new import InterpreterNew
from ..orm.dictionary_actions_abstract_collection import dic_abstract_collection_lookup_action
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
        self.context_class = AbstractCollectionContext
        self.function_names = None

    def get_function_names(self) -> List[str]:
        if self.function_names is None:
            self.function_names = list(dic_abstract_collection_lookup_action.keys())
        return self.function_names

    async def rows_as_dict(self, rows) -> List:
        return [await self.dialect_DB().convert_row_to_dict(row) for row in rows]

    async def get_html_representation(self):
        # Temporario até gerar código em html para recurso não espacial
        rows = await self.dialect_DB().fetch_all_as_json(prefix_col_val=self.protocol_host())
        #rows = await self.dialect_DB().fetch_all()
        #rows = await self.rows_as_dict(rows)
        return sanic.response.text(rows or [], content_type=CONTENT_TYPE_JSON)

    async def get_json_representation(self):

        start = time.time()
        print(f"time: {start} start rows in python")

        #rows = await self.dialect_DB().fetch_all()
        #rows_from_db = await self.rows_as_dict(rows)
        #res = sanic.response.json(rows_from_db or [])
        rows = await self.dialect_DB().fetch_all_as_json(prefix_col_val=self.protocol_host())
        res = sanic.response.text(rows or [], content_type=CONTENT_TYPE_JSON)
        end = time.time()
        print(f"time: {end - start} end rows in python")
        return res

    async def get_representation(self):
        accept = self.accept_type()
        if CONTENT_TYPE_HTML in accept:
            return await self.get_html_representation()
        else:
            return await self.get_json_representation()
    def first_word(self, path: str)->str:
        """
        :param path: is a substr from iri.  Ex.: filter/first_name/eq/John
        :return: the first word in path
        """
        return path.split('/')[0].strip().lower()

    def normalize_path(self, path: str)->str:
        """
        :param path: is a substr from iri.  Ex.: /filter/first_name/eq/John
        :return: Removes trail slash and returns str
        """
        return path[:-1] if path[-1] == '/' else path

    async def get_representation_given_path(self, path: str):
        # result = getattr(foo, 'bar')(*params)
        #path = self.normalize_path(a_path)
        try:
            operation_name_or_attribute_comma = self.first_word(path)
            if operation_name_or_attribute_comma in self.get_function_names():
                return await getattr(self, operation_name_or_attribute_comma)(*[path])
            else:
                att_names = set(operation_name_or_attribute_comma.split(','))
                atts = att_names.difference(set(self.attribute_names()))
                if len(atts) ==1 :
                   return sanic.response.json(f"The operation or attribute in this {list(atts)} does not exists", status=400)
                elif len(atts) > 1:
                    return sanic.response.json(f"The operations or attributes {list(atts)} do not exists",
                                               status=400)
                return await self.projection(path)

        except (RuntimeError, TypeError, NameError) as err:
            print(err)
            raise


    async def offsetlimit(self, path):
        arguments_from_url_by_slash = path.split('/')
        arguments_from_url = arguments_from_url_by_slash[1].split('&')
        # offsetlimit with 2 arguments. Ex.: offsetlimit/1&10
        if len(arguments_from_url_by_slash) != 2:
            raise SyntaxError("The operation offsetlimit has two mandatory integer arguments.")
        # offsetlimit with 4 arguments. Ex.: offsetlimit/1&10/orderby/name,sexo&desc
        if len(arguments_from_url) == 2:
            return await self._offsetlimit(int(arguments_from_url[0]), int(arguments_from_url[1]))
        if len(arguments_from_url) == 3:
            return await self._offsetlimit(int(arguments_from_url[0]), int(arguments_from_url[1]), arguments_from_url[2] )
        if len(arguments_from_url) == 4:
            return await self._offsetlimit(int(arguments_from_url[0]), int(arguments_from_url[1]), arguments_from_url[2],arguments_from_url[3] )
        raise SyntaxError("The operation offsetlimit has two mandatory integer arguments.")

    async def _offsetlimit(self, offset: int, limit: int, str_lst_attribute_comma: str = None, asc: str = None):
        #if self.is_content_type_in_accept('text/html'):
        #    return await self.get_html_representation()
        rows = await self.dialect_DB().offset_limit(offset, limit, str_lst_attribute_comma, asc, None)
        rows_dict = await self.rows_as_dict(rows)
        return sanic.response.text(rows_dict or [], content_type='application/json')

    async def count(self, path):
        result = await self.dialect_DB().count()
        return sanic.response.json(result['count'])

    async def orderby(self, path):
        str_attribute_as_comma_list = path.split('/')[1]
        att_names = str_attribute_as_comma_list.split(',')
        for att_name in att_names:
            if att_name not in self.attribute_names():
                return sanic.response.json(f"The attribute {att_name} does not exists", status=400)
        rows = await self.dialect_DB().order_by(str_attribute_as_comma_list)
        res = await self.rows_as_dict(rows)
        return sanic.response.json(res)

    def enum_attribute_from_projection(self, path: str) -> str:
        enum_attribute_name = self.first_word(path)
        if enum_attribute_name == 'projection':
            return path.split('/')[1]  # srv/projection/name,gender,age or srv/name,gender,age

    async def response_given(self, rows: List):
        rows_dict = await self.rows_as_dict(rows)
        if CONTENT_TYPE_JSON in self.accept_type():
            return sanic.response.json(rows_dict or [])
        if CONTENT_TYPE_XML in self.accept_type():
            dict_xml = dict_to_xml(rows_dict)
            return sanic.response.text(dict_xml, content_type=CONTENT_TYPE_XML)
        return sanic.response.json(rows_dict or [])

    async def projection(self, path: str):
        """
        :param path:
        :return:
        path should be:
        name,gender
        name,gender/filter/age/gte/100
        name,gender/orderby/name,age
        name,gender/filter/age/gte/100/*/orderby/name,age
        projection/name,gender
        projection/name,gender/filter/age/gte/100
        projection/name,gender/orderby/name,age&asc
        projection/name,gender/filter/age/gte/100/*/orderby/name,age&asc
        """
        paths: List[str] = path.split('/')
        if paths[0].lower().strip() != 'projection': #path ->name,gender
            paths.insert(0,'projection')
        if len(paths) == 2:
            return await self.projection_only(path)
        if paths[2] == 'filter' and '*' not in paths:
            filter_path: str = '/'.join(paths[3:])
            attribute_names: List[str] = paths[1].split(',')
            return await self.projection_filter(attribute_names, filter_path)
        if paths[2] == 'orderby' and '*' not in paths:
            if '&' in paths[3]:
                enum_attribute_sort, order = paths[3].split('&')
            else:
                enum_attribute_sort = paths[3]
                order = 'asc'
            attribute_names: List[str] = paths[1].split(',')
            return await self.projection_sort(attribute_names, enum_attribute_sort.split(','), order)
        if paths[2] == 'filter' and '*' in paths and paths[-2].lower().strip()=='orderby':
            return await self.projection_filter_sort(path)
        return PathError(f'Error in {path}', 400)

    async def projection_only(self, path: str):
        enum_attribute_name = path.split('/')[1]  # srv/projection/name,gender,age or srv/name,gender,age
        attr_names: List[str] = [a.strip() for a in enum_attribute_name.split(',')]
        rows = await self.dialect_DB().fetch_all(list_attribute=attr_names , prefix=self.protocol_host())
        return await self.response_given(rows)

    async def projection_filter(self, attribute_names: List[str], selection_path: str):
        interp = InterpreterNew(selection_path, self.entity_class(), self.dialect_DB())
        try:
            whereclause = await interp.translate_lookup()
        except (Exception, SyntaxError):
            print(f"Error in Path: {selection_path}")
            raise
        print(f'whereclause: {whereclause}')
        where: str = f' where {whereclause}'
        rows = await self.dialect_DB().fetch_all(list_attribute=attribute_names,where=where, prefix=self.protocol_host())
        return await self.response_given(rows)

    async def projection_sort(self, attribute_names: List[str], attributes_sort: List[str], order: str = 'asc'):
        enum_column_name: str = self.entity_class().enum_column_names_as_given_attributes(attributes_sort)
        order_by: str = f' order by {enum_column_name} {order}'
        rows = await self.dialect_DB().fetch_all(list_attribute=attribute_names, where=None, order_by=order_by,
                                                 prefix=self.protocol_host())
        return await self.response_given(rows)

    async def projection_filter_sort(self, path: str):
        pass

    async def groupbycount(self, path):
        str_atts = path.split('/')[1]  # groupbycount/departamento
        rows = await self.dialect_DB().group_by_count(str_atts, None, 'JSON')
        return sanic.response.text(rows or [], content_type=CONTENT_TYPE_JSON)

    async def groupbysum(self, path):
        str_atts = path.split('/')[1]  # empolyees/name&salary
        fields_from_path = str_atts[1].split('&')
        if self.fields_from_path_not_in_attribute_names(fields_from_path):
            return sanic.response.json(f"The attribute {str_atts} does not exists", status=400)
        return await self._groupbysum(self, path, 'JSON')

    async def _groupbysum(self, str_att_names_as_comma, att_to_sum):
        rows = await self.dialect_DB().group_by_sum(str_att_names_as_comma, att_to_sum, 'JSON')
        return sanic.response.json(rows)


    def dict_name_operation(self) -> Dict[str, 'function']:
        return {'filter': self.filter}

    def filter_base_response(self, rows):
        return sanic.response.text(rows or [], content_type=CONTENT_TYPE_JSON)

    async def predicate_query_from(self, path: str)-> str:

        interp = Interpreter(path, self.entity_class(), self.dialect_DB())
        try:
            return await interp.translate()

        except  (Exception, SyntaxError):
            print(f"path: {path}")
            raise

    def path_as_array_lookup_aggregate_order(self, path: str) -> List[str]:
        ls_path = path.split('/./')
        if len(ls_path) == 1:
            return ls_path
        elif len(ls_path) == 2:
            return [ls_path[0] + '/', '/' + ls_path[1]]
        else:
            ls = [ls_path[0] + '/']
            for s in ls_path[1:-1]:
                ls.append('/' + s + '/')
            ls.append('/' + ls_path[0])
            return ls
    async def filter(self, path: str):  # -> "AbstractCollectionResource":
        """
        params: path
        return: self
        description: Filter a collection given an expression
        example: http://server/api/drivers/filter/license/eq/valid
        """
        #self.call_filter(path)
        interp = InterpreterNew(path[6:], self.entity_class(), self.dialect_DB())
        try:
            whereclause = await interp.translate_lookup()
        except (Exception, SyntaxError):
            print(f"Error in Path: {path}")
            raise
        print(f'whereclause: {whereclause}')
        rows = await self.dialect_DB().filter_as_json(whereclause, None ,self.protocol_host())
        return sanic.response.text(rows or [], content_type=CONTENT_TYPE_JSON) #self.filter_base_response(rows)

        #return sanic.response.json([json.dumps(dict(row)) for row in rows])  # response.json(self.rows_as_dict(rows))

    async def filter_orderby(self, path: str):
        pass

    async def filter_count(self, path: str):
        pass

    async def filter_collect(self, path: str):
        pass

    async def head(self):
        return sanic.response.json({"context": 1})

    async def post(self):
        data = self.request.json
        print(f"Dados enviados: {data}")
        try:
            self.validate_data(data)
            id = await self.dialect_DB().insert(data)
            path = self.request.path if self.request.path[-1] != '/' else self.request.path[:-1]
            content_location = f'{self.request.host}{path}/{str(id)}'
        except UniqueViolationError as err:
            print(err)
            return sanic.response.json({"Error": "Resource already exists"}, status=409)
        except DataError as err:
            print(err)
            return sanic.response.json({"Error": "Data type"}, status=409)
        except (Exception, SyntaxError, NameError) as err:
            print(type(err))
            print(err)
            return sanic.response.json({"Error": f"{err}"}, status=400)


        return sanic.response.json(id, status=201, headers={'Content-Location': content_location })

    async def options(self, *args, **kwargs):
        context = self.context_class(self.dialect_DB(), self.metadata_table(), self.entity_class())
        return sanic.response.json(context.get_basic_context(), content_type=MIME_TYPE_JSONLD)

    """
        
     projection
     projection selection
     projection sort
     projection selection sort
     selection
     selection, aggregate
     selection, aggregate, sort
     selection, aggregate, aggregate
     selection, aggregate, aggregate, sort
     selection, sort
     aggregate
     aggregate, sort
     aggregate, aggregate
     aggregate, aggregate, sort
     sort
     
    project
    project_sort
    project_filter
    project_filter_sort
    filter
    filter-sort
    filer-collect
    filter-collect-collect
    filter-collect-sort
    filter-collect-collect-sort
    """