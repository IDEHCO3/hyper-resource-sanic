import os

from sqlalchemy.orm import RelationshipProperty

from generator.pre_generator import is_geo_class
from generator.util import convert_camel_case_to_underline
from sqlalchemy.orm.attributes import InstrumentedAttribute
from sqlalchemy.orm.properties import ColumnProperty


def base_template(is_geo: bool= False):
    if is_geo:
        alchemy_base = 'AlchemyGeoBase'
        import_geo = 'from geoalchemy2 import Geometry'
    else:
        alchemy_base = 'AlchemyBase'
        import_geo =''
    return f"""# -*- coding: utf-8 -*-
{import_geo}
from sqlalchemy import CHAR, Column, Float, Integer, Numeric, SmallInteger, String, Text, Date
from sqlalchemy.orm import relationship
from sqlalchemy.sql.sqltypes import NullType
from sqlalchemy.ext.declarative import declarative_base
from src.orm.models import {alchemy_base}, Base
"""
def generate_string_for_column_property(attribute_name, column_property):
    schema_column = column_property.columns[0]
    str_for_attr = 'Column('
    str_for_attr += "'" + schema_column.name + "'" + ','
    str_for_attr += schema_column.type.__repr__() + ','
    if schema_column.primary_key:
        str_for_attr += 'primary_key=True' + ','
    str_for_attr += 'nullable=' + schema_column.nullable.__repr__()
    str_for_attr += ')'
    return attribute_name + ' = ' + str_for_attr

def geo_field_name_template(a_class):
    tuple_k_name_col_type = [(key, value.prop.columns[0].name, value.prop.columns[0].type.__str__()) for key, value in
     a_class.__dict__.items() if isinstance(value, InstrumentedAttribute) and isinstance(value.prop,ColumnProperty )]
    geo_feld_name = next((tuple_name_type for tuple_name_type in tuple_k_name_col_type if tuple_name_type[2].startswith('geometry(')), None)
    return f"""
   @classmethod
   def geo_column_name(cls) -> str:
       return '{geo_feld_name[0]}'"""

def generate_model_file(path, file_name, class_name, a_class, is_geo: bool = False):
    #from templates.resource_template import template
    file_with_path = f'{path}{file_name}.py'
    with open(file_with_path, 'w') as file:
        file.write(base_template(is_geo))
        file.write('\n\n')
        base_alchemy = 'AlchemyGeoBase' if is_geo else 'AlchemyBase'
        file.write(f'class {class_name}({base_alchemy}, Base): \n')
        file.write(f"   __tablename__ = '{a_class.__tablename__}'\n")
        file.write(f"   __table_args__ = {a_class.__table_args__.__str__()}\n")
        file.write('\n')
        tuplas = [(key, value) for key, value in a_class.__dict__.items() if isinstance(value, InstrumentedAttribute)]
        for key, value in tuplas:
             if isinstance(value.prop, ColumnProperty):
                str_attrib =  generate_string_for_column_property(key, value.prop)
                file.write(f'   {str_attrib}\n')
             elif isinstance(value.prop, RelationshipProperty):
                str_attrib = f"{key} = relationship('{value.prop.entity.class_.__name__}')"
                file.write(f'   {str_attrib}\n')
        if is_geo:
            file.write(geo_field_name_template(a_class))

def generate_all_model_files(clsmembers):#, is_geo: bool = False):
    # passpath = r'' + os.getcwd() + '/src/models/'
    for class_name_class in clsmembers:
        is_geo = is_geo_class(class_name_class[1])
        class_name = class_name_class[0]
        file_name = convert_camel_case_to_underline(class_name)
        path = r'' + os.getcwd() + '/src/models/'
        generate_model_file(path, file_name, class_name, class_name_class[1], is_geo)