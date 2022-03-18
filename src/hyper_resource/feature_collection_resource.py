import io
import matplotlib.pyplot as plt
import time
from typing import List, Tuple, Optional, Dict
import geopandas as gpd
#gpd.read_postgis(sql, con=engine)

import cartopy.crs as ccrs
import shapely
from geopandas import GeoDataFrame
from shapely.geometry import Point, LineString, Polygon, MultiPolygon, MultiPoint, MultiLineString
from databases.backends.postgres import Record
from geoalchemy2 import Geometry, shape
from shapely import wkb

from settings import BASE_DIR, SOURCE_DIR
import sanic

from src.hyper_resource.common_resource import CONTENT_TYPE_HTML, CONTENT_TYPE_OCTET_STREAM, CONTENT_TYPE_GEOBUF, \
    CONTENT_TYPE_WKB, CONTENT_TYPE_VECTOR_TILE, CONTENT_TYPE_JSON, CONTENT_TYPE_GEOJSON, CONTENT_TYPE_GML, \
    CONTENT_TYPE_FLATGEOBUFFERS, CONTENT_TYPE_IMAGE_PNG
from src.hyper_resource.spatial_collection_resource import SpatialCollectionResource
from src.orm.action_type import ActionFunction
from src.orm.database_postgis import DialectDbPostgis
import json, os

from src.orm.dictionary_actions_abstract_collection import action_name
from src.orm.query_builder import QueryBuilder
from src.url_interpreter.interpreter import Interpreter
from src.url_interpreter.interpreter_error import PathError
from src.url_interpreter.interpreter_new import InterpreterNew

