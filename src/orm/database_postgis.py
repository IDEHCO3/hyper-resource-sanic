from typing import List

from geoalchemy2 import functions

from src.orm.database_postgresql import DialectDbPostgresql

class DialectDbPostgis(DialectDbPostgresql):
    def __init__(self, db, metadata_table, entity_class):
        super().__init__(db, metadata_table, entity_class)

    async def fetch_all_as_json(self):
        query = self.basic_select()
        sql = f"select json_build_object('type', 'FeatureCollection','features', json_agg(ST_AsGeoJSON(t.*)::json)) from ( {query} ) as t;"
        print(sql)
        rows = await self.db.fetch_all(sql)
        return rows[0]['json_build_object']

    def get_columns_sql(self) -> List[str]:
        full_columns_names = []
        for col in self.metadata_table.columns:
            if hasattr(col.type, "geometry_type"):
                full_columns_names.append(
                    "ST_AsGeoJSON(" + self.metadata_table.fullname + "." + col.name + ") as " + col.name)
            else:
                full_columns_names.append(self.metadata_table.fullname + "." + col.name)
        return full_columns_names

    def get_basic_select(self) -> str:
        query = "SELECT "
        full_columns_names = self.get_columns_sql()
        query += ",".join(full_columns_names)
        query += " FROM " + self.metadata_table.fullname
        return query

    # @staticmethod
    def get_sql_function(self, sql_type, function_name):
        try:
            return [tuple_func[0] for tuple_func in functions._FUNCTIONS if tuple_func[0].lower() == "st_" + function_name][0]
        except IndexError:
            return super().get_sql_function(sql_type, function_name)
