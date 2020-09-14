import os
import sys, inspect
from generator.generator_resource import generate_all_resource_files
from generator.generator_route import generate_all_router_files,generate_all_entry_point_file
from generator.all_models import *
from generator.generate_model_files import generate_all_model_files
clsmembers = inspect.getmembers(sys.modules['all_models'], inspect.isclass)
from sqlalchemy import CHAR, Column, Float, Integer, Numeric, SmallInteger, String, Text
from sqlalchemy.sql.sqltypes import NullType
from sqlalchemy.ext.declarative import declarative_base

Base = declarative_base()
metadata = Base.metadata

objetos = [CHAR, Column, Float, Integer, Numeric, SmallInteger, String, Text, NullType, Base, metadata, Base, declarative_base, declarative_base()]
clsmembers = [clncl for clncl in clsmembers if (clncl[0] != 'Base') and (clncl[1] not in objetos)]

for i in clsmembers:
    print(i[0])
generate_all_model_files(clsmembers)   
#Generate all resources
print("Generating resource files ...")
generate_all_resource_files(clsmembers)

#Generate all routes
print("Generating route files ...")
generate_all_router_files(clsmembers)

#Generate entrypoint file
print("Generating entrypoint file")
generate_all_entry_point_file(clsmembers)