MIME_TYPE_JSONLD = "application/ld+json"
from geoalchemy2.shape import to_shape
class FeatureCollectionResource(SpatialCollectionResource):

    def __init__(self, request):
        super().__init__(request)
        self.extent = None

    def get_geom_attribute(self) -> str:
        return self.entity_class().geo_attribute_name()

    def get_geom_column(self) -> str:
        return self.dialect_DB().get_geom_column()

    def has_geom_attribute(self, enum_attribute_name: str) -> bool:
        return self.get_geom_attribute() in enum_attribute_name.split(',')

    def has_not_geom_attribute(self, enum_attribute_name: str) -> bool:
        return not self.has_geom_attribute(enum_attribute_name)

    def is_action_geom(self, attribute_name: str, action_names: List[str]) -> bool:
        a_type: type = self.entity_class().attribute_type_given(attribute_name)
        tp: object = self.dialect_DB().last_action_in_chain(a_type, action_names)
        return tp.answer in [Geometry]

    def is_not_action_geom(self,attribute_name: str, action_names: List[str]) -> bool:
        return not self.is_action_geom(attribute_name, action_names )

    def get_function_names(self) -> List[str]:
        if self.function_names is None:
            collection_func: List[str] = super(FeatureCollectionResource, self).get_function_names()
            self.function_names = collection_func + self.dialect_DB().get_spatial_function_names()
        return self.function_names

    def lookup_function_names(self) -> List[str]:
        return self.dialect_DB().get_spatial_lookup_function_names()

    def aggregate_function_names(self) -> List[str]:
        return self.dialect_DB().get_spatial_aggregate_function_names()


    async def get_extent(self, query: Optional[str] = None):
        if self.extent is None:
            self.extent = await self.dialect_DB().extent(query)
        return self.extent

    async def rows_as_dict(self, rows, geom_attribute_name: Optional[str] = None):
        if CONTENT_TYPE_HTML in self.accept_type():
            return await super(FeatureCollectionResource, self).rows_as_dict(rows)
        response_data = []
        geom_attribute = geom_attribute_name or self.get_geom_attribute()
        a_row: Record = rows[0]
        if geom_attribute not in list(a_row):
            return await super(FeatureCollectionResource, self).rows_as_dict(rows)
        feature_collection = { "type": "FeatureCollection",}
        try:

            for row in rows:
                row_dict = await self.dialect_DB().convert_row_to_dict(row)
                feature = {"type": "Feature"}
                geom_value = row_dict[geom_attribute]
                if type(geom_value) == str:
                    geom_value = wkb.loads(geom_value, hex=True)
                else:
                    geom_value = wkb.loads(geom_value)
                geometry = geom_value.__geo_interface__ #json.loads(row_dict[geom_attrubute])
                row_dict.pop(geom_attribute, None)
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
            if action_name in self.get_function_names():
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

    async def linestring_as_figure(self, geometries: List):
        #fig = plt.figure()
        # fig.set_visible(False)
        ax = plt.axes(projection=ccrs.PlateCarree(),  frameon=False)
        #ax = fig.add_axes([0, 0, 1, 1], projection=ccrs.PlateCarree(), frameon=False)
        ext: List[float] = await self.get_extent()
        ax.set_extent(ext, ccrs.PlateCarree())
        ax.patch.set_visible(False)
        ax.add_geometries(geometries, ccrs.PlateCarree(), facecolor='none',  edgecolor="black")
        b = io.BytesIO()
        plt.savefig(b, format='png')
        plt.close()
        return b.getvalue()

    async def polygon_as_figure(self, geometries: List):
        #fig = plt.figure()
        # fig.set_visible(False)
        #ax = fig.add_axes([0, 0, 1, 1], projection=ccrs.PlateCarree(), frameon=False)
        ax = plt.axes(projection=ccrs.PlateCarree(), frameon=False)
        #ax.set_extent([-74.018, -28.877, -33.742, 5.2672], ccrs.PlateCarree())
        ext: List[float] = await self.get_extent()
        ax.set_extent(ext, ccrs.PlateCarree())
        ax.add_geometries(geometries, ccrs.PlateCarree(), facecolor='#C8A2C8', alpha=0.5, edgecolor="black")
        b = io.BytesIO()
        plt.savefig(b, format='png')
        plt.close()
        return b.getvalue()

    async def point_as_figure(self, geometries: List):
        ax = plt.axes(projection=ccrs.PlateCarree(), frameon=False)
        ext: List[float] = await self.get_extent()
        ax.set_extent(ext, ccrs.PlateCarree())
        #ax.patch.set_visible(False)
        for point in geometries:
            plt.plot(point.x, point.y,  markersize=1, marker='o', color='b', transform=ccrs.PlateCarree())
        b = io.BytesIO()
        plt.savefig(b, format='png')
        plt.close()
        return b.getvalue()


    async def get_image_representation(self, query: str):
        a_query: str = self.dialect_DB().wkb_query(query)
        await self.get_extent(query)
        rows: List[Record] = await self.dialect_DB().fetch_all_by(a_query)
        geometries = [shapely.wkb.loads(row.get('st_asbinary')) for row in rows]
        if len(geometries) > 0 and (type(geometries[0]) == MultiPolygon or type(geometries[0]) == Polygon):
            res = await self.polygon_as_figure(geometries)
        elif len(geometries) > 0 and (type(geometries[0]) == LineString or type(geometries[0]) == MultiLineString):
            res = await self.linestring_as_figure(geometries)
        elif len(geometries) > 0 and (type(geometries[0]) == Point or type(geometries[0]) == MultiPoint):
            res = await self.point_as_figure(geometries)

        return sanic.response.raw(res, content_type=CONTENT_TYPE_IMAGE_PNG)

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

    async def get_wkb_representation(self, where: Optional[str] = None, order_by: Optional[str] = None) -> Record:
        rows = await self.dialect_DB().fetch_all_as_wkb(where=where, order_by=order_by)
        return sanic.response.raw(rows or [], content_type=CONTENT_TYPE_WKB)

    async def get_representation(self):
        accept = self.accept_type()
        if CONTENT_TYPE_HTML in accept:
            return await self.get_html_representation()
        elif (CONTENT_TYPE_GEOBUF in accept) or (CONTENT_TYPE_OCTET_STREAM in accept):
            return await self.get_geobuf_representation(prefix=self.protocol_host())
        elif (CONTENT_TYPE_FLATGEOBUFFERS in accept):
            return await self.get_flatgeobuf_representation(prefix=self.protocol_host())
        elif CONTENT_TYPE_IMAGE_PNG in self.accept_type():
            query: str = self.dialect_DB().query_build_by()
            return await self.get_image_representation(query)
        else:
            return await self.get_json_representation()

    async def get_mvt_representation_given_path(self, path):
        #application/vnd.mapbox-vector-tile
        params = path.split('&')
        rows = await self.dialect_DB().fetch_as_mvt_tiles(params)
        res = sanic.response.raw(rows or [], content_type= CONTENT_TYPE_VECTOR_TILE)
        return res

    async def add_collect_in_qb(self, qb, path):
        if not qb.has_geometry and self.has_geometry_in_collect(path):
            action: ActionFunction = await self.last_action_in_collect(path.split('/')[1:])
            qb.set_geom_attribute_name(action.name)
        qb.add_collect(await self.interpreter().translate_collect(path, self.protocol_host()))

    async def add_projection_in_qb(self, qb: QueryBuilder, path: str):
        path_ = path if path[0: len('projection/')] == 'projection/' else 'projection/' + path
        qb.has_geometry = self.has_geom_attribute(path_[len('projection/'):])
        qb.add_column(self.predicate_projection(path_))

    async def add_spatial_lookup_in_qb(self, qb: QueryBuilder, path: str):
        filter_path: str = f'{self.get_geom_attribute()}/{path}'
        where_clause: str = await self.interpreter(filter_path).translate_lookup()
        qb.add_where(where_clause)

    async def add_spatial_aggregate_in_qb(self, qb: QueryBuilder, path: str):
        aggregate: str = f'collect/{self.get_geom_attribute()}/{path}'
        qb.add_collect(await self.interpreter().translate_collect(aggregate, self.protocol_host()))


    def dict_qb_lookup_function(self) -> Dict:
        dic = {}
        for name in self.lookup_function_names():
            dic[name] = self.add_spatial_lookup_in_qb
        return dic

    def dict_qb_aggregate_function(self) -> Dict:
        dic = {}
        for name in self.aggregate_function_names():
            dic[name] = self.add_spatial_aggregate_in_qb
        return dic


    async def get_representation_given_path(self, path: str) -> str:
        try:
            paths: List[str] = self.normalize_path_as_list(path, '/*/')
            qb: QueryBuilder = QueryBuilder(dialect_db=self.dialect_DB(), entity_class=self.entity_class())
            qb.has_geometry = True
            for path in paths:
                await self.execute_qb_function(qb, path)
            qb.add_table_name(self.dialect_DB().schema_table_name())
            return await self.response_by_qb(qb)
        except PathError as err:
            return sanic.response.json(err.message, err.code)
        except (RuntimeError, TypeError, NameError) as err:
            return sanic.response.json("Error {0}". format(err))

    async def get_representation_given_path_new(self, path: str) -> str:
        try:

            paths: List[str] = self.normalize_path_as_list(path, '/*/')
            qb: QueryBuilder = QueryBuilder(self.dialect_DB())
            qb.has_geometry = True
            if len(paths) == 1:
                return await self.execute_method(paths[0])
            for path in paths:
                operation_name: str = self.operation_name_in_path(path)
                if operation_name == 'filter':
                    qb.add_where(await self.interpreter(path[6:]).translate_lookup())
                elif operation_name == 'collect':
                    if not qb.has_geometry and self.has_geometry_in_collect(path):
                            action: ActionFunction = await self.last_action_in_collect(path.split('/')[1:])
                            qb.set_geom_attribute_name(action.name)
                    qb.add_collect(await self.interpreter().translate_collect(path, self.protocol_host()))
                elif operation_name == 'projection':
                    path_ = path if path[0: len('projection/')] == 'projection/' else 'projection/' + path
                    qb.has_geometry = self.has_geom_attribute(path_[len('projection/'):])
                    qb.add_column(self.predicate_projection(path_))
                elif operation_name == 'groupby':
                    qb.add_group_by(await self.predicate_group_by(path))
                elif operation_name == 'count':
                    qb.add_count()
                elif operation_name == 'offsetlimit':
                    qb.add_offsetlimit(self.predicate_offsetlimit(path))
                elif operation_name == 'orderby':
                    qb.add_offsetlimit(self.predicate_order_by(path[8:]))
                elif operation_name == 'sum':
                    qb.add_sum(path)
                elif operation_name == 'avg':
                    count_ = self.predicate_avg(path)
            qb.add_table_name(self.dialect_DB().schema_table_name())
            return await self.response_by_qb(qb)
        except PathError as err:
            return sanic.response.json(err.message, err.code)
        except (RuntimeError, TypeError, NameError) as err:
            return sanic.response.json("Error {0}". format(err))

    async def get_representation_given_path_old(self, path: str):
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
            return sanic.response.json(rows_dict or [], content_type=CONTENT_TYPE_GEOJSON)
        if CONTENT_TYPE_WKB in self.accept_type():
            rows = await self.dialect_DB().fetch_all(list_attribute=attribute_names, where=where, order_by=order_by, prefix=prefix)
            rows_dict = await self.rows_as_dict(rows)
            return sanic.response.json(rows_dict or [], content_type=CONTENT_TYPE_GEOJSON)
        if CONTENT_TYPE_GEOBUF in self.accept_type():
            return await self.get_geobuf_representation(list_attribute=attribute_names, where=where, order_by=order_by, prefix=prefix)
        if CONTENT_TYPE_FLATGEOBUFFERS in self.accept_type():
            return await self.get_flatgeobuf_representation(list_attribute=attribute_names, where=where, order_by=order_by, prefix=prefix)
        if CONTENT_TYPE_IMAGE_PNG in self.accept_type():
            query: str = self.dialect_DB().query_build_by( where_predicate=where or '', enum_order_by=order_by or '')
            return await self.get_image_representation(query)

        rows = await self.dialect_DB().fetch_all(list_attribute=attribute_names, where=where, order_by=order_by,
                                                 prefix=prefix)
        rows_dict = await self.rows_as_dict(rows)
        return sanic.response.json(rows_dict or [])

    async def response_by_qb(self, qb: QueryBuilder):
        if qb.has_only_one_aggregate_math_function():
            return sanic.response.json(await qb.count())

        if CONTENT_TYPE_HTML in self.accept_type():
            return await self.get_html_representation()

        if (CONTENT_TYPE_JSON in self.accept_type()) or (CONTENT_TYPE_GEOJSON in self.accept_type()):
            rows = await self.dialect_DB().fetch_all_by(qb.query())
            if not qb.has_geometry:
                rows_dict = await super().rows_as_dict(rows)
                return sanic.response.json(rows_dict or [], content_type=CONTENT_TYPE_JSON)
            rows_dict = await self.rows_as_dict(rows, qb.geom_attribute_name)
            return sanic.response.json(rows_dict or [], content_type=CONTENT_TYPE_GEOJSON)
        if CONTENT_TYPE_GEOBUF in self.accept_type():
            geo_buf = await qb.fetch_all_as_geobuf()
            if geo_buf is None:
                return sanic.response.text('This query does not found any resource', status=404)
            return sanic.response.raw(geo_buf or None, content_type=CONTENT_TYPE_GEOBUF)
        if CONTENT_TYPE_FLATGEOBUFFERS in self.accept_type():
            flat_geo_buffer = await qb.fetch_all_as_flatgeobuffers()
            if flat_geo_buffer is None:
                return sanic.response.text('This query does not found any resource', status=404)
            return sanic.response.raw(flat_geo_buffer, content_type=CONTENT_TYPE_FLATGEOBUFFERS)
        if CONTENT_TYPE_IMAGE_PNG in self.accept_type():
            return await self.get_image_representation(qb.query())

        rows = await self.dialect_DB().fetch_all_by(qb.query())
        rows_dict = await self.rows_as_dict(rows)
        return sanic.response.json(rows_dict or [])

    async def response_by(self, query: str):
        if CONTENT_TYPE_HTML in self.accept_type():
            return await self.get_html_representation()
        if (CONTENT_TYPE_JSON in self.accept_type()) or (CONTENT_TYPE_GEOJSON in self.accept_type()):
            rows = await self.dialect_DB().fetch_all_by(query)
            rows_dict = await self.rows_as_dict(rows)
            return sanic.response.json(rows_dict or [], content_type=CONTENT_TYPE_GEOJSON)
        if CONTENT_TYPE_GEOBUF in self.accept_type():
            a_query: str = self.dialect_db.geobuf_query(query)
            rows = await self.dialect_DB().fetch_all_by(a_query)
            return sanic.response.raw(rows or [], content_type=CONTENT_TYPE_GEOBUF)
        if CONTENT_TYPE_FLATGEOBUFFERS in self.accept_type():
            a_query: str = self.dialect_db.flatgeobuf_query(query)
            rows = await self.dialect_DB().fetch_all_by(a_query)
            return sanic.response.raw(rows or [], content_type=CONTENT_TYPE_FLATGEOBUFFERS)
        if CONTENT_TYPE_IMAGE_PNG in self.accept_type():
            return self.get_image_representation(query)

        rows = await self.dialect_DB().fetch_all_by(query)
        rows_dict = await self.rows_as_dict(rows)
        return sanic.response.json(rows_dict or [])

    async def order_by(self, path: str) -> str:
        # order_by => orderby/name,gender&asc
        paths: List[str] = self.normalize_path(path).split('/')
        ordr: str = self.predicate_order_by(paths[-1])
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
        order_by: str = self.predicate_order_by(_order_by)
        return await self.response_request(attribute_names=attribute_names, where=where, order_by=order_by)

    async def last_action_in_collect(self, attrib_actions: List[str]):
        attribute_names: List[str] = attrib_actions[0].split("&")
        attribute_name: str = attribute_names[0] if len(attribute_names) == 1 else attribute_names[1]
        a_type: type = self.entity_class().attribute_type_given(attribute_name)
        return self.dialect_DB().last_action_in_chain(a_type, attrib_actions[1:])

    def is_geometry_type_last_action(self, action_names: List[str]) -> bool:
        tp = self.dialect_db.type_of_last_action_in_chain(self.entity_class().geo_attribute_type(), action_names)
        return tp == Geometry

    def has_geometry_in_collect(self, path: str) -> bool:
        words: List[str] = path.split('/')
        word: str = words[1].lower().strip()
        if '&' not in path: #collect/geom/transform/3005/area
            if self.get_geom_attribute() != word:
                return False
            else:
                return self.is_geometry_type_last_action(words[2:])
        enum_attribute: str = word.split('&')[0]
        if self.has_geom_attribute(enum_attribute):
            return True
        return self.is_geometry_type_last_action(words[2:])

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
    http://127.0.0.1:8000/lim-unidade-federacao-a-list/extent
    select st_extent(geom) from bcim.lim_unidade_federacao_a
    
    http://127.0.0.1:8000/lim-unidade-federacao-a-list/extent/*/groupby/sigla
    select sigla, st_extent(geom) from bcim.lim_unidade_federacao_a group by sigla
    
    http://127.0.0.1:8000/lim-unidade-federacao-a-list/filter/regiao/eq/Sul/*/extent/*/groupby/sigla
    select sigla, st_extent(geom) from bcim.lim_unidade_federacao_a where regiao = 'Sul' group by sigla
    
    UNION
    http://127.0.0.1:8000/lim-unidade-federacao-a-list/filter/regiao/eq/Sul/*/union/*/groupby/regiao
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