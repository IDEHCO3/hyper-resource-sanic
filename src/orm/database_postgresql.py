import datetime
from datetime import date
from typing import List, Tuple, Optional, Any, Dict
import copy
import time

from databases.backends.postgres import Record
from sqlalchemy.orm.attributes import InstrumentedAttribute

from .database import DialectDatabase
from sqlalchemy import text
from sqlalchemy import ARRAY, BIGINT, CHAR, BigInteger, BINARY, BLOB, BOOLEAN, Boolean, CHAR, CLOB, DATE, Date, DATETIME, \
    DateTime, DateTime, DECIMAL, Enum, Column, FLOAT, Float, INT, INTEGER, Integer, JSON, LargeBinary, NCHAR, NUMERIC, \
    Numeric, NVARCHAR, PickleType, REAL, SMALLINT, SmallInteger, String, TEXT, Text, TIME, Time, TIMESTAMP, TypeDecorator, \
    Unicode, UnicodeText, VARBINARY, VARCHAR

# reference: https://www.postgresql.org/docs/9.1/functions-string.html
from .dictionary_actions import ActionFunction
from .models import AlchemyBase
from src.hyper_resource.basic_route import BasicRoute
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

    async def offset_limit(self, offset: int, limit: int, orderby= None, asc=None, format_row = None ):
        offset = offset - 1
        colums_as_comma_name = self.columns_as_enum_column_names(self.metadata_table.columns)
        asc = 'desc' if asc == 'desc' else 'asc'
        orderbyasc = '' if orderby is None else f' order by {orderby} {asc} '
        query = f'select {colums_as_comma_name} from {self.schema_table_name()} {orderbyasc} limit {limit} offset {offset}'
        if format_row is None:
            rows = await self.db.fetch_all(query)
        else:
            rows = await self.fetch_all_as_json(None, query)
        return rows
    async def fetch_all_by(self, query: str):
        return await self.db.fetch_all(query)

    async def fetch_all(self, list_attribute: Optional[List] = None, where: Optional[str] = None, order_by: Optional[str] = None, prefix: Optional[str] = None):
        query = self.basic_select(list_attrib=list_attribute, prefix_col_val=prefix) #self.metadata_table.select()
        query += where or ''
        query += order_by or ''
        start = time.time()
        print(f"time: {start} start query: {query}")
        rows = await self.db.fetch_all(query)
        end = time.time()
        print(f"time: {end - start} end query: {query}")
        return rows

    async def next_val(self, schema_sequence: str = None) -> int:
        sequence = schema_sequence if schema_sequence is not None else self.schema_sequence()
        row = await self.db.fetch_one(f"select nextval('{sequence}')")
        return row['nextval']

    def alias_column(self, inst_attr: InstrumentedAttribute, prefix_col: str = None):
        if self.entity_class.is_relationship_fk_attribute(inst_attr)  and prefix_col is not None:
            col_name = self.entity_class.column_name_or_None(inst_attr) #inst_attr.prop._user_defined_foreign_keys[0].name
            model_class = self.entity_class.class_given_relationship_fk(inst_attr)
            return f"CASE WHEN {col_name} is not null THEN '{prefix_col}{model_class.router_list()}/' || {col_name} ELSE null  END AS {self.entity_class.attribute_name_given(inst_attr)}"
        elif self.entity_class.is_primary_key(inst_attr):
            pref = f'{prefix_col}{self.entity_class.router_list()}/' if prefix_col is not None  else ''
            col_name = self.entity_class.column_name_or_None(inst_attr)
            attr_name = self.entity_class.attribute_name_given(inst_attr)
            return f"{col_name} as {attr_name}" if pref == '' else f"'{pref}' || {col_name} as {attr_name}"
        elif self.entity_class.is_relationship_attribute(inst_attr):
            return None
        else:
            col_name = self.entity_class.column_name_or_None(inst_attr)
            attr_name = self.entity_class.attribute_name_given(inst_attr)
            return f'{col_name} as {attr_name}'

    def column_names_alias(self, attrib_names: Optional[List[str]] = None, prefix_col_val: str = None) -> str:
        attr_names = attrib_names if attrib_names is not None else self.attribute_names()
        attributes = [self.entity_class.__dict__[name] for name in attr_names]
        list_alias = []
        for att in attributes:
            alias = self.alias_column(att, prefix_col_val)
            if alias is not None:
                list_alias.append(alias)
        return ','.join(list_alias)

    def enum_column_names_alias_attribute_given(self, attributes: List[InstrumentedAttribute], prefix_col_val: str = None) -> str:
        list_alias = []
        for att in attributes:
            alias = self.alias_column(att, prefix_col_val)
            if alias is not None:
                list_alias.append(alias)
        return ','.join(list_alias)

    async def fetch_one(self, dic: dict, all_column: str=None, prefix_col_val: str=None ):
        key_or_unique = next(key for key in dic.keys())
        query = self.basic_select(all_column, prefix_col_val)
        query = f"{query} where {key_or_unique} = :{key_or_unique}"
        row = await self.db.fetch_one(query=query, values=dic)
        return row


    def query_build_by(self, enum_fields: str = '', enum_schema_table: str ='', where_predicate: str ='', enum_order_by:str = '', offsetlimit: str = '') -> str:
        predicate_field: str        = self.enum_column_names() if enum_fields == '' else enum_fields
        predicate_schema_table: str = self.schema_table_name() if enum_schema_table == '' else enum_schema_table
        predicate_join: str         = '' if where_predicate == '' else f'{where_predicate} '
        predicate_orderby: str      = '' if enum_order_by == '' else f'order by {enum_order_by}'
        predicate_offset: str       = '' if offsetlimit == '' else offsetlimit
        return f'select {predicate_field} from {predicate_schema_table} {predicate_join} {predicate_orderby} {predicate_offset}'

    def basic_select(self, list_attrib: List[str] = None, prefix_col_val: str = None ) -> str:

        enum_col_names = self.column_names_alias(list_attrib, prefix_col_val)
        query = f'select {enum_col_names} from {self.schema_table_name()}'
        return query

    def basic_select_one_by_key_value(self, key_value: Tuple, tuple_attrib: Tuple[str] = None, prefix_col_val: str=None):
        tp_attribute = self.db_type_name_given_attribute(key_value[0])
        value_converted = self.convert_to_db(tp_attribute, key_value[1], True)
        query = self.basic_select(tuple_attrib, prefix_col_val)
        query = f'{query} where {key_value[0]} = {value_converted}'
        return query

    def basic_select_by_id(self, pk, tuple_attrib: Tuple[str] = None, prefix_col_val: str=None):
        query = self.basic_select(tuple_attrib, prefix_col_val)
        pk_value = pk
        query = f'{query} where {self.primary_key()}={pk_value}'
        return query
    async def fetch_all_as_json(self, tuple_attrib : Tuple[str] = None, a_query: str = None, prefix_col_val: str=None):
        query = self.basic_select(tuple_attrib, prefix_col_val) if a_query is None else a_query
        sql = f"select json_agg(t.*) from ({query}) as t;"
        print(sql)
        rows = await self.db.fetch_all(sql)
        return rows[0]['json_agg']
    def function_db(self) -> str:
        return 'row_to_json'
    async def fetch_one_as_json(self, pk, tuple_attrib : Tuple[str] = None,prefix_col_val: str=None):
        query = self.basic_select_by_id(pk, tuple_attrib, prefix_col_val)
        sql = f"select {self.function_db()}(t.*) from ({query}) as t;"
        print(sql)
        rows = await self.db.fetch_one(sql)
        return rows if rows is None else rows[self.function_db()]

    async def fetch_all_model(self, tuple_attrib : Tuple[str] = None, prefix_col_val: str=None):
        query = self.basic_select(tuple_attrib, prefix_col_val)
        print(query)
        start = time.time()
        print(f"time: {start} start rows in python")
        rows = await self.db.fetch_all(query)
        res = [ self.entity_class(**row) for row in rows]
        end = time.time()
        print(f"time: {end - start} end rows in python")
        return res

    async def fetch_one_model(self, pk_or_key_value_tuple, key_value: Dict= None, tuple_attrib : Tuple[str] = None, prefix_col_val: str=None) -> Optional[AlchemyBase]:

        if type(pk_or_key_value_tuple) == int :
            sql = self.basic_select_by_id(pk_or_key_value_tuple, tuple_attrib, prefix_col_val)
        else:
            sql = self.basic_select_one_by_key_value(pk_or_key_value_tuple, tuple_attrib, prefix_col_val)
        print(sql)
        row = await self.db.fetch_one(sql)
        if row:
            return self.entity_class(**row)
        return None

    async def filter(self, a_filter, e_column_names : str = None, prefix_col_val: str=None):
        query = self.basic_select(e_column_names, prefix_col_val)
        query = f'{query} where {a_filter}'
        print(query)
        rows = await self.db.fetch_all(query)
        return rows

    async def filter_as_json(self, a_filter, e_column_names : str = None, prefix_col_val: str=None):
        query = self.basic_select(e_column_names, prefix_col_val)
        query = f'{query} where {a_filter}'
        print(query)
        rows = await self.fetch_all_as_json(None, query)
        return rows

    async def count(self, column_name: str = None, where: str = None) -> int:
        asterisk: str = column_name or '*'
        where_clause = where or ''
        query = f'select count({asterisk}) from {self.schema_table_name()} {where_clause}'
        row = await self.db.fetch_one(query)
        return row['count']

    def predicate_offset_limit(self, offset: int, limit: int) -> str:
        return f'limit {limit} offset {offset - 1} '

    def predicate_order_by(self, column_names: List[str], orders: List[str] = []) -> str:
        if len(column_names) == len(orders):
            predicate: str = ','.join([f' {col} {orders[idx]}' for idx, col in enumerate(column_names)])
            return f' order by {predicate}'
        elif len(orders) >= 1:
            predicate: str = ','.join([f' {col} {orders[0]}' for col in column_names])
            return f' order by {predicate}'
        enum_column_name: str = ','.join(column_names)
        return f' order by {enum_column_name}'

    def predicate_collect(self, attribute_names: Optional[List[str]], predicate_action: str, prefix: str) -> str:

        if len(attribute_names) == 0:
            return f'{predicate_action}'
        enum_column_names = self.column_names_alias(attribute_names, prefix)
        return f'{enum_column_names}, {predicate_action}'

    async def order_by(self, column_names: List[str], orders: List[str] = []):
        cacls = self.columns_as_enum_column_names(self.metadata_table.columns)
        predicate: str = self.predicate_order_by(column_names, orders)
        query = f'select {cacls} from {self.schema_table_name()} {predicate}'
        rows = await self.db.fetch_all(query)
        return rows

    async def projection(self, str_attribute_as_comma_list, orderby=None):
        order_by = '' if orderby is None else f' order by {orderby} '
        query = f'select {str_attribute_as_comma_list} from {self.schema_table_name()} {order_by}'
        rows = await self.db.fetch_all(query)
        return rows

    async def group_by_count(self, str_attr_as_comma_list, orderby=None, format_row = None):
        order_by = '' if orderby is None else f' order by {orderby} '
        query = f'select {str_attr_as_comma_list}, count(*) from {self.schema_table_name()} {order_by} group by {str_attr_as_comma_list}'

        if format_row is None:
            rows = await self.db.fetch_all(query)
        else:
            rows = await self.fetch_all_as_json(None, query)
        return rows

    async def group_by_sum(self, str_attr_as_comma_list, attr_to_sum, orderby=None, format_row=None):
        order_by = '' if orderby is None else f' order by {orderby} '
        query = f'select {str_attr_as_comma_list}, sum({attr_to_sum}) from {self.schema_table_name()} {order_by} group by {str_attr_as_comma_list}'
        if format_row is None:
            rows = await self.db.fetch_all(query)
        else:
            rows = await self.fetch_all_as_json(None, query)
        return rows
    def get_sql_function(self, sql_type, function_name):
        return [operation for operation in SQLALCHEMY_TYPES_SQL_OPERATIONS[sql_type] if operation == function_name][0]

    async def delete(self, id_or_dict : dict):
        id_dict = id_or_dict if type(id_or_dict) == dict else {self.entity_class.primary_key() : id_or_dict}
        tuple_key_value = id_dict.popitem()
        col_eq_value = tuple_key_value[0] + ' = ' + str(tuple_key_value[1])
        query = f"DELETE FROM {self.schema_table_name()} WHERE {col_eq_value}"
        res = await self.db.execute(query=query)
        return res

    async def update(self, id_or_dict: dict, attribute_value: dict):
        id_dict = id_or_dict if type(id_or_dict) == dict else {self.entity_class.primary_key(): id_or_dict}
        list_attr_col_type = self.list_attribute_column_type_given(attribute_value.keys())
        dict_column_value = self.convert_all_to_db(list_attr_col_type, attribute_value, True)
        tuple_key_value = id_dict.popitem()
        col_eq_value = tuple_key_value[0] + ' = ' + str(tuple_key_value[1])
        enum_col_eq_value = self.enum_equal_column_names(dict_column_value)
        query = f"UPDATE {self.schema_table_name()} SET {enum_col_eq_value} WHERE {col_eq_value} "
        res = await self.db.execute(query=query, values=dict_column_value)
        return res

    async def insert(self, attribute_value: dict):
        list_attr_col_type = self.list_attribute_column_type_given(attribute_value.keys())
        dict_column_value = self.convert_all_to_db(list_attr_col_type, attribute_value)
        column_names = copy.deepcopy(list(dict_column_value.keys()))
        pk_name = self.entity_class.primary_key()
        if pk_name not in column_names:
            pk_value = await self.next_val()
            # dict_column_value[pk_name] = pk_value
        query = f"INSERT INTO {self.schema_table_name()}({self.enum_column_names(column_names)}) VALUES ({self.enum_colon_column_names(column_names)})"
        await self.db.execute(query=query, values=dict_column_value)
        return pk_value

    def db_type_name_given_attribute(self, attribute_name: str)->str:
        tp_name = self.entity_class().attrib_name_col_name_type_col_name(attribute_name)[2]
        if ('VARCHAR' in tp_name) or ('CHAR' in tp_name):
            return 'VARCHAR'
        if tp_name in ('INTEGER', 'INT', 'Integer'):
            return 'INTEGER'
        if tp_name in ('FLOAT'):
            return 'FLOAT'
        if tp_name in ('DOUBLE'):
            return 'DOUBLE'
        if tp_name in ('DATE'):
           return 'DATE'

    def convert_to_db(self, a_type: str, val, is_update: bool= False) -> Any:
        if a_type in ('VARCHAR', 'CHAR'):
            return f"'{val}'" if is_update else val
        if a_type in ('INTEGER', 'INT', 'Integer'):
            return int(val)
        if a_type in ('FLOAT', 'DOUBLE'):
            return float(val)
        if a_type in ('DATE'):
            return date.fromisoformat(val) #iso => yyyy-mm-dd
        return val

    def convert_all_to_db(self, attribute_column_type: List[tuple], attribute_value: dict, is_update : bool = False) -> dict:
        column_value = {}
        for attr, col,typ  in attribute_column_type:
            column_value[col] = self.convert_to_db(typ, attribute_value[attr], is_update)
        return column_value

    async def convert_row_to_dict(self, row: Record) -> Dict:
        dic = {}
        for key, value in row.items():
            a_type = type(value)
            if a_type == datetime.date or a_type == datetime.datetime:
                val = value.isoformat()
            else:
                val = value
            dic[key] = val
        return dic

    def action(self, typeof: object, action_name: str) -> Optional[ActionFunction]:
        if typeof in self.dict_action() and (action_name in self.dict_action()[typeof]):
            d = self.dict_action()[typeof]
            return d[action_name]
        return None

    def actions_in_chain(self, a_type: type, action_names: List[str]) -> List[ActionFunction]:
        tp: object = a_type
        actions: List[ActionFunction] = list()
        index: int = 0
        len_action: int = len(action_names)
        while index < len_action:
            action: ActionFunction = self.action(tp, action_names[index])
            actions.append(action)
            tp = action.answer
            if action.has_parameters():
                index += 1
            index += 1
        return actions

    def last_action_in_chain(self,a_type: type, action_names: List[str]) -> ActionFunction:
        return self.actions_in_chain(a_type, action_names)[-1]

    def type_of_last_action_in_chain(self,a_type: type, action_names: List[str]) -> object:
        return self.last_action_in_chain(a_type, action_names).answer
