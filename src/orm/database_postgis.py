import json
from typing import List, Tuple, Dict, Optional
from databases.backends.postgres import Record
from shapely.errors import WKBReadingError
from sqlalchemy.orm import InstrumentedAttribute
from geoalchemy2 import functions, Geometry
from src.aiohttp_client import ClientIOHTTP
from src.hyper_resource.common_resource import CONTENT_TYPE_GEOJSON, CONTENT_TYPE_WKB, CONTENT_TYPE_JSON
from src.orm.database_postgresql import DialectDbPostgresql
from src.orm.dictionary_actions import ActionFunction
from src.orm.dictionary_actions_postgis import dic_spatial_lookup_action, dic_action, dic_spatial_aggregate_action
from shapely import wkb

class DialectDbPostgis(DialectDbPostgresql):
    def __init__(self, db, metadata_table, entity_class):
        super().__init__(db, metadata_table, entity_class)
        self.srid = 4674

    def get_spatial_lookup_function_names(self) -> List[str]:
        return list(dic_spatial_lookup_action.keys())

    def get_spatial_aggregate_function_names(self) -> List[str]:
        return list(dic_spatial_aggregate_action.keys())

    def get_spatial_function_names(self) -> List[str]:
        return self.get_spatial_lookup_function_names() + self.get_spatial_aggregate_function_names()

    def has_geom_column(self, tuple_attrib) -> bool:
        return self.entity_class.geo_column_name()  in tuple_attrib

    def has_not_geom_column(self,tuple_attrib) -> bool:
        return not self.has_geom_column(tuple_attrib)

    async def fetch_all_as_json(self, tuple_attrib : Tuple[str] = None,  a_query: str = None, prefix_col_val: str=None):
        if (tuple_attrib is not None) and (self.has_not_geom_column(tuple_attrib) ):
            return await super().fetch_all_as_json(tuple_attrib)
        query = self.basic_select(tuple_attrib) if a_query is None else a_query
        geom = self.entity_class.geo_column_name()
        query = query.replace(f'ST_AsEWKB({geom})', geom)
        sql = f"select json_build_object('type', 'FeatureCollection','features', json_agg(ST_AsGeoJSON(t.*)::json)) from ( {query} ) as t;"
        print(sql)
        rows = await self.db.fetch_all(sql)
        result = rows[0]['json_build_object']
        if len(result) == 49: #'{"type" : "FeatureCollection", "features" : null}'
            return None
        return result

    async def fetch_one_as_json(self, pk, tuple_attrib : Tuple[str] = None,prefix_col_val: str=None):
        query = self.basic_select_by_id(pk, tuple_attrib, prefix_col_val)
        func_name = f'ST_AsEWKB({self.get_geom_column()})'
        query = query.replace(func_name, self.get_geom_column())
        sql = f"select {self.function_db()}(t.*) from ({query}) as t;"
        print(sql)
        rows = await self.db.fetch_one(sql)
        return rows if rows is None else rows[self.function_db()]

    def wkb_query(self, sub_query: str) -> str:
        geom: str = self.get_geom_column()
        return f"SELECT ST_AsBinary({geom}) FROM ({sub_query}) AS q"

    def geobuf_query(self, sub_query: str) -> str:
        geom: str = self.get_geom_column()
        return f"SELECT  ST_AsGeobuf(q, '{geom}') FROM ({sub_query}) AS q"

    async def fetch_all_as_geobuf(self, list_attribute: List[str] = None,  where: Optional[str] = None, order_by: Optional[str] = None, prefix_col_val: str = None):
        sub_query = self.basic_select(list_attrib=list_attribute, prefix_col_val=prefix_col_val)  # self.metadata_table.select()
        sub_query += where or ''
        sub_query += order_by or ''
        geom = self.entity_class.geo_column_name()
        if list_attribute == None:
            sub_query = sub_query.replace(f'ST_AsEWKB({geom})', geom)
        query: str = self.geobuf_query(sub_query) #f"SELECT  ST_AsGeobuf(q, '{geom}') FROM ({sub_query}) AS q"
        rows = await self.db.fetch_all(query)
        return rows[0]['st_asgeobuf']

    def extent_query(self, sub_query: str) -> str:
        return f"SELECT ST_Extent({self.get_geom_column()}) FROM ({sub_query or self.schema_table_name()}) AS q"

    async def extent(self, sub_query: str) -> List[float]:
        query: str = self.extent_query(sub_query)
        rows: List[Record] = await self.db.fetch_all(query)
        s: str = rows[0]['st_extent']
        coords = s.removeprefix('BOX(').removesuffix(')').split(',')[0].split(' ') + \
                 s.removeprefix('BOX(').removesuffix(')').split(',')[1].split(' ')
        return [float(coord) for coord in coords]

    def flatgeobuf_query(self, sub_query: str) -> str:
        return f"SELECT ST_AsFlatGeobuf(q.*) FROM ({sub_query}) AS q"

    def query_wkb(self, geom_expression: Optional[str] = None,
                               table_name_expression: Optional[str] = None,
                               where: Optional[str] = None,
                               order_by: Optional[str] = None) -> str:

        geom_expr: str = f'ST_AsBinary({geom_expression or self.entity_class.geo_column_name()})'
        table_name_expr: str = table_name_expression or self.schema_table_name()
        sub_query = f'select {geom_expr} from {table_name_expr} '
        sub_query += where or ''
        sub_query += order_by or ''
        return sub_query

    async def fetch_all_as_wkb(self, geom_expression: Optional[str] = None,
                               table_name_expression: Optional[str] = None,
                               where: Optional[str] = None,
                               order_by: Optional[str] = None):
        query: str = self.query_wkb(geom_expression,table_name_expression, where, order_by )
        rows = await self.db.fetch_all(query)
        return [row['st_asbinary'] for row in rows]

    async def fetch_all_as_flatgeobuf(self,  list_attribute: List[str] = None,  where: Optional[str] = None, order_by: Optional[str] = None, prefix_col_val: str = None):
        sub_query: str = self.basic_select(list_attrib=list_attribute,
                                      prefix_col_val=prefix_col_val)  # self.metadata_table.select()
        sub_query += where or ''
        sub_query += order_by or ''
        geom = self.entity_class.geo_column_name()
        if list_attribute == None:
            sub_query = sub_query.replace(f'ST_AsEWKB({geom})', geom)
        query: str = self.flatgeobuf_query(sub_query) #f"SELECT ST_AsFlatGeobuf(q.*) FROM ({sub_query}) AS q"
        rows = await self.db.fetch_all(query)
        return rows[0]['st_asflatgeobuf']

    async def fetch_as_mvt_tiles(self, zoom, x, y):
        """
        Custom view to serve Mapbox Vector Tiles for the custom polygon model.
        """
        query = f"SELECT ST_AsMVT(tile) FROM (SELECT id, description, ST_AsMVTGeom(geometry, TileBBox({zoom}, {x}, {y}, 4326)) FROM {self.schema_table_name()}) AS tile"
        rows = await self.db.fetch_all(query)
        return rows[0]['st_asmvt']

    def function_db(self) -> str:
        return 'st_asgeojson'

    def get_geom_column(self) -> str:
        for column in self.metadata_table.columns:
            if hasattr(column.type, "geometry_type"):
                return str(column.name)
        #self.entity_class.geo_column_name()

    def get_geom_attribute(self) -> Optional[str]:
        return self.entity_class.geo_attribute_name

    def get_columns_sql(self) -> List[str]:
        full_columns_names = []
        for col in self.metadata_table.columns:
            if hasattr(col.type, "geometry_type"):
                full_columns_names.append(
                    "ST_AsGeoJSON(" + self.metadata_table.fullname + "." + col.name + ") as " + col.name)
            else:
                full_columns_names.append(self.metadata_table.fullname + "." + col.name)
        return full_columns_names

    def alias_column_old(self, inst_attr: InstrumentedAttribute, prefix_col: str = None):
        if self.entity_class.is_relationship_fk_attribute(inst_attr)  and prefix_col is not None:
            col_name = self.entity_class.column_name_or_None(inst_attr) #inst_attr.prop._user_defined_foreign_keys[0].name
            model_class = self.entity_class.class_given_relationship_fk(inst_attr)
            return f"CASE WHEN {col_name} is not null THEN '{prefix_col}{model_class.router_list()}/' || {col_name} ELSE null  END AS {self.entity_class.attribute_name_given(inst_attr)}"
        elif self.entity_class.is_primary_key(inst_attr):
            pref = f'{prefix_col}{self.entity_class.router_list()}/' if prefix_col is not None  else ''
            col_name = self.entity_class.column_name_or_None(inst_attr)
            attr_name = self.entity_class.attribute_name_given(inst_attr)
            return f"'{pref}' || {col_name} as {attr_name}"
        elif self.entity_class.is_relationship_attribute(inst_attr):
            return None
        elif self.entity_class.is_geometry_attribute(inst_attr):
            col_name = self.entity_class.column_name_or_None(inst_attr)
            attr_name = self.entity_class.attribute_name_given(inst_attr)
            return f"ST_AsEWKB({col_name}) as {attr_name}"
        else:
            col_name = self.entity_class.column_name_or_None(inst_attr)
            attr_name = self.entity_class.attribute_name_given(inst_attr)
            return f'{col_name} as {attr_name}'

    # @staticmethod
    def get_sql_function(self, sql_type, function_name):
        try:
            return [tuple_func[0] for tuple_func in functions._FUNCTIONS if tuple_func[0].lower() == "st_" + function_name][0]
        except IndexError:
            return super().get_sql_function(sql_type, function_name)

    def function_as_sql(self, function_name: str, action_function: ActionFunction ) -> str:
        geom = self.entity_class.geo_column_name()
        if action_function.count_params() > 1:
            params = action_function.paramActions[1:]
        params_as_enum = params
        return f'{action_function.name}({geom},{params_as_enum})'

    async def execute_spatial_function(self, function_name: str, geometry: Geometry, content_type:str = CONTENT_TYPE_GEOJSON):
        action_function = self.dict_action()[function_name]
        query = f'select * from {self.schema_table_name()} where ~({self.get_geom_column()},{geometry})'
        if content_type == CONTENT_TYPE_GEOJSON:
            return await self.fetch_all_as_json('*', query, )
        return []

    def dict_action(self) -> Dict[type, ActionFunction]:
        d = {Geometry: dic_action}
        return d

    def action(self, typeof: object, action_name: str) -> Optional[ActionFunction]:
        if typeof in self.dict_action() and (action_name in self.dict_action()[typeof]):
            d = self.dict_action()[typeof]
            return d[action_name]
        return None

    def value_seems_wkt(self, well_know_text: str):
        wkts = ['point', 'Linestring', 'polygon', 'multipoint', 'multilinestring', 'muiltpolygon', 'geometrycollection']
        value_from_path = well_know_text[0:20].lower()
        for wkt in wkts:
            if value_from_path.startswith(wkt):
                return True
        return False

    def get_geometry_geojson(self, json_str: str) -> str:
        jgeo = json.loads(json_str)
        if (jgeo.get("type") and jgeo["type"].lower() == 'feature'):
            return jgeo["geometry"]
        return json.dumps(json_str)

    def make_geometrycollection_from_featurecollection(self, feature_collection: Dict):
        geoms = []
        #features = json.loads(feature_collection)
        coordinates = []
        for feature in feature_collection['features']:
            feature_geom = json.dumps(feature['geometry'])
            coordinates.append(feature_geom)

        return {"type": "GeometryCollection", "geometries": [{"type": "MultiPolygon", "coordinates": coordinates}]}

    async def convert_geometry_from_request(self, url: str, accept: str = CONTENT_TYPE_WKB) -> str:
        headers = {'accept': accept}
        async with ClientIOHTTP().session.get(url, headers=headers) as resp:
            if resp.content_type == CONTENT_TYPE_WKB:
                geom = await resp.read()
                #geom_encoded = wkb.loads(geom.decode(), hex=True)
                #return wkb.loads(geom.decode(), hex=True)
                #return f"ST_SetSRID('{geom_encoded}'::geometry, {self.srid})"
                try:
                    geom_encoded = wkb.loads(geom)
                except (WKBReadingError, UnicodeDecodeError) as error:
                    geom_encoded = wkb.loads(geom.decode(), hex=True)
                return f"ST_SetSRID('{geom_encoded}'::geometry, {self.srid})"
            elif resp.content_type in [CONTENT_TYPE_GEOJSON, CONTENT_TYPE_JSON]:
                geometry = await resp.json()
                if 'geometry' in geometry:
                    geometry = geometry['geometry']
                elif geometry['type'] == 'FeatureCollection':
                    geometry = self.make_geometrycollection_from_featurecollection(geometry)
                return f"ST_GeomFromGeoJSON('{json.dumps(geometry)}')"

    async def convert_to_db_geometry(self, value_as_str: str) -> str:
        try:
            if self.value_seems_json(value_as_str):
                geometry = self.get_geometry_geojson(value_as_str)
                return f'ST_GeomFromGeoJSON({geometry})'
            elif self.value_seems_wkt(value_as_str):
                return f'ST_GeomFromText({value_as_str})'
            elif self.value_has_url(value_as_str):
                return await self.convert_geometry_from_request(value_as_str)
            else:
                return value_as_str

        except (ValueError, ConnectionError) as err:
            print('Error: '.format(err))