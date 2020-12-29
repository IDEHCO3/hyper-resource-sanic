from sqlalchemy.orm import sessionmaker

class AbstractDialectDatabase():
    pass

class DialectDatabase(AbstractDialectDatabase):
    def __init__(self, db, metadata_table, entity_class):
        self.db = db
        self.metadata_table = metadata_table
        self.entity_class = entity_class
        
    def columns_as_comma_list_str(self, columns):
        return ','.join([column.name for column in columns])
    
    def column_names_as_enum(self):
        return self.entity_class.column_names_as_enum()
    def basic_select(self):
        query = f'select {self.column_names_as_enum()} from {self.metadata_table.schema}.{self.metadata_table.name}'
        return query
    async def offset_limit(self, offset, limit, orderby=None, asc=None):
        raise NotImplementedError("'offset_limit' must be implemented in subclasses")
    async def fetch_all(self):
        raise NotImplementedError("'fetch_all' must be implemented in subclasses")
    async def fetch_one(self):
        raise NotImplementedError("'fetch_one' must be implemented in subclasses")
    async def fetch_all_as_json(self):
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
    async def filter(a_filter, attr_to_sum, orderby=None):
        raise NotImplementedError("'filter' must be implemented in subclasses")