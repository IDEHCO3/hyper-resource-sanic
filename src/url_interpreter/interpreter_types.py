"""
Converters to handle python/SQLAlchemy types -> JSON-LD/Schema.org conversions
"""

from geoalchemy2 import Geometry, Geography, Raster, WKTElement, WKBElement, RasterElement
from sqlalchemy import ARRAY, BIGINT, BigInteger, BINARY, Binary, BLOB, BOOLEAN, Boolean, CHAR, CLOB, DATE, Date, DATETIME, \
    DateTime, DECIMAL, Enum, Column, FLOAT, Float, INT, INTEGER, Integer, JSON, LargeBinary, NCHAR, NUMERIC, \
    Numeric, NVARCHAR, PickleType, REAL, SMALLINT, SmallInteger, String, TEXT, Text, TIME, Time, TIMESTAMP, TypeDecorator, \
    Unicode, UnicodeText, VARBINARY, VARCHAR


def is_geom_type(type) -> bool:
    return type in [Geometry, Geography, Raster, WKTElement, WKBElement, RasterElement]

def type_has_operation(type, statement:str) -> bool:
    # return callable(getattr(type.python_type, statement))
    # [ele for ele in dir(type.python_type) if not ele.startswith("__") and not ele.endswith("__") and callable(type.python_type, statement)]
    # return hasattr(type, statement)
    operations_dict = SQLALCHEMY_TYPES_OPERATIONS

    if is_geom_type(type):
        operations_dict = GEOALCHEMY_TYPES_OPERATIONS

    operations = [operation for operation in operations_dict[type]]
    operation_names = [operation.__name__ for operation in operations]
    return statement in operation_names

def get_operation(type, operation_name:str) -> str:
    operations_dict = SQLALCHEMY_TYPES_OPERATIONS

    if is_geom_type(type):
        operations_dict = GEOALCHEMY_TYPES_OPERATIONS

    operation = [oper for oper in operations_dict[type] if oper.__name__ == operation_name][0]
    return operation


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