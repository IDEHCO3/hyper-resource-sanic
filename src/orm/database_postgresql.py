from orm.database import DialectDatabase
from sqlalchemy import text
class DialectDbPostgresql(DialectDatabase):
    def __init__(self, db, metadata_table, entity_class):
        super().__init__(db, metadata_table, entity_class)
           
    async def offset_limit(self, offset, limit, orderby= None, asc=None):
        colums_as_comma_name = self.columns_as_comma_list_str(self.metadata_table.columns)
        asc = 'desc' if asc == 'desc' else 'asc'
        orderbyasc = '' if orderby is None else f' order by {orderby} {asc} '  
        query = f'select {colums_as_comma_name} from {self.metadata_table.schema}.{self.metadata_table.name} {orderbyasc}limit {limit} offset {offset}'
        return await self.db.fetch_all(query)
     
    async def fetch_all(self):
        query = self.metadata_table.select()
        print(query)
        rows = await self.db.fetch_all(query)
        return rows
    
    async def fetch_one(self, dic):
        key_name = next(key for key in dic.keys())
        cols_as_enum = self.column_names_as_enum()
        query = f'select {cols_as_enum} from {self.metadata_table.schema}.{self.metadata_table.name} where {key_name} = :{key_name}'
        row = await self.db.fetch_one(query=query, values=dic)
        return row
        
    async def count(self):
        query = f'select count(*) from {self.metadata_table.schema}.{self.metadata_table.name}'
        row = await self.db.fetch_one(query)
        return row
        
    async def order_by(self, str_attr_as_comma_list):
        cacls = self.columns_as_comma_list_str(self.metadata_table.columns)
        query = f'select {cacls} from {self.metadata_table.schema}.{self.metadata_table.name} order by {str_attr_as_comma_list}'
        rows = await self.db.fetch_all(query)
        return rows
    
    async def projection(self, str_attribute_as_comma_list, orderby=None):
        order_by = '' if orderby is None else f' order by {orderby} '
        query = f'select {str_attribute_as_comma_list} from {self.metadata_table.schema}.{self.metadata_table.name}{order_by}'
        rows = await self.db.fetch_all(query)
        return rows
    
    async def group_by_count(self, str_attr_as_comma_list, orderby=None):
        order_by = '' if orderby is None else f' order by {orderby} '
        query = f'select {str_attr_as_comma_list}, count(*) from {self.metadata_table.schema}.{self.metadata_table.name}{order_by} group by {str_attr_as_comma_list}'
        rows = await self.db.fetch_all(query)
        return rows
    
    async def group_by_sum(self, str_attr_as_comma_list, attr_to_sum, orderby=None):
        order_by = '' if orderby is None else f' order by {orderby} '
        query = f'select {str_attribute_as_comma_list}, sum({attr_to_sum}) from {self.metadata_table.schema}.{self.metadata_table.name}{order_by} group by {str_attribute_as_comma_list}'
        rows = await self.db.fetch_all(query)
        return rows
   