from typing import List, Tuple

from .database import DialectDatabase
from sqlalchemy import text
from sqlalchemy import ARRAY, BIGINT, CHAR, BigInteger, BINARY, Binary, BLOB, BOOLEAN, Boolean, CHAR, CLOB, DATE, Date, DATETIME, \
    DateTime, DateTime, DECIMAL, Enum, Column, FLOAT, Float, INT, INTEGER, Integer, JSON, LargeBinary, NCHAR, NUMERIC, \
    Numeric, NVARCHAR, PickleType, REAL, SMALLINT, SmallInteger, String, TEXT, Text, TIME, Time, TIMESTAMP, TypeDecorator, \
    Unicode, UnicodeText, VARBINARY, VARCHAR

# reference: https://www.postgresql.org/docs/9.1/functions-string.html
STRING_SQL_OPERATIONS = ["lower", "replace", "upper"]
SQLALCHEMY_TYPES_SQL_OPERATIONS = {
    ARRAY:          [],
    BIGINT:         [],
    CHAR:           [],
    BigInteger:     [],
    BINARY:         [],
    Binary:         [],
    BLOB:           [],
    BOOLEAN:        [],
    Boolean:        [],
    CLOB:           [],
    DATE:           [],
    Date:           [],
    DATETIME:       [],
    DateTime:       [],
    DECIMAL:        [],
    Enum:           [],
    Column:         [],
    FLOAT:          [],
    Float:          [],
    INT:            [],
    INTEGER:        [],
    Integer:        [],
    JSON:           [],
    LargeBinary:    [],
    NCHAR:          [],
    NUMERIC:        [],
    Numeric:        [],
    NVARCHAR:       [],
    PickleType:     [],
    REAL:           [],
    SMALLINT:       [],
    SmallInteger:   [],
    String:         STRING_SQL_OPERATIONS,
    TEXT:           [],
    Text:           [],
    TIME:           [],
    Time:           [],
    TIMESTAMP:      [],
    TypeDecorator:  [],
    Unicode:        [],
    UnicodeText:    [],
    VARBINARY:      [],
    VARCHAR:        []
}

class DialectDbPostgresql(DialectDatabase):
    def __init__(self, db, metadata_table, entity_class):
        super().__init__(db, metadata_table, entity_class)

    async def offset_limit(self, offset, limit, orderby= None, asc=None):
        colums_as_comma_name = self.columns_as_comma_list_str(self.metadata_table.columns)
        asc = 'desc' if asc == 'desc' else 'asc'
        orderbyasc = '' if orderby is None else f' order by {orderby} {asc} '  
        query = f'select {colums_as_comma_name} from {self.schema_table_name()} {orderbyasc}limit {limit} offset {offset}'
        return await self.db.fetch_all(query)
     
    async def fetch_all(self):
        query = self.metadata_table.select()
        rows = await self.db.fetch_all(query)
        return rows
    
    async def fetch_one(self, dic, all_column='*'):
        key_or_unique = next(key for key in dic.keys())
        query = f'select {all_column} from {self.schema_table_name()} where {key_or_unique} = :{key_or_unique}'
        row = await self.db.fetch_one(query=query, values=dic)
        return row

    async def fetch_all_as_json(self, tuple_attrib : Tuple[str] = None):
        query = self.basic_select(tuple_attrib)
        sql = f"select json_agg(t.*) from ({query}) as t;"
        print(sql)
        rows = await self.db.fetch_all(sql)
        return rows[0]['json_agg']

    async def fetch_one_as_json(self, id_dict):
        raise NotImplementedError("'fetch_one_as_json' must be implemented in subclasses")

    async def filter(self, a_filter):
        cols_as_enum = self.column_names_as_enum()
        query = f'select {cols_as_enum} from {self.schema_table_name()} where {a_filter}'
        print(query)
        rows = await self.db.fetch_all(query)
        return rows

    async def count(self):
        query = f'select count(*) from {self.schema_table_name()}'
        row = await self.db.fetch_one(query)
        return row
        
    async def order_by(self, str_attr_as_comma_list):
        cacls = self.columns_as_comma_list_str(self.metadata_table.columns)
        query = f'select {cacls} from {self.schema_table_name()} order by {str_attr_as_comma_list}'
        rows = await self.db.fetch_all(query)
        return rows
    
    async def projection(self, str_attribute_as_comma_list, orderby=None):
        order_by = '' if orderby is None else f' order by {orderby} '
        query = f'select {str_attribute_as_comma_list} from {self.schema_table_name()} {order_by}'
        rows = await self.db.fetch_all(query)
        return rows
    
    async def group_by_count(self, str_attr_as_comma_list, orderby=None):
        order_by = '' if orderby is None else f' order by {orderby} '
        query = f'select {str_attr_as_comma_list}, count(*) from {self.schema_table_name()} {order_by} group by {str_attr_as_comma_list}'
        rows = await self.db.fetch_all(query)
        return rows
    
    async def group_by_sum(self, str_attr_as_comma_list, attr_to_sum, orderby=None):
        order_by = '' if orderby is None else f' order by {orderby} '
        query = f'select {str_attr_as_comma_list}, sum({attr_to_sum}) from {self.schema_table_name()} {order_by} group by {str_attr_as_comma_list}'
        rows = await self.db.fetch_all(query)
        return rows

    # @staticmethod
    def get_sql_function(self, sql_type, function_name):
        return [operation for operation in SQLALCHEMY_TYPES_SQL_OPERATIONS[sql_type] if operation == function_name][0]

    async def delete_one(self, id_dict: dict):
        raise NotImplementedError("'delete' must be implemented in subclasses")

    async def update_one(self, id_dict: dict, field_value: dict):
        raise NotImplementedError("'update' must be implemented in subclasses")

    async def insert_one(self, field_value: dict):
        raise NotImplementedError("'insert' must be implemented in subclasses")
        query = f"INSERT INTO {self.schema_table_name()}({self.enum_column_names()}) VALUES ({self.enum_column_names_colon()})"
        values = field_value
        return await self.db.execute(query=query, values=values)