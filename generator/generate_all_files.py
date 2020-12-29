import os
import sys, inspect, importlib

from generator.generate_static import generate_all_static_files
from generator.generator_resource import generate_all_resource_files
from generator.generator_route import generate_all_router_files,generate_all_entry_point_file
from generator.all_models import *
from generator.generate_model_files import generate_all_model_files
# clsmembers = inspect.getmembers(sys.modules['all_models'], inspect.isclass)
from sqlalchemy import CHAR, Column, Float, Integer, Numeric, SmallInteger, String, Text
from sqlalchemy.sql.sqltypes import NullType
from sqlalchemy.ext.declarative import declarative_base

all_models = importlib.import_module("generator.all_models")
clsmembers = inspect.getmembers(all_models, inspect.isclass)
clsmodels = [(name, _class) for name, _class in clsmembers if issubclass(_class, Base) and _class != Base]

Base = declarative_base()
metadata = Base.metadata

objetos = [CHAR, Column, Float, Integer, Numeric, SmallInteger, String, Text, NullType, Base, metadata, Base, declarative_base, declarative_base()]
# clsmembers = [clncl for clncl in clsmembers if (clncl[0] != 'Base') and (clncl[1] not in objetos)]

def main(argv):
    #for i in clsmodels:
    #    print(i[0])
    is_geo = False
    if len(argv) > 1:
        is_geo = argv[1].strip().lower() == 'true'

    print(f"Generating final model files ... is_geo = {is_geo}")

    generate_all_model_files(clsmodels, is_geo)

    # Generate all resources
    print("Generating resource files ...")
    generate_all_resource_files(clsmodels, is_geo)

    # Generate all routes
    print("Generating route files ...")
    generate_all_router_files(clsmodels)

    # Generate entrypoint file
    print("Generating entrypoint file...")
    generate_all_entry_point_file(clsmodels)

    #Generate all static files
    print("Generating all static files...")
    generate_all_static_files(clsmodels, is_geo)

if __name__ == "__main__":
   main(sys.argv)