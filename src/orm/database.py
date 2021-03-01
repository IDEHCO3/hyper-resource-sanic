from typing import List, Tuple, Optional, Any

from sqlalchemy import Column
from sqlalchemy.inspection import inspect
from sqlalchemy.orm.attributes import InstrumentedAttribute
from sqlalchemy.orm import sessionmaker
from src.orm.models import AlchemyBase, Base

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
        # return self.metadata_table.primary_key.columns[0].name
        return list(self.metadata_table.primary_key.columns)[0].name

    def foreign_keys_columns(self):
        attrs = [attribute for attribute in list(self.entity_class.__table__.c) if isinstance(attribute, Column)]
        fk_columns = [att for att in attrs if len(att.foreign_keys) > 0]
        return fk_columns

    def foreign_key_column_by_name(self, column_name:str):
        fk_columns = self.foreign_keys_columns()
        col = [column for column in fk_columns if column.key == column_name]
        if(len(col) == 0):
            raise NameError(f"The attribute is not existent or does not represent a foreign key: {column_name}")
        else:
            return col[0]

    def get_model_by_foreign_key(self, fk_column:Column):
        refered_model_name = list(fk_column.foreign_keys)[0].column.table.name
        for c in Base._decl_class_registry.values():
            if hasattr(c, '__tablename__') and c.__tablename__ == refered_model_name:
                return c

    def foreign_keys_names(self):
        # entity_relations = inspect( self.entity_class).relationships.items()
        # self.entity_class.__table__.c.<attribute>.foreign_keys
        """
        self.entity_class.usuario.parent._init_properties:OrderedDict
	    con_tipo_gasto:RelationshipProperty
	    con_usuario:RelationshipProperty
		comparator.prop.class_attribute.prop.entity._identity_class

        self.entity_class.usuario.parent._init_properties._list:List<str>
        :return:
        """
        # attrs = [attribute for key, attribute in self.entity_class.__dict__.items() if isinstance(attribute, Column)]
        fk_columns = self.foreign_keys_columns()
        # mapper = attrs[0].parent
        # fk_dict = mapper._init_properties
        # return fk_dict.keys()
        return [col.key for col in fk_columns]

    def schema_table_name(self) -> str:
        return f'{self.schema()}.{self.table_name()}'

    # todo: hardcoded
    def sequence_name(self) -> str:
        # return 's_' + self.table_name()
        return self.table_name() + "_seq"

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
        pk_value = pk
        query = f'select {enum_col_names} from {self.schema_table_name()} where {self.primary_key()}={pk_value}'
        return query

    async def next_val(sequence_name: str):
        raise NotImplementedError("'offset_limit' must be implemented in subclasses")
    async def offset_limit(self, offset, limit, orderby= None, asc=None, format_row = None):
        raise NotImplementedError("'offset_limit' must be implemented in subclasses")
    async def fetch_all(self):
        raise NotImplementedError("'fetch_all' must be implemented in subclasses")
    async def fetch_one(self):
        raise NotImplementedError("'fetch_one' must be implemented in subclasses")
    async def fetch_one_as_json(self, id_dict):
        raise NotImplementedError("'fetch_one_as_json' must be implemented in subclasses")
    async def fetch_all_as_json(self, tuple_attrib : Tuple[str] = None, a_query: str = None):
        raise NotImplementedError("'fetch_all_as_json' must be implemented in subclasses")
    async def count(self) -> int:
        raise NotImplementedError("'count' must be implemented in subclasses")
    async def order_by(self, enum):
        raise NotImplementedError("'order_by' must be implemented in subclasses")
    async def projection(self, str_attribute_as_comma_list, orderby=None):
        raise NotImplementedError("'projection' must be implemented in subclasses")
    async def group_by_count(enum, enum_attribute: str, orderby=None, format_row = None):
        raise NotImplementedError("'groupbycount' must be implemented in subclasses")
    async def group_by_sum(enum, enum_attribute: str, attr_to_sum, orderby=None, format_row=None):
        raise NotImplementedError("'groupbycount' must be implemented in subclasses")
    async def filter(self, a_filter: str):
        raise NotImplementedError("'filter' must be implemented in subclasses")
    async def filter_as_json(self, a_filter, e_column_names: str = None):
        raise NotImplementedError("'filter_as_json' must be implemented in subclasses")
    async def delete(self, id_or_dict):
        raise NotImplementedError("'delete' must be implemented in subclasses")
    async def update(self, id_dict: dict, field_value: dict):
        raise NotImplementedError("'update' must be implemented in subclasses")
    async def insert(self, field_value: dict) -> Any:
        raise NotImplementedError("'insert' must be implemented in subclasses")
