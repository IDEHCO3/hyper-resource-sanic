import time

from asyncpg import UniqueViolationError, DataError

from settings import BASE_DIR, SOURCE_DIR
import sanic
from typing import Dict, List, Optional
import json, os

from src.hyper_resource.abstract_resource import AbstractResource, MIME_TYPE_JSONLD
from src.hyper_resource.context.abstract_context import AbstractCollectionContext
from src.hyper_resource.common_resource import CONTENT_TYPE_HTML, CONTENT_TYPE_JSON, CONTENT_TYPE_XML, dict_to_xml
from ..orm.action_type import ActionFunction
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

    async def rows_as_dict(self, rows) -> List[Dict]:
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
        if ',' in operation_name_or_attribute_comma or operation_name_or_attribute_comma in self.attribute_names():
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
        paths: List[str] = self.normalize_path_as_list(path, '/')
        off_limit: List[str] = paths[1].split('&')
        if len(off_limit) == 1:
            return self.dialect_DB().predicate_offset_limit(0, int(off_limit[0]))
        return self.dialect_DB().predicate_offset_limit(int(off_limit[0]), int(off_limit[1]))

    async def execute_method(self, path):
        operation_name = self.operation_name_in_path(path)
        return await getattr(self, action_name(operation_name))(*[path])

    async def response_by_qb(self, qb: QueryBuilder):
        print(qb.query())
        if (CONTENT_TYPE_JSON in self.accept_type()):
            rows = await self.dialect_DB().fetch_all_by(qb.query())
            rows_dict = await self.rows_as_dict(rows)
            if qb.has_only_one_aggregate_math_function():
                key, value = rows_dict[0].popitem()
                return sanic.response.json(value)
            return sanic.response.json(rows_dict or [], content_type=CONTENT_TYPE_JSON)

        rows = await self.dialect_DB().fetch_all_by(qb.query())
        rows_dict = await self.rows_as_dict(rows)
        if qb.has_only_one_aggregate_math_function():
            key, value = rows_dict[0].popitem()
            return sanic.response.json(value)
        return sanic.response.json(rows_dict or [])

    async def add_where_in_qb(self, qb: QueryBuilder, path: str):
        qb.add_where(await self.interpreter(path[6:]).translate_lookup())

    async def add_collect_in_qb(self, qb, path):
        colL_predicate: str = await self.interpreter().translate_collect(path, self.protocol_host())
        qb.add_collect(colL_predicate)

    async def add_projection_in_qb(self, qb: QueryBuilder, path: str):
        path_ = path if path[0: len('projection/')] == 'projection/' else 'projection/' + path
        qb.add_column(self.predicate_projection(self.normalize_path(path_)))

    async def add_group_by_in_qb(self, qb: QueryBuilder, path: str):
        qb.add_group_by(await self.predicate_group_by(path))

    async def add_count_in_qb(self, qb: QueryBuilder, path: str):
        qb.add_count()

    async def add_sum_in_qb(self, qb: QueryBuilder, path: str):
        qb.add_sum(self.normalize_path(path[4:]))

    async def add_max_in_qb(self, qb: QueryBuilder, path: str):
        qb.add_max(self.normalize_path(path[4:]))

    async def add_min_in_qb(self, qb: QueryBuilder, path: str):
        qb.add_min(self.normalize_path(path[4:]))

    async def add_avg_in_qb(self, qb: QueryBuilder, path: str):
        qb.add_avg(self.normalize_path(path[4:]))

    async def add_offsetlimit_in_qb(self, qb: QueryBuilder, path: str):
        pred_offset_limit: str = self.predicate_offsetlimit(path)
        qb.add_offsetlimit(pred_offset_limit)

    async def add_order_by_in_qb(self, qb: QueryBuilder, path: str):
        qb.add_order_by(self.predicate_order_by(path[8:]))

    def dict_qb_function(self) -> Dict:
        return {
            'collect': self.add_collect_in_qb,
            'projection': self.add_projection_in_qb,
            'count': self.add_count_in_qb,
            'orderby': self.add_order_by_in_qb,
        }

    def dict_qb_lookup_function(self) -> Dict:
        return {
            'filter': self.add_where_in_qb,
            'offsetlimit': self.add_offsetlimit_in_qb,
        }

    def dict_qb_aggregate_function(self) -> Dict:
        return {
            'sum': self.add_sum_in_qb,
            'avg': self.add_avg_in_qb,
            'max': self.add_max_in_qb,
            'min': self.add_min_in_qb,
            'groupby': self.add_group_by_in_qb,
        }
    def dict_query_builder_function(self):
        pass
    async def execute_qb_function(self, qb, path):
        qb_function: Dict = {**self.dict_qb_function(), **self.dict_qb_lookup_function(), **self.dict_qb_aggregate_function() }
        operation_name: str = self.operation_name_in_path(path)
        if operation_name not in qb_function:
            msg: str = f"Error in path. This {operation_name} does not exists"
            raise PathError(msg, 400)
        return await qb_function[operation_name](*[qb, path])

    async def get_representation_given_path(self, path: str) -> str:
        try:
            paths: List[str] = self.normalize_path_as_list(path, '/*/')
            qb: QueryBuilder = QueryBuilder(dialect_db=self.dialect_DB(), entity_class=self.entity_class())
            qb.has_geometry = False
            for path in paths:
                await self.execute_qb_function(qb, path)
            qb.add_table_name(self.dialect_DB().schema_table_name())
            return await self.response_by_qb(qb)
        except PathError as err:
            return sanic.response.json(err.message, err.code)
        except (RuntimeError, TypeError, NameError) as err:
            return sanic.response.json("Error {0}". format(err))

    async def get_representation_given_path_old(self, path: str):
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