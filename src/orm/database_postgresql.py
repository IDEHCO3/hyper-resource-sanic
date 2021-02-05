from datetime import date
from typing import List, Tuple, Optional, Any

from .database import DialectDatabase
from sqlalchemy import text
from sqlalchemy import ARRAY, BIGINT, CHAR, BigInteger, BINARY, BLOB, BOOLEAN, Boolean, CHAR, CLOB, DATE, Date, DATETIME, \
    DateTime, DateTime, DECIMAL, Enum, Column, FLOAT, Float, INT, INTEGER, Integer, JSON, LargeBinary, NCHAR, NUMERIC, \
    Numeric, NVARCHAR, PickleType, REAL, SMALLINT, SmallInteger, String, TEXT, Text, TIME, Time, TIMESTAMP, TypeDecorator, \
    Unicode, UnicodeText, VARBINARY, VARCHAR

# reference: https://www.postgresql.org/docs/9.1/functions-string.html
from .models import AlchemyBase

STRING_SQL_OPERATIONS = ["lower", "replace", "upper"]
SQLALCHEMY_TYPES_SQL_OPERATIONS = {
    ARRAY:          [],
    BIGINT:         [],
    CHAR:           [],
    BigInteger:     [],
    BINARY:         [],
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
    async def next_val(self, schema_sequence: str = None) -> int:
        sequence = schema_sequence if schema_sequence is not None else self.schema_sequence()
        row = await self.db.fetch_one(f"select nextval('{sequence}')")
        return row['nextval']
    async def fetch_one(self, dic: dict, all_column: str='*'):
        key_or_unique = next(key for key in dic.keys())
        query = f'select {all_column} from {self.schema_table_name()} where {key_or_unique} = :{key_or_unique}'
        row = await self.db.fetch_one(query=query, values=dic)
        return row
    async def fetch_all_as_json(self, tuple_attrib : Tuple[str] = None, a_query: str = None):
        query = self.basic_select(tuple_attrib) if a_query is None else a_query
        sql = f"select json_agg(t.*) from ({query}) as t;"
        print(sql)
        rows = await self.db.fetch_all(sql)
        return rows[0]['json_agg']

    def function_db(self) -> str:
        return 'row_to_json'

    async def fetch_one_as_json(self, pk):
        query = self.basic_select_by_id(pk)
        sql = f"select {self.function_db()}(t.*) from ({query}) as t;"
        print(sql)
        rows = await self.db.fetch_one(sql)
        return rows if rows is None else rows[self.function_db()]

    async def find_one_as_model(self, pk: int , all_column: str ='*' ) -> Optional[AlchemyBase]:

        query = self.basic_select_by_id(pk)
        sql = f"select (t.*) from ({query}) as t;"
        print(sql)
        rows = await self.db.fetch_one(sql)
        return self.entity_class(**rows)
    async def filter(self, a_filter):
        cols_as_enum = self.enum_column_names()
        query = f'select {cols_as_enum} from {self.schema_table_name()} where {a_filter}'
        print(query)
        rows = await self.db.fetch_all(query)
        return rows
    async def filter_as_json(self, a_filter, e_column_names : str = None):
        cols_as_enum = self.enum_column_names() if e_column_names is None else e_column_names
        query = f'select {cols_as_enum} from {self.schema_table_name()} where {a_filter}'
        print(query)
        rows = await self.fetch_all_as_json(None, query)
        return rows
    async def count(self) -> int:
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
    async def delete_one(self, value: int):
        return await self.delete({self.entity_class.primary_key() : value})
    async def delete(self, id_or_dict):
        id_dict = id_or_dict if type(id_or_dict) == dict else {self.entity_class.primary_key() : id_or_dict}
        tuple_key_value = id_dict.popitem()
        col_eq_value = tuple_key_value[0] + ' = ' + str(tuple_key_value[1])
        query = f"DELETE FROM {self.schema_table_name()} WHERE {col_eq_value}"
        res = await self.db.execute(query=query)
        return res
    async def update_one(self, a_value: int, attribute_value: dict):
        return await self.update_raw({self.entity_class.primary_key() : a_value}, attribute_value)
    async def update(self, id_dict: dict, column_value: dict):
        tuple_key_value = id_dict.popitem()
        col_eq_value = tuple_key_value[0] + ' = ' + str(tuple_key_value[1])
        enum_col_eq_value = self.enum_equal_column_names(column_value)
        query = f"UPDATE {self.schema_table_name()} SET {enum_col_eq_value} WHERE {col_eq_value} "
        res = await self.db.execute(query=query, values=column_value)
        return res
    async def update_raw(self, id_or_dict, attribute_value: dict):
        id_dict = id_or_dict if type(id_or_dict) == dict else {self.entity_class.primary_key() : id_or_dict}
        list_attr_col_type = self.list_attribute_column_type_given(attribute_value.keys())
        dict_column_value = self.convert_all_to_db(list_attr_col_type, attribute_value, True)
        return await self.update(id_dict, dict_column_value)
    async def insert_one(self, column_value: dict):
        column_names = column_value.keys()
        pk_name = self.entity_class.primary_key()
        if pk_name not in column_names:
            pk_value = await self.next_val()
            column_value[pk_name] = pk_value
        query = f"INSERT INTO {self.schema_table_name()}({self.enum_column_names(column_names)}) VALUES ({self.enum_colon_column_names(column_names)})"
        await self.db.execute(query=query, values=column_value)
        return pk_value
    async def insert_one_raw(self, attribute_value: dict) -> int:
        list_attr_col_type = self.list_attribute_column_type_given(attribute_value.keys())
        dict_column_value = self.convert_all_to_db(list_attr_col_type, attribute_value)
        return await self.insert_one(dict_column_value)
    def convert_to_db(self, a_type: str, val, is_update: bool= False) -> Any:
        if a_type in ('VARCHAR', 'CHAR'):
            return f"'{val}'" if is_update else val
        if a_type in ('INTEGER', 'INT', 'Integer'):
            return int(val)
        if a_type in ('DATE'):
            return date.fromisoformat(val) #iso => yyyy-mm-dd
        return val
    def convert_all_to_db(self, attribute_column_type: List[tuple], attribute_value: dict, is_update : bool = False) -> dict:
        column_value = {}
        for attr, col,typ  in attribute_column_type:
            column_value[col] = self.convert_to_db(typ, attribute_value[attr], is_update)
        return column_value