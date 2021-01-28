from typing import List, Tuple, Optional, Any

from sqlalchemy.orm import sessionmaker

from src.orm.models import AlchemyBase


class AbstractDialectDatabase():
    def __init__(self, db):
        self.db = db


class DialectDatabase(AbstractDialectDatabase):
    def __init__(self, db, metadata_table=None, entity_class: AlchemyBase = None):
        super().__init__(db)
        self.metadata_table = metadata_table if metadata_table is not None else entity_class.__table__
        self.entity_class = entity_class

    def schema(self) -> str:
        return self.metadata_table.schema

    def table_name(self) -> str:
        return self.metadata_table.name

    def primary_key(self) -> str:
        return self.metadata_table.primary_key.columns[0].name
    def schema_table_name(self) -> str:
        return f'{self.schema()}.{self.table_name()}'

    def sequence_name(self) -> str:
        return 's_' + self.table_name()

    def schema_sequence(self) -> str:
        return f'{self.schema()}.{self.sequence_name()}'

    def columns_as_comma_list_str(self, columns) -> str:
        return ','.join([column.name for column in columns])

    def enum_column_names(self, column_names: List[str] = None) -> str:
        if column_names is not None:
            return ','.join(column_names)
        return ','.join(self.entity_class.column_names())

    def enum_colon_column_names(self, column_names: List[str] = None) -> str:
        if column_names is not None:
            return (','.join((':' + s for s in column_names)))

        return (','.join((':' + s for s in self.entity_class.column_names())))

    def enum_equal_column_names(self, column_value: dict) -> str:
        return (','.join((key + ' = :' + key for key, value in column_value.items())))

    def column_names_given_attributes(self, attributes_from_path) -> List[str]:
        return self.entity_class.column_names_given_attributes(attributes_from_path)

    def column_names_as_enum_given_attributes(self, attributes_from_path) -> str:
        return self.column_names_as_enum_given_attributes(attributes_from_path)

    def enum_column_names_alias_attribute_given(self, tuple_attrib: Tuple[str]) -> str:
        list_attrib_column = self.list_attribute_column_given(tuple_attrib)
        return self.entity_class.enum_column_names_alias_attribute_given(list_attrib_column)

    def list_attribute_column_given(self, attributes_from_path: Optional[Tuple[str]]) -> List[Tuple]:
        return self.entity_class.list_attribute_column_given(attributes_from_path)

    def list_attribute_column_type(self) -> List[tuple]:
        return self.entity_class.list_attribute_column_type()

    def list_attribute_column_type_given(self, attributes: List[str]) -> List[tuple]:
        return self.entity_class.list_attribute_column_type_given(attributes)

    def attribute_names(self) -> List[str]:
        return self.entity_class.attribute_names()

    def basic_select(self, tuple_attrib: Tuple[str] = None) -> str:
        if tuple_attrib is not None:
            enum_col_names = self.enum_column_names_alias_attribute_given(tuple_attrib)
        else:
            enum_col_names = self.enum_column_names_alias_attribute_given(self.attribute_names())
        query = f'select {enum_col_names} from {self.schema_table_name()}'
        return query

    def basic_select_by_id(self, pk, tuple_attrib: Tuple[str] = None):
        if tuple_attrib is not None:
            enum_col_names = self.enum_column_names_alias_attribute_given(tuple_attrib)
        else:
            enum_col_names = self.enum_column_names_alias_attribute_given(self.attribute_names())
        pk_value = int(pk)
        query = f'select {enum_col_names} from {self.schema_table_name()} where {self.primary_key()}={pk_value}'
        return query
    async def next_val(sequence_name: str):
        raise NotImplementedError("'offset_limit' must be implemented in subclasses")

    async def offset_limit(self, offset, limit, orderby=None, asc=None):
        raise NotImplementedError("'offset_limit' must be implemented in subclasses")

    async def fetch_all(self):
        raise NotImplementedError("'fetch_all' must be implemented in subclasses")

    async def fetch_one(self):
        raise NotImplementedError("'fetch_one' must be implemented in subclasses")

    async def fetch_one_as_json(self, id_dict):
        raise NotImplementedError("'fetch_one_as_json' must be implemented in subclasses")

    async def fetch_all_as_json(self, list_attrib_column: Tuple[str] = None):
        raise NotImplementedError("'fetch_all_as_json' must be implemented in subclasses")

    async def count(self) -> int:
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

    async def delete_one(self, value: int):
        raise NotImplementedError("'delete one' must be implemented in subclasses")

    async def delete(self, id_or_dict):
        raise NotImplementedError("'delete' must be implemented in subclasses")

    async def update(self, id_dict: dict, field_value: dict):
        raise NotImplementedError("'update' must be implemented in subclasses")

    async def update_raw(self, id_dict: dict, field_value: dict):
        raise NotImplementedError("'update raw' must be implemented in subclasses")

    async def insert_one(self, field_value: dict) -> Any:
        raise NotImplementedError("'insert' must be implemented in subclasses")

    async def insert_one_raw(self, attribute_value: dict) -> Any:
        raise NotImplementedError("'insert raw' must be implemented in subclasses")
