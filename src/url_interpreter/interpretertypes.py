from geoalchemy2 import Geometry, Geography, Raster, WKTElement, WKBElement, RasterElement
from sqlalchemy import ARRAY, BIGINT, CHAR, BigInteger, BINARY, Binary, BLOB, BOOLEAN, Boolean, CHAR, CLOB, DATE, Date, DATETIME, \
    DateTime, DateTime, DECIMAL, Enum, Column, FLOAT, Float, INT, INTEGER, Integer, JSON, LargeBinary, NCHAR, NUMERIC, \
    Numeric, NVARCHAR, PickleType, REAL, SMALLINT, SmallInteger, String, TEXT, Text, TIME, Time, TIMESTAMP, TypeDecorator, \
    Unicode, UnicodeText, VARBINARY, VARCHAR
import copy

def is_geom_type(type) -> bool:
    return type in [Geometry, Geography, Raster, WKTElement, WKBElement, RasterElement]

def type_has_operation(type, statement):
    # return callable(getattr(type.python_type, statement))
    # [ele for ele in dir(type.python_type) if not ele.startswith("__") and not ele.endswith("__") and callable(type.python_type, statement)]
    # return hasattr(type, statement)
    operations_dict = SQLALCHEMY_TYPES_OPERATIONS

    if is_geom_type(type):
        operations_dict = GEOALCHEMY_TYPES_OPERATIONS

    operations = [operation for operation in operations_dict[type]]
    operation_names = [operation.__name__ for operation in operations]
    return statement in operation_names

def get_operation(type, operation_name):
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

PREFIX_SCHEMAORG = "schema"
SQLALCHEMY_SCHEMA_ORG_TYPES = {
    ARRAY:          None,
    BIGINT:         f"{PREFIX_SCHEMAORG}:Integer",
    CHAR:           f"{PREFIX_SCHEMAORG}:Float",
    BigInteger:     f"{PREFIX_SCHEMAORG}:Integer",
    BINARY:         None,
    Binary:         None,
    BLOB:           None,
    BOOLEAN:        f"{PREFIX_SCHEMAORG}:Boolean",
    Boolean:        f"{PREFIX_SCHEMAORG}:Boolean",
    CLOB:           None,
    DATE:           None,
    Date:           None,
    DATETIME:       None,
    DateTime:       None,
    DECIMAL:        f"{PREFIX_SCHEMAORG}:Float",
    Enum:           None,
    Column:         None,
    FLOAT:          f"{PREFIX_SCHEMAORG}:Float",
    Float:          f"{PREFIX_SCHEMAORG}:Float",
    INT:            f"{PREFIX_SCHEMAORG}:Integer",
    INTEGER:        f"{PREFIX_SCHEMAORG}:Integer",
    Integer:        f"{PREFIX_SCHEMAORG}:Integer",
    JSON:           None,
    LargeBinary:    None,
    NCHAR:          f"{PREFIX_SCHEMAORG}:Text",
    NUMERIC:        f"{PREFIX_SCHEMAORG}:Float",
    Numeric:        f"{PREFIX_SCHEMAORG}:Float",
    NVARCHAR:       f"{PREFIX_SCHEMAORG}:Text",
    PickleType:     None,
    REAL:           f"{PREFIX_SCHEMAORG}:Float",
    SMALLINT:       f"{PREFIX_SCHEMAORG}:Integer",
    SmallInteger:   f"{PREFIX_SCHEMAORG}:Integer",
    String:         f"{PREFIX_SCHEMAORG}:Text",
    TEXT:           f"{PREFIX_SCHEMAORG}:Text",
    Text:           f"{PREFIX_SCHEMAORG}:Text",
    TIME:           None,
    Time:           None,
    TIMESTAMP:      None,
    TypeDecorator:  None,
    Unicode:        None,
    UnicodeText:    None,
    VARBINARY:      None,
    VARCHAR:        f"{PREFIX_SCHEMAORG}:Text",
}

PYTHON_SCHEMA_ORG_TYPES = {
    int:            f"{PREFIX_SCHEMAORG}:Integer",
    float:          f"{PREFIX_SCHEMAORG}:Float",
    bool:           f"{PREFIX_SCHEMAORG}:Boolean",
    str:            f"{PREFIX_SCHEMAORG}:Text"
}
GEOPYTHON_SCHEMA_ORG_TYPES = copy.deepcopy(PYTHON_SCHEMA_ORG_TYPES)

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
