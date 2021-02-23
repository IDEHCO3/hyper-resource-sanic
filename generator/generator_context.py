import os

from generator.pre_generator import is_geo_class
from generator.util import convert_camel_case_to_hifen, convert_camel_case_to_underline
from settings import RESOURCES_DIR, CONTEXTS_DIR


def get_template(file_name, class_name, is_geo: bool = False):
    if is_geo:
        inherit_class = 'GeoDetailContext'
        inherit_class_col = 'GeoCollectionContext'
        from_resource = 'from src.hyper_resource.context.geocontext import GeoDetailContext'
        from_collection = 'from src.hyper_resource.context.geocontext import GeoCollectionContext'
    else:
        inherit_class = 'AbstractDetailContext'
        inherit_class_col = 'AbstractCollectionContext'
        from_resource = 'from src.hyper_resource.context.abstract_context import AbstractDetailContext'
        from_collection = 'from src.hyper_resource.context.abstract_context import AbstractCollectionContext'

    template = f"""
{from_resource}
{from_collection}

class {class_name}CollectionContext({inherit_class_col}):
    @staticmethod
    def get_type_by_model_class():
        return {inherit_class_col}.get_type_by_model_class()

class {class_name}DetailContext({inherit_class}):
    @staticmethod
    def get_type_by_model_class():
        return {inherit_class}.get_type_by_model_class()
"""
    return template

# def generate_setup_contexts_file(path, file_name="setup_routes", file_names=[], class_names=[]):
#     file_with_path = os.path.join(path, f'{file_name}.py')
#     with open(file_with_path, 'w') as file:
#         for i in range(0, len(file_names)):
#             file.write(f'from src.routes.{file_names[i]} import {file_names[i]}_routes\n')
#         file.write('def setup_all_routes(app):\n')
#         for i in range(0, len(file_names)):
#             file.write(f'    {file_names[i]}_routes(app)\n')

def generate_context_file(path, file_name, class_name, is_geo: bool = False):
    file_with_path = os.path.join(path, f'{file_name}.py')
    with open(file_with_path, 'w') as file:
        file.write(get_template(file_name, class_name, is_geo))

def generate_all_context_files(clsmembers):
    path = CONTEXTS_DIR#os.path.join(os.getcwd(), 'src', 'contexts')
    try:
        os.mkdir(path)
    except FileExistsError:
        pass

    for class_name_class in clsmembers:
        is_geo = is_geo_class(class_name_class[1])
        class_name = class_name_class[0]
        file_name = convert_camel_case_to_underline(class_name)
        generate_context_file(path, file_name, class_name, is_geo)