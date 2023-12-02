"""
Converters to handle python/SQLAlchemy types -> JSON-LD/Schema.org conversions
"""
from typing import List, Any, Union

from geoalchemy2 import Geometry, Geography, Raster, WKTElement, WKBElement, RasterElement
from sqlalchemy import ARRAY, BIGINT, BigInteger, BINARY,  BLOB, BOOLEAN, CHAR, CLOB, DATE, Date, DATETIME, \
    DateTime, DECIMAL, Enum, Column, FLOAT, Float, INT, INTEGER, Integer, JSON, LargeBinary, NCHAR, NUMERIC, \
    Numeric, NVARCHAR, PickleType, REAL, SMALLINT, SmallInteger, String, TEXT, Text, TIME, Time, TIMESTAMP, TypeDecorator, \
    Unicode, UnicodeText, VARBINARY, VARCHAR

from src.orm.database_postgis import dic_action


def is_geom_type(_type) -> bool:
    return _type in [Geometry, Geography, Raster, WKTElement, WKBElement, RasterElement]

def type_has_operation(_type, statement:str) -> bool:
    # return callable(getattr(type.python_type, statement))
    # [ele for ele in dir(type.python_type) if not ele.startswith("__") and not ele.endswith("__") and callable(type.python_type, statement)]
    # return hasattr(type, statement)
    operations_dict = SQLALCHEMY_TYPES_OPERATIONS

    if is_geom_type(_type):
        #operations_dict = GEOALCHEMY_TYPES_OPERATIONS
        return statement in dic_action.keys()

    operations = [operation for operation in operations_dict[_type]]
    operation_names = [operation.__name__ for operation in operations]
    return statement in operation_names

def get_operation(_type, operation_name:str) -> str:
    operations_dict = SQLALCHEMY_TYPES_OPERATIONS

    if is_geom_type(_type):
        #operations_dict = GEOALCHEMY_TYPES_OPERATIONS
        return operation_name in dic_action.keys()

    operation = [oper for oper in operations_dict[_type] if oper.__name__ == operation_name][0]
    return operation


class SupportedProperty:
    def __init__(self, property:str, required:bool, readable:bool, writable:bool, isExternal:bool):
        self.property = property
        self.required = required
        self.readable = readable
        self.writable = writable
        self.isExternal = isExternal

class Operator:
    def __init__(self, name:str, symbol:str):
        self.name = name
        self.symbol = symbol

    @classmethod
    def build(cls):
        raise NotImplementedError("'build' must be implemented in subclasses")


class GreaterOperator(Operator):
    def __init__(self):
        super().__init__("greater", 'gt')

    @classmethod
    def build(cls):
        return GreaterOperator()

class EqualsOperator(Operator):
    def __init__(self):
        super().__init__("equals", 'eq')

    @classmethod
    def build(cls):
        return EqualsOperator()

# dict_relational_operator = {
#     'gt': '>',
#     'lt': '<',
#     'eq': '=',
#     'neq': '<>',
#     'gte': '>=',
#     'lte': '<='
# }

def filter(supported_property:SupportedProperty, operator:Union[GreaterOperator, EqualsOperator], value:Any) -> List[object]:
    pass

COLLECTION_EXPOSED_OPERATIONS = [filter]
COLLECTION_TYPES_OPERATIONS = {
    List: COLLECTION_EXPOSED_OPERATIONS
}
# --- operations executable throught client URL ---
def upper() -> str:
    pass
def lower() -> str:
    pass
def replace(old: str, new: str) -> str:
    pass

STRING_EXPOSED_OPERATIONS = [upper, lower, replace]

SQLALCHEMY_TYPES_OPERATIONS = {
    ARRAY:          [],
    BIGINT:         [],
    CHAR:           [],
    BigInteger:     [],
    BINARY:         [],
    #Binary:         [],
    BLOB:           [],
    BOOLEAN:        [],
    #Boolean:        [],
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
    String:         STRING_EXPOSED_OPERATIONS,
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
# --- Geospatial collection operations ---
def within(geometry: Geometry) -> List[Geometry]:
    pass
def contains(geometry: Geometry) -> List[Geometry]:
    pass

GEOMETRY_COLLECTION_EXPOSED_OPERATIONS = [within, contains]

GEOALCHEMY_COLLECTION_TYPES_OPERATIONS = {
    Geometry:       GEOMETRY_COLLECTION_EXPOSED_OPERATIONS,
    Geography:      [],
    Raster:         [],
    WKTElement:     [],
    WKBElement:     [],
    RasterElement:  []
}

# --- Geospatial operations ---
def area() -> float:
    pass
def buffer(radius_of_buffer: float) -> Geometry:
    pass

GEOMETRY_EXPOSED_OPERATIONS = [area, buffer]

GEOALCHEMY_TYPES_OPERATIONS = {
    Geometry:       GEOMETRY_EXPOSED_OPERATIONS,
    Geography:      [],
    Raster:         [],
    WKTElement:     [],
    WKBElement:     [],
    RasterElement:  []
}

def python_to_sqlalchemy_type(python_type: type) -> str:
    d = {
        # "TypeEngine",
        # "TypeDecorator",
        # "UserDefinedType",
        # "INT",
        # "CHAR",
        str: "VARCHAR",
        # "NCHAR",
        # "NVARCHAR",
        # "TEXT",
        # "Text",
        float: "FLOAT",
        # "NUMERIC",
        # "REAL",
        # "DECIMAL",
        # "TIMESTAMP",
        # "DATETIME",
        # "CLOB",
        # "BLOB",
        # "BINARY",
        # "VARBINARY",
        bool: "BOOLEAN",
        # "BIGINT",
        # "SMALLINT",
        int: "INTEGER",
        # "DATE",
        # "TIME",
        # "String",
        # "Integer",
        # "SmallInteger",
        # "BigInteger",
        # "Numeric",
        # "Float",
        # "DateTime",
        # "Date",
        # "Time",
        # "LargeBinary",
        # "Binary",
        # "Boolean",
        # "Unicode",
        # "Concatenable",
        # "UnicodeText",
        # "PickleType",
        # "Interval",
        # "Enum",
        # "Indexable",
        list: "ARRAY",
        # "JSON",
    }
    return d[python_type]