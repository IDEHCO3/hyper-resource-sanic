import os
from util import convert_camel_case_to_underline
from sqlalchemy.orm.attributes import InstrumentedAttribute

def base_template():
   return """
# coding: utf-8
from sqlalchemy import CHAR, Column, Float, Integer, Numeric, SmallInteger, String, Text
from sqlalchemy.sql.sqltypes import NullType
from sqlalchemy.ext.declarative import declarative_base
from src.orm.models import AlchemyBase, Base
"""

def generate_model_file(path, file_name, class_name, a_class):
    #from templates.resource_template import template
    file_with_path = os.path.join(path, file_name + '.py')
    with open(file_with_path, 'w') as file:
        file.write(base_template())
        file.write('\n\n')
        file.write(f'class {class_name}(AlchemyBase, Base): \n')
        file.write(f"   __tablename__ = '{a_class.__tablename__}'\n")
        file.write(f"   __table_args__ = {a_class.__table_args__.__str__()}\n")
        file.write('\n')
        for key, value in a_class.__dict__.items():
             if isinstance(value, InstrumentedAttribute):
                left_part = key + ' = '
                str_column = value.prop.columns[0].__repr__()
                if str_column.split(',')[-1].startswith(' table'):
                    right_part = ','.join(str_column.split(',')[:-1]) + ')'
                else:
                    res = [snippet for snippet in str_column.split(',') if not snippet.startswith(' table')] 
                    right_part = ','.join(res)
                file.write(f'   {left_part}{right_part}\n')

def generate_all_model_files(clsmembers):
    src_path = os.path.join(os.path.dirname(os.getcwd()), 'src')
    models_path = os.path.join(src_path, 'models')
    if not os.path.exists(models_path):
        os.makedirs(models_path)

    for class_name_class in clsmembers:
        class_name = class_name_class[0]
        file_name = convert_camel_case_to_underline(class_name)
        generate_model_file(models_path, file_name, class_name, class_name_class[1])