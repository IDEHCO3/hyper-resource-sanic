import time
from typing import List, Tuple, Optional

from geoalchemy2 import Geometry
from shapely import wkb

from settings import BASE_DIR, SOURCE_DIR
import sanic

from src.hyper_resource.common_resource import CONTENT_TYPE_HTML, CONTENT_TYPE_OCTET_STREAM, CONTENT_TYPE_GEOBUF, \
    CONTENT_TYPE_WKB, CONTENT_TYPE_VECTOR_TILE, CONTENT_TYPE_JSON, CONTENT_TYPE_GEOJSON, CONTENT_TYPE_GML, \
    CONTENT_TYPE_FLATGEOBUFFERS
from src.hyper_resource.spatial_collection_resource import SpatialCollectionResource
from src.orm.database_postgis import DialectDbPostgis
import json, os

from src.orm.dictionary_actions_abstract_collection import action_name
from src.url_interpreter.interpreter import Interpreter
from src.url_interpreter.interpreter_new import InterpreterNew

MIME_TYPE_JSONLD = "application/ld+json"
from geoalchemy2.shape import to_shape
class FeatureCollectionResource(SpatialCollectionResource):

    def __init__(self, request):
        super().__init__(request)

    def get_geom_attribute(self) -> str:
        return  self.entity_class().geo_attribute_name()

    def geom_attribute_in(self, enum_attribute_name: str) -> bool:
        return self.get_geom_attribute() in enum_attribute_name.split(',')

    def geom_attribute_not_in(self, enum_attribute_name: str) -> bool:
        return not self.geom_attribute_in(enum_attribute_name)

    def is_action_geom(self, attribute_name: str, action_names: List[str]) -> bool:
        a_type: type = self.entity_class().attribute_type_given(attribute_name)
        tp: object = self.dialect_DB().last_action_in_chain(a_type, action_names)
        return tp in [Geometry]

    def is_not_action_geom(self,attribute_name: str, action_names: List[str]) -> bool:
        return not self.is_action_geom(attribute_name, action_names )

    def get_spatial_function_names(self) -> List[str]:
        return self.dialect_DB().get_spatial_function_names()

    def lookup_function_names(self) -> List[str]:
        return self.dialect_DB().get_spatial_lookup_function_names()

    async def rows_as_dict(self, rows):
        if CONTENT_TYPE_HTML in self.accept_type():
            return await super(FeatureCollectionResource, self).rows_as_dict(rows)
        response_data = []
        geom_attrubute = self.get_geom_attribute()
        if geom_attrubute not in list(rows[0].keys()):
            return await super(FeatureCollectionResource, self).rows_as_dict(rows)
        feature_collection = { "type": "FeatureCollection",}
        try:

            for row in rows:
                row_dict = await self.dialect_DB().convert_row_to_dict(row)
                feature = {"type": "Feature"}
                geometry = wkb.loads(row_dict[geom_attrubute]).__geo_interface__ #json.loads(row_dict[geom_attrubute])
                row_dict.pop(geom_attrubute, None)
                #geometry.pop("crs", None)
                #"crs": {
                #    "type": "name",
                #    "properties": {
                #        "name": "EPSG:4326"
                #    }
                #}
                feature["geometry"] = geometry
                feature["properties"] = row_dict
                response_data.append(feature)
        except Exception as err:
            print(err)
            raise
        feature_collection["features"] = response_data
        return feature_collection

    async def get_json_representation(self):
        start = time.time()
        print(f"time: {start} start rows in python")
        rows = await self.dialect_DB().fetch_all()
        rows_from_db = await self.rows_as_dict(rows)
        res = sanic.response.json(rows_from_db or [])
        #rows = await self.dialect_DB().fetch_all_as_json(prefix_col_val=self.protocol_host())
        #res = sanic.response.text(rows or [], content_type='application/json')
        end = time.time()
        print(f"time: {end - start} end rows in python")
        return res

    async def get_json_representation_given_path(self, path):
       try:
            start = time.time()
            print(f"time: {start} start rows in python")
            action_name = path.split('/')[0].strip().lower()
            if action_name in self.get_spatial_function_names():
                where = await self.predicate_query_from(path)
                rows = await self.dialect_DB().execute_spatial_function(action_name, where)
            rows_from_db = await self.rows_as_dict(rows)
            res = sanic.response.json(rows_from_db or [])
            #rows = await self.dialect_DB().fetch_all_as_json(prefix_col_val=self.protocol_host())
            #res = sanic.response.text(rows or [], content_type='application/json')
            end = time.time()
            print(f"time: {end - start} end rows in python")
            return res
       except (RuntimeError):
           return sanic.response.json({"error: Error no banco"}, status=500)
       except (TypeError, NameError):
           return sanic.response.json({"error: Error no banco"}, status=400)

    async def get_html_representation(self):
        html_filepath = os.path.join(SOURCE_DIR, "hyper_resource", "templates" ,"basic_geo.html")
        with open(html_filepath, "r") as body:
            html_content = body.read()
            content = self.set_html_variables(html_content)
            return sanic.response.html(content, 200)

    async def get_flatgeobuf_representation(self, list_attribute: List[str] = None, where: Optional[str] = None,
                                        order_by: Optional[str] = None, prefix: str = None):
        rows = await self.dialect_DB().fetch_all_as_flatgeobuf(list_attribute=list_attribute, where=where,
                                                           order_by=order_by, prefix_col_val=prefix)
        return sanic.response.raw(rows or [], content_type=CONTENT_TYPE_FLATGEOBUFFERS)

    async def get_geobuf_representation(self, list_attribute: List[str] = None, where: Optional[str] = None, order_by: Optional[str] = None, prefix: str = None):
        #start = time.time()
        #print(f"time: {start} start rows in python")
        rows = await self.dialect_DB().fetch_all_as_geobuf(list_attribute=list_attribute,where=where, order_by=order_by, prefix_col_val=prefix)
        return sanic.response.raw(rows or [], content_type=CONTENT_TYPE_GEOBUF)
        #res = sanic.response.raw(rows or [], content_type=CONTENT_TYPE_GEOBUF)
        #end = time.time()
        #print(f"time: {end - start} end rows in python")
        #return res

    async def get_representation(self):
        accept = self.accept_type()
        if CONTENT_TYPE_HTML in accept:
            return await self.get_html_representation()
        elif (CONTENT_TYPE_GEOBUF in accept) or (CONTENT_TYPE_OCTET_STREAM in accept):
            return await self.get_geobuf_representation(prefix=self.protocol_host())
        elif (CONTENT_TYPE_FLATGEOBUFFERS in accept):
            return await self.get_flatgeobuf_representation(prefix=self.protocol_host())
        else:
            return await self.get_json_representation()

    async def get_mvt_representation_given_path(self, path):
        #application/vnd.mapbox-vector-tile
        params = path.split('&')
        rows = await self.dialect_DB().fetch_as_mvt_tiles(params)
        res = sanic.response.raw(rows or [], content_type= CONTENT_TYPE_VECTOR_TILE)
        return res

    async def get_representation_given_path(self, path: str):
        try:
            if CONTENT_TYPE_HTML in self.accept_type() and self.get_geom_attribute() in self.attribute_names_from(path):
                return await self.get_html_representation()
            operation_name_or_attribute_comma = self.first_word(path)
            if operation_name_or_attribute_comma in self.get_function_names():
                return await getattr(self, action_name(operation_name_or_attribute_comma))(*[path])
            else:
                att_names = set(operation_name_or_attribute_comma.split(','))
                atts = att_names.difference(set(self.attribute_names()))
                if len(atts) == 1:
                    return sanic.response.json(f"The operation or attribute in this {list(atts)} does not exists",
                                               status=400)
                elif len(atts) > 1:
                    return sanic.response.json(f"The operations or attributes {list(atts)} do not exists",
                                               status=400)
                return await self.projection(path)

        except (RuntimeError, TypeError, NameError) as err:
            print(err)
            raise
    async def options(self, *args, **kwargs):
        context = self.context_class(self.dialect_DB(), self.metadata_table(), self.entity_class())
        return sanic.response.json(context.get_basic_context(), content_type=MIME_TYPE_JSONLD)

    def dialect_DB(self)-> DialectDbPostgis:
        if self.dialect_db is None:
          self.dialect_db = DialectDbPostgis(self.request.app.db, self.metadata_table(), self.entity_class())
        return self.dialect_db
    def attribute_names_from(self, path: str) -> Tuple[str]:
        """
        :param path is expect as string enum of attribute Names. Ex.: ../.../name,age
        """
        return tuple(a.strip() for a in path.split(','))

    async def response_request(self, attribute_names: List[str] = None, where: str= None, order_by: str= None, prefix: str =None):
        if CONTENT_TYPE_HTML in self.accept_type():
            return await self.get_html_representation()
        if (CONTENT_TYPE_JSON in self.accept_type()) or (CONTENT_TYPE_GEOJSON in self.accept_type()):
            rows = await self.dialect_DB().fetch_all(list_attribute=attribute_names, where=where, order_by=order_by, prefix=prefix)
            rows_dict = await self.rows_as_dict(rows)
            return sanic.response.json(rows_dict or [])
        if CONTENT_TYPE_GEOBUF in self.accept_type():
            return await self.get_geobuf_representation(list_attribute=attribute_names, where=where, order_by=order_by, prefix=prefix)
        if CONTENT_TYPE_FLATGEOBUFFERS in self.accept_type():
            return await self.get_flatgeobuf_representation(list_attribute=attribute_names, where=where, order_by=order_by, prefix=prefix)
        rows = await self.dialect_DB().fetch_all(list_attribute=attribute_names, where=where, order_by=order_by,
                                                 prefix=prefix)
        rows_dict = await self.rows_as_dict(rows)
        return sanic.response.json(rows_dict or [])

    async def order_by(self, path: str) -> str:
        # order_by => orderby/name,gender&asc
        paths: List[str] = self.normalize_path(path).split('/')
        ordr: str = self.order_by_predicate(paths[-1])
        return await self.response_request(order_by=ordr)

    async def projection_only(self, attribute_names: List[str]):
        if self.get_geom_attribute() not in attribute_names:
            return await super(FeatureCollectionResource, self).projection_only(attribute_names)
        return await self.response_request(attribute_names=attribute_names)

    async def projection_filter(self, attribute_names: List[str], selection_path: str):
        if self.get_geom_attribute() not in attribute_names:
            return super(FeatureCollectionResource, self).projection_filter(attribute_names, selection_path)
        interp = InterpreterNew(selection_path, self.entity_class(), self.dialect_DB())
        try:
            whereclause = await interp.translate_lookup()
        except (Exception, SyntaxError):
            print(f"Error in Path: {selection_path}")
            raise
        print(f'whereclause: {whereclause}')
        where: str = f' where {whereclause}'
        return await self.response_request(attribute_names=attribute_names, where=where, prefix=self.protocol_host())

    async def projection_sort(self, attribute_names: List[str], attributes_sort: List[str], order: str = 'asc'):
        if self.get_geom_attribute() not in attribute_names:
            return await super(FeatureCollectionResource, self).projection_sort(attribute_names, attributes_sort, order)
        if CONTENT_TYPE_HTML in self.accept_type():
            return await self.get_html_representation()
        enum_column_name: str = self.entity_class().enum_column_names_as_given_attributes(attributes_sort)
        order_by: str = f' order by {enum_column_name} {order}'
        return await self.response_request(attribute_names=attribute_names, order_by=order_by, prefix=self.protocol_host())

    async def projection_filter_sort(self, attribute_names: List[str], filter_path: str, _order_by: str):
        if self.get_geom_attribute() not in attribute_names:
            return await super(FeatureCollectionResource, self).projection_filter_sort(attribute_names, filter_path, _order_by)
        where: str = await self.where_interpreted(filter_path)
        order_by: str = self.order_by_predicate(_order_by)
        return await self.response_request(attribute_names=attribute_names, where=where, order_by=order_by)

    async def collect_only(self, path: str): #/collect/date,name&geom/transform/3005/area
        a_path: str = path[8:] #len(collect/) = 8

        if '&' in a_path:
            paths: List[str] = a_path.split('&')
            attribute_name_actions: str = paths[1]
            enum_attrib_name: str = paths[0]
        else:
            attribute_name_actions: str = a_path
            enum_attrib_name: Optional[str] = ''   #/collect/geom/transform/3005/area

        attrib_actions: List[str] = self.normalize_path_as_list(attribute_name_actions, '/')

        if self.geom_attribute_not_in(enum_attrib_name) and self.is_not_action_geom(attrib_actions[0], attrib_actions[1:] ):
            return await super(FeatureCollectionResource, self).collect_only(path)
        action_translated: str = await self.translate_path(attribute_name_actions)  # path => filter/license/eq/valid
        attribute_names: List[str] = enum_attrib_name.split(',') + [attribute_name_actions[0: attribute_name_actions.index('/')]]
        if not self.entity_class().has_all_attributes(attribute_names):
            non_attribute_names = [att for att in attribute_names if self.entity_class().has_not_attribute(att)]
            if len(non_attribute_names) == 1:
                return sanic.response.text(f'This attribute {non_attribute_names} does not exist.', status=400)
            else:
                return sanic.response.text(f'These attributes {",".join(non_attribute_names)} do not exist.', status=400)
        attribute_name_actions_norm = self.normalize_path(attribute_name_actions)
        last_action_name: str = attribute_name_actions_norm[attribute_name_actions_norm.rindex("/")+ 1:]
        predicate_action: str = f'{action_translated} as {last_action_name}'
        select_fields: str = self.dialect_DB().predicate_collect(attribute_names[0:-1], predicate_action, self.protocol_host())
        query = self.dialect_DB().query_build_by(enum_fields=select_fields)
        rows = await self.dialect_DB().fetch_all_by(query)
        return await self.response_given(rows)

    async def filter_only(self, path: str):
        if CONTENT_TYPE_HTML in self.accept_type():
            return await self.get_html_representation()
        try:
            whereclause = await self.where_interpreted(path[6:])
        except (Exception, SyntaxError):
            print(f"Error in Path: {path}")
            raise
        return await self.response_request(where=whereclause, prefix=self.protocol_host())

    async def filter_order_by(self, filter_expression: str, orderby_expression: str):
        order_by_: str = self.order_by_predicate(orderby_expression)
        where: str = await self.where_interpreted(filter_expression)
        return await self.response_request(where=where, order_by=order_by_)

    async def offsetlimit_only(self, offset: int, limit: int, str_lst_attribute_comma: str=None, asc: str=None):
        if self.is_content_type_in_accept(CONTENT_TYPE_HTML):
            return await self.get_html_representation()
        rows = await self.dialect_DB().offset_limit(offset, limit, str_lst_attribute_comma, asc, 'JSON')
        #rows_dict = await self.rows_as_dict(rows)
        return sanic.response.text(rows or [], content_type=CONTENT_TYPE_JSON)

    async def execute_lookup_action(self, action_name: str, path: str):
        """
         lookup
         lookup, aggregate
         lookup, aggregate, sort
         lookup, aggregate, aggregate
         lookup, aggregate, aggregate, sort
         lookup, sort
        """
        sub_paths = path.split('/./')
        if len(sub_paths) == 1:
            return self.dialect_DB().execute

    async def execute_action(self, action_name: str, path: str):
        accept = self.request.headers['accept']
        if action_name in self.lookup_function_names():
            return await self.execute_lookup_action(self, action_name, path)

        path_as_array = self.path_as_array_lookup_aggregate_order(path)
        if action_name in self.dialect_DB().get_spatial_lookup_function_names():
            first_part_path = path_as_array[0][len(action_name):]
            interp = InterpreterNew(first_part_path, self.entity_class(), self.dialect_DB())
            whereclause = await interp.translate()


    """
    AGGREGATE FUNCTIONS
    EXTENT
    http://127.0.0.1:8000/lim-unidade-federacao-a-list/extent/geom
    select st_extent(geom) from bcim.lim_unidade_federacao_a
    
    http://127.0.0.1:8000/lim-unidade-federacao-a-list/extent/geom/*/groupby/sigla
    select sigla, st_extent(geom) from bcim.lim_unidade_federacao_a group by sigla
    
    http://127.0.0.1:8000/lim-unidade-federacao-a-list/filter/regiao/eq/Sul/*/extent/geom/*/groupby/sigla
    select sigla, st_extent(geom) from bcim.lim_unidade_federacao_a where regiao = 'Sul' group by sigla
    
    UNION
    http://127.0.0.1:8000/lim-unidade-federacao-a-list/filter/regiao/eq/Sul/*/union/geom/*/groupby/regiao
    select regiao, st_union(geom) from bcim.lim_unidade_federacao_a where regiao = 'Sul' group by regiao
    """

    """
    chamadas:
     project
     project lookup
     project sort
     project lookup sort
     lookup
     lookup, aggregate
     lookup, aggregate, sort
     lookup, aggregate, aggregate
     lookup, aggregate, aggregate, sort
     lookup, sort
     aggregate
     aggregate, sort
     aggregate, aggregate
     aggregate, aggregate, sort
     sort
    http://127.0.0.1:8000/lim-unidade-federacao-a-list/projection/nome,sigla,geom/
    http://127.0.0.1:8000/lim-unidade-federacao-a-list/nome,sigla,geom/-/filter/regiao/eq/Sul/
    http://127.0.0.1:8000/lim-unidade-federacao-a-list/projection/nome,sigla,geom/-/orderby/regiao
    http://127.0.0.1:8000/lim-unidade-federacao-a-list/nome,sigla,geom/filter/regiao/eq/Sul/-/orderby/regiao
    http://127.0.0.1:8000/lim-unidade-federacao-a-list/filter/regiao/eq/Sul/./collect/nome,sigla&geom/buffer/1.2/./orderby/regiao
    http://127.0.0.1:8000/lim-unidade-federacao-a-list/offset-limit/5&2/./collect/nome,sigla&geom/buffer/0.8"
    http://127.0.0.1:8000/lim-unidade-federacao-a-list/filter/regiao/eq/Sul/./count
    """