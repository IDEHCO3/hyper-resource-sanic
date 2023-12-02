"""
Converters to handle python/SQLAlchemy types -> JSON-LD/Schema.org conversions
"""
import copy
import typing
from typing import Any

from sqlalchemy import ARRAY, BIGINT, CHAR, BigInteger, BINARY, BLOB, BOOLEAN, CLOB, DATE, \
    DATETIME, DateTime, DECIMAL, Enum, Column, FLOAT, Float, INT, INTEGER, Integer, JSON, LargeBinary, NCHAR, NUMERIC, \
    Numeric, NVARCHAR, PickleType, REAL, SMALLINT, SmallInteger, String, TEXT, Text, TIME, Time, TIMESTAMP, \
    TypeDecorator, Unicode, UnicodeText, VARBINARY, VARCHAR, Date

from src.hyper_resource.common_resource import CONTENT_TYPE_TEXT
from src.url_interpreter.interpreter_types import SupportedProperty, Operator, GreaterOperator, EqualsOperator

ACONTEXT_KEYWORD = "@context"
ATYPE_KEYWORD = "@type"
AID_KEYWORD = "@id"
ASET_KEYWORD = "@set"
ACONTAINER_KEYWORD = "@container"
HYPER_RESOURCE_VOCAB_KEY = "hr"
SUPPORTED_OPERATIONS_KEYWORD = f"{HYPER_RESOURCE_VOCAB_KEY}:supportedOperations"
SUPPORTED_PROPERTIES_KEYWORD = f"{HYPER_RESOURCE_VOCAB_KEY}:supportedProperties"
SUPPORTED_PROPERTY_KEYWORD = f"{HYPER_RESOURCE_VOCAB_KEY}:SupportedProperty"
OPERATION_KEYWORD = f"{HYPER_RESOURCE_VOCAB_KEY}:Operation"
APPEND_PATH_KEYWORD = f"{HYPER_RESOURCE_VOCAB_KEY}:appendPath"
VARIABLE_PATH_KEYWORD = f"{HYPER_RESOURCE_VOCAB_KEY}:variable"
REQUIRED_PARAMETER_PATH_KEYWORD = f"{HYPER_RESOURCE_VOCAB_KEY}:requiredParameter"
OPERATION_PARAMETER_KEYWORD = f"{HYPER_RESOURCE_VOCAB_KEY}:OperationParameter"
EXPECTS_KEYWORD_SERIALIZATION = f"{HYPER_RESOURCE_VOCAB_KEY}:expectsSerialization"
PARAMETERS_KEYWORD = f"{HYPER_RESOURCE_VOCAB_KEY}:parameters"
IS_EXTERNAL_KEYWORD = f"{HYPER_RESOURCE_VOCAB_KEY}:isExternal"
HYDRA_VOCAB_KEY = "hydra"
HYDRA_METHOD_KEYWORD = f"{HYDRA_VOCAB_KEY}:method"
HYDRA_RETURNS_HEADER_KEYWORD = f"{HYDRA_VOCAB_KEY}:returnsHeader"
HYDRA_HEADER_NAME_KEYWORD = f"{HYDRA_VOCAB_KEY}:headerName"
HYDRA_POSSIBLE_VALUE_KEYWORD = f"{HYDRA_VOCAB_KEY}:possibleValue"
HYDRA_POSSIBLE_STATUS_VALUE_KEYWORD = f"{HYDRA_VOCAB_KEY}:possibleStatus"
HYDRA_EXPECTS_HEADER_KEYWORD = f"{HYDRA_VOCAB_KEY}:expectsHeader"
HYDRA_EXPECTS_KEYWORD = f"{HYDRA_VOCAB_KEY}:expects"
HYDRA_SUPPORTED_PROPERTIES_KEYWORD = f"{HYDRA_VOCAB_KEY}:supportedProperty"
HYDRA_SUPPORTED_PROPERTY_KEYWORD = f"{HYDRA_VOCAB_KEY}:SupportedProperty"
HYDRA_PROPERTY_KEYWORD = f"{HYDRA_VOCAB_KEY}:property"
HYDRA_REQUIRED_KEYWORD = f"{HYDRA_VOCAB_KEY}:required"
HYDRA_READABLE_KEYWORD = f"{HYDRA_VOCAB_KEY}:readable"
HYDRA_WRITABLE_KEYWORD = f"{HYDRA_VOCAB_KEY}:writable"

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
    DATE:           f"{PREFIX_SCHEMAORG}:Date",
    Date:           f"{PREFIX_SCHEMAORG}:Date",
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
    str:            f"{PREFIX_SCHEMAORG}:Text",
    object:         f"{PREFIX_SCHEMAORG}:Thing",
}

MIME_TYPES_FOR_TYPE = {
    SupportedProperty: [CONTENT_TYPE_TEXT],
    GreaterOperator: [CONTENT_TYPE_TEXT],
    EqualsOperator: [CONTENT_TYPE_TEXT],
    typing.Any: [CONTENT_TYPE_TEXT]
}

HYPER_RESOURCE_TYPES = {
    SupportedProperty: f"{SUPPORTED_PROPERTY_KEYWORD}",
    GreaterOperator: f"{PREFIX_SCHEMAORG}:greater",
    EqualsOperator: f"{PREFIX_SCHEMAORG}:equal",
    typing.Any: f"{PREFIX_SCHEMAORG}:value",
}
# dict_relational_operator = {
#     'gt': '>',
#     'lt': '<',
#     'eq': '=',
#     'neq': '<>',
#     'gte': '>=',
#     'lte': '<='
# }
# = 	        Equal 	                                                                        https://schema.org/equal
# > 	        Greater than 	                                                                https://schema.org/greater
# < 	        Less than 	                                                                    https://schema.org/lesser
# >= 	        Greater than or equal 	                                                        https://schema.org/greaterOrEqual
# <= 	        Less than or equal 	                                                            https://schema.org/lesserOrEqual
# <> 	        Not equal. Note: In some versions of SQL this operator may be written as !=     https://schema.org/nonEqual
# BETWEEN 	Between a certain range
# LIKE 	    Search for a pattern
# IN 	        To specify multiple possible values for a column