"""
Converters to handle python/SQLAlchemy types -> JSON-LD/Schema.org conversions
"""
import copy

from sqlalchemy import ARRAY, BIGINT, CHAR, BigInteger, BINARY,  BLOB, BOOLEAN,  CLOB, DATE, \
    DATETIME, DateTime, DECIMAL, Enum, Column, FLOAT, Float, INT, INTEGER, Integer, JSON, LargeBinary, NCHAR, NUMERIC, \
    Numeric, NVARCHAR, PickleType, REAL, SMALLINT, SmallInteger, String, TEXT, Text, TIME, Time, TIMESTAMP, \
    TypeDecorator, Unicode, UnicodeText, VARBINARY, VARCHAR
PREFIX_SCHEMAORG = "schema"
SQLALCHEMY_SCHEMA_ORG_TYPES = {
    ARRAY:          None,
    BIGINT:         f"{PREFIX_SCHEMAORG}:Integer",
    CHAR:           f"{PREFIX_SCHEMAORG}:Float",
    BigInteger:     f"{PREFIX_SCHEMAORG}:Integer",
    BINARY:         None,
    #Binary:         None,
    BLOB:           None,
    BOOLEAN:        f"{PREFIX_SCHEMAORG}:Boolean",
    #Boolean:        f"{PREFIX_SCHEMAORG}:Boolean",
    CLOB:           None,
    DATE:           None,
    #Date:           None,
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