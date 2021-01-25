from typing import List, Tuple

from sqlalchemy.orm import sessionmaker

class AbstractDialectDatabase():
    pass

class DialectDatabase(AbstractDialectDatabase):
    def __init__(self, db, metadata_table, entity_class):
        self.db = db
        self.metadata_table = metadata_table
        self.entity_class = entity_class

    def schema(self) -> str:
        return self.metadata_table.schema
    def table_name(self) -> str:
        return self.metadata_table.name
    def schema_table_name(self) -> str:
        return f'{self.schema()}.{self.table_name()}'
    def columns_as_comma_list_str(self, columns) -> str:
        return ','.join([column.name for column in columns])
    def column_names_as_enum(self) -> str:
        return self.entity_class.enum_column_names()
    def column_names_colon_as_enum(self) -> str:
        return self.entity_class.enum_column_names_colon()
    def column_names_given_attributes(self, attributes_from_path)-> List[str]:
        return self.entity_class.column_names_given_attributes(attributes_from_path)
    def column_names_as_enum_given_attributes(self, attributes_from_path) -> str:
        return self.column_names_as_enum_given_attributes(attributes_from_path)
    def enum_column_names_alias_attribute_given(self, tuple_attrib: Tuple[str]) -> str:
        list_attrib_column = self.list_attribute_column_given(tuple_attrib)
        return self.entity_class.enum_column_names_alias_attribute_given(list_attrib_column)
    def list_attribute_column_given(self, attributes_from_path: Tuple[str]) -> List[Tuple]:
        return self.entity_class.list_attribute_column_given(attributes_from_path)

    def basic_select(self, tuple_attrib: Tuple[str]) -> str:
        if tuple_attrib is None:
            query = f'select {self.column_names_as_enum()} from {self.schema_table_name()}'
        else:
            query = f'select {self.enum_column_names_alias_attribute_given(tuple_attrib)} from {self.schema_table_name()}'
        return query
    def basic_select_by_id(self, pk):
        columns_names = self.column_names_as_enum()
        schema = self.metadata_table.schema
        table_name = self.metadata_table.name
        id_fullname = f'{schema}.{table_name}.{list(self.metadata_table.primary_key.columns)[0].name}'
        query = f'select {columns_names} from {schema}.{table_name} where {id_fullname}={pk}'
        return query
    async def offset_limit(self, offset, limit, orderby=None, asc=None):
        raise NotImplementedError("'offset_limit' must be implemented in subclasses")
    async def fetch_all(self):
        raise NotImplementedError("'fetch_all' must be implemented in subclasses")
    async def fetch_one(self):
        raise NotImplementedError("'fetch_one' must be implemented in subclasses")
    async def fetch_all_as_json(self, list_attrib_column : Tuple[str] = None):
        raise NotImplementedError("'fetch_all_as_json' must be implemented in subclasses")
    async def count(self):
        raise NotImplementedError("'count' must be implemented in subclasses")
    async def order_by(self, enum):
        raise NotImplementedError("'order_by' must be implemented in subclasses")
    async def projection(self, str_attribute_as_comma_list, orderby=None):
        raise NotImplementedError("'projection' must be implemented in subclasses")
    async def group_by_count(enum, orderby=None):
        raise NotImplementedError("'groupbycount' must be implemented in subclasses")
    async def group_by_sum(enum, attr_to_sum, orderby=None):
        raise NotImplementedError("'groupbycount' must be implemented in subclasses")
    async def filter(self, a_filter, attr_to_sum, orderby=None):
        raise NotImplementedError("'filter' must be implemented in subclasses")
    async def delete_one(self, id_dict: dict):
        raise NotImplementedError("'delete' must be implemented in subclasses")
    async def update_one(self, id_dict: dict, field_value: dict):
        raise NotImplementedError("'update' must be implemented in subclasses")
    async def insert_one(self, field_value: dict):
        raise NotImplementedError("'insert' must be implemented in subclasses")