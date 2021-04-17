import json
from typing import List, Tuple

from geoalchemy2 import functions
from sqlalchemy.orm import InstrumentedAttribute

from src.orm.database_postgresql import DialectDbPostgresql

class DialectDbPostgis(DialectDbPostgresql):
    def __init__(self, db, metadata_table, entity_class):
        super().__init__(db, metadata_table, entity_class)

    def has_geom_column(self, tuple_attrib) -> bool:
        return self.entity_class.geo_column_name()  in tuple_attrib

    def has_not_geom_column(self,tuple_attrib) -> bool:
        return not self.has_geom_column(tuple_attrib)

    async def fetch_all_as_json(self, tuple_attrib : Tuple[str] = None,  a_query: str = None, prefix_col_val: str=None):
        if (tuple_attrib is not None) and (self.has_not_geom_column(tuple_attrib) ):
            return await super().fetch_all_as_json(tuple_attrib)
        query = self.basic_select(tuple_attrib) if a_query is None else a_query
        sql = f"select json_build_object('type', 'FeatureCollection','features', json_agg(ST_AsGeoJSON(t.*)::json)) from ( {query} ) as t;"
        print(sql)
        rows = await self.db.fetch_all(sql)
        return rows[0]['json_build_object']

    async def fetch_one_as_json(self, pk, tuple_attrib : Tuple[str] = None,prefix_col_val: str=None):
        query = self.basic_select_by_id(pk, tuple_attrib, prefix_col_val)
        func_name = f'ST_AsEWKB({self.get_geom_column()})'
        query.replace(func_name, self.get_geom_column())
        sql = f"select {self.function_db()}(t.*) from ({query}) as t;"
        print(sql)
        rows = await self.db.fetch_one(sql)
        return rows if rows is None else rows[self.function_db()]

    async def fetch_all_as_geobuf(self, tuple_attrib : Tuple[str] = None,  a_query: str = None, prefix_col_val: str=None ):
        sub_query = self.basic_select(tuple_attrib, prefix_col_val) if a_query is None else a_query
        geom = self.entity_class.geo_column_name()
        query = f"SELECT  ST_AsGeobuf(q, '{geom}') FROM ({sub_query}) AS q"
        rows = await self.db.fetch_all(query)
        return rows[0]['st_asgeobuf']

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

    def get_columns_sql(self) -> List[str]:
        full_columns_names = []
        for col in self.metadata_table.columns:
            if hasattr(col.type, "geometry_type"):
                full_columns_names.append(
                    "ST_AsGeoJSON(" + self.metadata_table.fullname + "." + col.name + ") as " + col.name)
            else:
                full_columns_names.append(self.metadata_table.fullname + "." + col.name)
        return full_columns_names

    def alias_column(self, inst_attr: InstrumentedAttribute, prefix_col: str = None):
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
