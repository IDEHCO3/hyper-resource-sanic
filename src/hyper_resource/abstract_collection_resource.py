import time

from asyncpg import UniqueViolationError, DataError

from settings import BASE_DIR, SOURCE_DIR
import sanic
from typing import Dict, List, Optional
import json, os

from src.hyper_resource.abstract_resource import AbstractResource, MIME_TYPE_JSONLD
from src.hyper_resource.context.abstract_context import AbstractCollectionContext
from src.hyper_resource.common_resource import CONTENT_TYPE_HTML, CONTENT_TYPE_JSON, CONTENT_TYPE_XML, dict_to_xml
from ..orm.query_builder import QueryBuilder
from ..url_interpreter.interpreter import Interpreter
from ..url_interpreter.interpreter_error import PathError
from ..url_interpreter.interpreter_new import InterpreterNew
from ..orm.dictionary_actions_abstract_collection import dic_abstract_collection_lookup_action, action_name

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
        #rows = await self.dialect_DB().fetch_all_as_json(prefix_col_val=self.protocol_host())
        rows = await self.dialect_DB().fetch_all(prefix=self.protocol_host())
        rows_db = await self.rows_as_dict(rows)
        return sanic.response.json(rows_db)
        #return sanic.response.text(rows or [], content_type=CONTENT_TYPE_JSON)

    async def get_json_representation(self):

        start = time.time()
        print(f"time: {start} start rows in python")

        rows = await self.dialect_DB().fetch_all()
        rows_from_db = await self.rows_as_dict(rows)
        res = sanic.response.json(rows_from_db or [])
        #rows = await self.dialect_DB().fetch_all_as_json(prefix_col_val=self.protocol_host())
        #res = sanic.response.text(rows or [], content_type=CONTENT_TYPE_JSON)
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

    def operation_name_in_path(self, path) -> str:
        operation_name_or_attribute_comma: str = self.first_word(path)
        if ',' in operation_name_or_attribute_comma:
            return 'projection'
        if operation_name_or_attribute_comma in self.get_function_names():
            return operation_name_or_attribute_comma
        msg = f"This {path} is incorrect"
        print(msg)
        raise PathError(msg, 400)

    def normalize_path(self, path: str) -> str:
        """
        :param path: is a substr from iri.  Ex.: /filter/first_name/eq/John
        :return: Removes trail slash and returns str
        """
        return path[:-1] if path[-1] == '/' else path

    async def predicate_filter(self, path: str) -> str:
        return await self.interpreter(path).translate_lookup()

    async def predicate_group_by(self, path: str) -> str:
        return path.split('/')[1]

    async def predicate_collect(self, path: str, query_collect: str) -> str:
        a_query_collect: str = query_collect
        if len(query_collect) == 0:
            return await self.interpreter(path).translate_collect(path,self.protocol_host())
        a_query_collect += f', ({await self.interpreter(path).translate_collect(path, self.protocol_host())})'

    def predicate_projection(self, path: str) -> str:
        attr_names: List[str] = path[len('projection/'):].split(',')
        attr_differs: List[str] = list(set(attr_names) - set(self.attribute_names()))
        size_difference: int = len(attr_differs)
        if size_difference == 0:
            return self.dialect_DB().column_names_alias(attrib_names=attr_names, prefix_col_val=self.protocol_host())
        elif size_difference == 1:
            att = attr_differs[0]
            raise PathError(f"The attribute {att} does not exists", 400)
        elif size_difference >= 2:
            atts = attr_differs
            raise PathError(f"These attributes {atts} do not exist", 400)
        return ','.join(attr_names)

    def predicate_offsetlimit(self, path) -> str:
        pass

    async def execute_method(self, path):
        operation_name = self.operation_name_in_path(path)
        return await getattr(self, action_name(operation_name))(*[path])

    async def get_representation_given_path_new(self, path: str) -> str:
        paths: List[str] = self.normalize_path_as_list(path, '/*/')
        qb: QueryBuilder = QueryBuilder()
        if len(paths) == 1:
            return await self.execute_method(paths[0])
        for path in paths:
            operation_name: str = self.operation_name_in_path(path)
            if operation_name == 'filter':
                qb.add_where(await self.interpreter(path[6:]).translate_lookup())
            elif operation_name == 'collect':
                qb.add_column(await self.interpreter().translate_collect(path, self.protocol_host()))
            elif operation_name == 'projection':
                qb.add_column(self.predicate_projection(path))
            elif operation_name == 'groupby':
                qb.add_group_by(await self.predicate_group_by(path))
            elif operation_name == 'count':
                qb.add_count()
            elif operation_name == 'offsetlimit':
                qb.add_offsetlimit(self.predicate_offsetlimit(path))
            elif operation_name == 'sum':
                qb.add_sum(path)
            elif operation_name == 'avg':
                count_ = self.predicate_avg(path)
        qb.add_table_name(self.dialect_DB().schema_table_name())
        return await self.response_by_qb(qb)

    async def get_representation_given_path(self, path: str):
        # result = getattr(foo, 'bar')(*params)
        #path = self.normalize_path(a_path)
        try:
            operation_name_or_attribute_comma = self.first_word(path)
            if operation_name_or_attribute_comma in self.get_function_names():
                return await getattr(self, action_name(operation_name_or_attribute_comma))(*[path])
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
        """
        offsetlimit
        offsetlimit orderby
        offsetlimit agregate
        offsetlimit agregate agregate
        offsetlimit agregate orderby
        offsetlimit agregate agragate orderby
        :param path:
        :return:
        """
        arguments_from_url_by_slash = path.split('/')
        arguments_from_url = arguments_from_url_by_slash[1].split('&')
        # offsetlimit with 2 arguments. Ex.: offsetlimit/1&10
        if len(arguments_from_url_by_slash) != 2:
            raise SyntaxError("The operation offsetlimit has two mandatory integer arguments.")
        # offsetlimit with 4 arguments. Ex.: offsetlimit/1&10/orderby/name,sexo&desc
        if len(arguments_from_url) == 2:
            return await self.offsetlimit_only(int(arguments_from_url[0]), int(arguments_from_url[1]))
        if len(arguments_from_url) == 3:
            return await self.offsetlimit_only(int(arguments_from_url[0]), int(arguments_from_url[1]), arguments_from_url[2])
        if len(arguments_from_url) == 4:
            return await self.offsetlimit_only(int(arguments_from_url[0]), int(arguments_from_url[1]), arguments_from_url[2], arguments_from_url[3])
        raise SyntaxError("The operation offsetlimit has two mandatory integer arguments.")

    async def offsetlimit_only(self, offset: int, limit: int, str_lst_attribute_comma: str = None, asc: str = None):
        #if self.is_content_type_in_accept('text/html'):
        #    return await self.get_html_representation()
        rows = await self.dialect_DB().offset_limit(offset-1, limit, str_lst_attribute_comma, asc, None)
        return await self.response_given(rows)

    async def count(self, path):
        result = await self.dialect_DB().count()
        return sanic.response.json(result)

    async def response_fetch_all(self, list_attribute: Optional[List] = None, where: Optional[str] = None, order_by: Optional[str] = None, prefix: Optional[str] = None):
        rows = await self.dialect_DB().fetch_all(list_attribute=list_attribute, where=where, order_by=order_by, prefix=self.protocol_host())
        return await self.response_given(rows)

    def predicate_order_by(self, path: str) -> str:
        order_by_asc_dsc: str = path
        order_by_asc_dsc = self.normalize_path(order_by_asc_dsc)
        orders_by_asc_dsc: List[str] = []
        if '&' in order_by_asc_dsc:
            enum_attribute_sort, enum_order = order_by_asc_dsc.split('&')
            attribute_name_sort: List[str] = enum_attribute_sort.split(',')
            orders_by_asc_dsc = enum_order.split(',')
        else:
            attribute_name_sort: List[str] = order_by_asc_dsc.split(',')
        column_names: List[str] = self.entity_class().column_names_given_attributes(attribute_name_sort)
        return self.dialect_DB().predicate_order_by(column_names, orders_by_asc_dsc)

    async def orderby(self, path: str) -> str:
        # order_by => orderby/name,gender&asc,desc
        paths: List[str] = self.normalize_path(path).split('/')
        ordr: str = self.predicate_order_by(paths[-1])
        rows = await self.dialect_DB().fetch_all(order_by=ordr, prefix=self.protocol_host())
        return await self.response_given(rows)

    def interpreter(self, path: str = ''):
        return InterpreterNew(path, self.entity_class(), self.dialect_DB())

    async def translate_path(self, path) -> str:
        interp = self.interpreter(path)
        try:
            translated: str = await interp.translate_lookup()
        except (Exception, SyntaxError):
            print(f"Error in Path: {path}")
            raise
        return translated

    async def where_interpreted(self, selection_path: str) -> str:
        predicate: str = await self.translate_path(selection_path)
        print(f'whereclause: {predicate}')
        return f' where {predicate}'


    async def response_given(self, rows: List):
        rows_dict = await self.rows_as_dict(rows)
        if CONTENT_TYPE_JSON in self.accept_type():
            return sanic.response.json(rows_dict or [])
        if CONTENT_TYPE_HTML in self.accept_type():
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
        paths = paths[0:-1] if paths[-1] == '' else paths
        if paths[0].lower().strip() != 'projection': #path ->name,gender
            paths.insert(0,'projection')
        attribute_names: List[str] = [a.strip() for a in paths[1].split(',')]
        if len(paths) == 2:
            return await self.projection_only(attribute_names)
        if paths[2] == 'filter' and '*' not in paths:
            filter_path: str = '/'.join(paths[3:])
            return await self.projection_filter(attribute_names, filter_path)
        if paths[2] == 'orderby' and '*' not in paths:
            if '&' in paths[3]:
                enum_attribute_sort, order = paths[3].split('&')
            else:
                enum_attribute_sort = paths[3]
                order = 'asc'
            return await self.projection_sort(attribute_names, enum_attribute_sort.split(','), order)
        if paths[2] == 'filter' and '*' in paths and paths[-2].lower().strip()=='orderby':
            idx_ast: int = paths.index('*')
            filter_path: str = '/'.join(paths[3: idx_ast])
            _order_by: str = paths[-1]
            return await self.projection_filter_sort(attribute_names, filter_path, _order_by)
        return PathError(f'Error in {path}', 400)

    async def projection_only(self, attribute_names: List[str]):
        rows = await self.dialect_DB().fetch_all(list_attribute=attribute_names, prefix=self.protocol_host())
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

    async def projection_filter_sort(self, attribute_names: List[str], filter_path: str, _order_by: str):
        interp = InterpreterNew(filter_path, self.entity_class(), self.dialect_DB())
        try:
            whereclause = await interp.translate_lookup()
        except (Exception, SyntaxError):
            print(f"Error in Path: {filter_path}")
            raise
        print(f'whereclause: {whereclause}')
        where: str = f' where {whereclause}'
        an_order: str = self.predicate_order_by(_order_by)
        rows = await self.dialect_DB().fetch_all(list_attribute=attribute_names, where=where, order_by=an_order, prefix=self.protocol_host())
        return await self.response_given(rows)

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

    async def collect_old(self, path):
        """
        collect
        collect orderby
        collect offsetlimit
        collect orderby offsetlimit
        collect collect
        collect collect ...orderby
        collect collect ...offselimit
        collect collect ...orderby offsetlimit

        :param path:
        :return:
        """
        paths: List[str] = self.normalize_path_as_list(path, '/*/')
        if len(paths) == 1:
            return await self.collect_only(paths[0])

    async def collect_base(self, path: str) -> str:
        a_path: str = path[8:]  # len(collect/) = 8
        if '&' in a_path:
            paths: List[str] = a_path.split('&')
            attribute_name_actions: str = paths[1]
            enum_attrib_name: str = paths[0]
        else:
            attribute_name_actions: str = a_path
            enum_attrib_name: Optional[str] = ''  # /collect/geom/transform/3005/area
        action_translated: str = await self.translate_path(attribute_name_actions)  # path => filter/license/eq/valid
        attribute_names: List[str] = enum_attrib_name.split(',') + [
            attribute_name_actions[0: attribute_name_actions.index('/')]]
        if not self.entity_class().has_all_attributes(attribute_names):
            non_attribute_names = [att for att in attribute_names if self.entity_class().has_not_attribute(att)]
            if len(non_attribute_names) == 1:
                return sanic.response.text(f'This attribute {non_attribute_names} does not exist.', status=400)
            else:
                return sanic.response.text(f'These attributes {",".join(non_attribute_names)} do not exist.',
                                           status=400)
        attribute_name_actions_norm = self.normalize_path(attribute_name_actions)
        last_action_name: str = attribute_name_actions_norm[attribute_name_actions_norm.rindex("/") + 1:]
        predicate_action: str = f'{action_translated} as {last_action_name}'
        return self.dialect_DB().predicate_collect(attribute_names[0:-1], predicate_action,
                                                                 self.protocol_host())
    async def collect(self, path: str): #/collect/date,name&geom/transform/3005/area
        interp = self.interpreter()
        select_fields: str = await interp.translate_collect(path, self.protocol_host())
        query: str = self.dialect_DB().query_build_by(enum_fields=select_fields)
        rows = await self.dialect_DB().fetch_all_by(query)
        return await self.response_given(rows)

    async def filter(self, path: str):  # -> "AbstractCollectionResource":
        """
        filter
        filter orderby
        filter count
        filter collect
        filter collect orderby
        filter collect collect orderby
        """
        #self.call_filter(path)
        #return sanic.response.json([json.dumps(dict(row)) for row in rows])  # response.json(self.rows_as_dict(rows))
        paths: List[str] = self.normalize_path_as_list(path, '/*/')
        if len(paths) == 1:
            return await self.filter_only(path)
        if len(paths) == 2:
            sub_paths: List[str] = self.normalize_path_as_list(paths[-1], '/')
            operation_1: str = self.normalize_path(sub_paths[0].strip('/').strip().lower())
            filter_path: str = paths[0] + '/' if paths[0][-1] == ')' else paths[0]
            if operation_1 == 'count':
                return await self.filter_count(filter_path)
            if operation_1 == 'orderby':
                return await self.filter_order_by(filter_path[6:], sub_paths[1])
            if operation_1 == 'collect':
                return await self.filter_collect(filter_path[6:], sub_paths)

    async def filter_only(self, path: str):  # -> "AbstractCollectionResource":
        """
        params: path
        return: self
        description: Filter a collection given an expression
        example: http://server/api/drivers/filter/license/eq/valid
        :param path:
        :return:
        """
        whereclause = await self.where_interpreted(path[6:])  # path => filter/license/eq/valid
        rows = await self.dialect_DB().fetch_all(where=whereclause, prefix=self.protocol_host())
        return await self.response_given(rows)  # self.filter_base_response(rows)

    async def filter_order_by(self, filter_expression: str, orderby_expression: str):
        order_by_: str = self.predicate_order_by(orderby_expression)
        where: str = await self.where_interpreted(filter_expression)
        rows = await self.dialect_DB().fetch_all( where=where, order_by= order_by_,prefix=self.protocol_host())
        return await self.response_given(rows)

    async def filter_count(self, path: str):
        where = await self.where_interpreted(path[6:])  # path => filter/license/eq/valid
        row = await self.dialect_DB().count(where=where)
        return sanic.response.json(row)

    async def filter_collect(self, filter_path: str, sub_paths: List[str]):
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