
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm.attributes import InstrumentedAttribute

Base = declarative_base()

class AlchemyBase:
    @classmethod     
    def schema(cls):
        return cls.__table_args__ ['schema']
    @classmethod
    def table_name(cls):
        return cls.__table__.name

    @classmethod
    def primary_key(cls):
        return next(c.key for c in cls.__table__.columns if c.primary_key)

    @classmethod
    def attribute_names(cls):
        return [ value.key for key, value in cls.__dict__.items() if isinstance(value, InstrumentedAttribute)]
    
    @classmethod
    def dict_attribute_column(cls): 
        return [ {key: value.prop.columns[0].name} for key, value in cls.__dict__.items() if isinstance(value, InstrumentedAttribute)]
    
    @classmethod    
    def columns_name(cls):
        return [col.name for col in cls.__table__.columns]
    
    @classmethod
    def column_names_as_enum(cls):
        return ','.join(cls.columns_name())