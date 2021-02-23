import importlib
import inspect
import os
from typing import Dict, List

from sqlalchemy.ext.declarative import DeclarativeMeta

from src.hyper_resource.context.abstract_context import AbstractContext
from generator.pre_generator import is_geo_class
from generator.util import convert_camel_case_to_underline, convert_camel_case_to_hifen
from settings import RESOURCES_DIR

def get_template(file_name, class_name, is_geo: bool = False):
    if is_geo:
        inherit_class_feature = 'FeatureResource'
        inherit_class_feature_col = 'FeatureCollectionResource'
        from_resource = 'from src.hyper_resource.feature_resource import FeatureResource'
        from_collection = 'from src.hyper_resource.feature_collection_resource import FeatureCollectionResource'
    else:
        inherit_class_feature = 'NonSpatialResource'
        inherit_class_feature_col = 'AbstractCollectionResource'
        from_resource = 'from src.hyper_resource.non_spatial_resource import NonSpatialResource'
        from_collection = 'from src.hyper_resource.abstract_collection_resource import AbstractCollectionResource'
    template = f"""
{from_resource}
{from_collection}
from src.models.{file_name} import {class_name}
from src.contexts.{file_name} import {class_name}DetailContext, {class_name}CollectionContext

class {class_name}Resource({inherit_class_feature}):
   model_class = {class_name}
   context_class = {class_name}DetailContext
   def __init__(self, request):
        super().__init__(request)
    
   def entity_class(self):
       return {class_name}
        
class {class_name}CollectionResource({inherit_class_feature_col}):
    model_class = {class_name}
    context_class = {class_name}CollectionContext    
    
    def __init__(self, request):
        super().__init__(request)
    
    def entity_class(self):
        return {class_name}
"""
    return template

def get_setup_template(imports:List[str], map_model_for_context_dict:Dict) -> str:
    template = f"""
    {imports}

    def setup_all_resources():
    AbstractResource.MAP_MODEL_FOR_CONTEXT = {map_model_for_context_dict}    
    """
    return template

def generate_setup_resources_file(path, class_names_list, file_name="setup_resources"):
    # d = {}
    # imports = []
    # for class_name in class_names_list:
    #
    #     imports.append(f"from src.resources.{class_file_name} import {class_name}Resource")
    #     d.update({
    #         f"{class_name}Resource.model_class": f"{class_name}Resource.context_class"
    #     })
    #
    # content = get_setup_template(imports, d)
    TAB = " " * 4
    file_with_path = os.path.join(path, f'{file_name}.py')
    with open(file_with_path, 'w') as file:
        file.write("from src.hyper_resource.abstract_resource import AbstractResource\n")
        for class_name in class_names_list:
            class_file_name = convert_camel_case_to_underline(class_name)
            file.write(f'from src.resources.{class_file_name} import {class_name}Resource, {class_name}CollectionResource\n')
        file.write('\ndef setup_all_resources():\n')
        file.write(TAB + 'AbstractResource.MAP_MODEL_FOR_CONTEXT = {\n')
        for class_name in class_names_list:
            file.write((TAB*2) + f"{class_name}Resource.model_class: {class_name}Resource.context_class,\n")
        file.write(TAB + '}')
        # for i in range(0, len(file_names)):
        #     file.write(f'    {file_names[i]}_routes(app)\n')

def generate_resource_file(path, file_name, class_name, is_geo: bool = False):
    file_with_path = os.path.join(path, f'{file_name}.py')
    with open(file_with_path, 'w') as file:
        file.write(get_template(file_name, class_name, is_geo))

def get_resource_model_class(file_name: str):
    return [_class for name, _class in inspect.getmembers(importlib.import_module(f"src.resources.{file_name}"), inspect.isclass) if isinstance(_class, DeclarativeMeta)][0]

def get_resource_context_class(file_name: str):
    return [_class for name, _class in inspect.getmembers(importlib.import_module(f"src.contexts.{file_name}"), inspect.isclass) if issubclass(_class, AbstractContext)][0]

def generate_all_resource_files(clsmembers):#, is_geo: bool = False):
    path = RESOURCES_DIR#os.path.join(os.getcwd(), 'src', 'resources')
    try:
        os.mkdir(path)
    except FileExistsError:
        pass
    class_names_list = []
    for class_name_class in clsmembers:
        is_geo = is_geo_class(class_name_class[1])
        class_name = class_name_class[0]
        file_name = convert_camel_case_to_underline(class_name)
        generate_resource_file(path, file_name, class_name, is_geo)
        # model_class = get_resource_model_class(file_name)
        # context_class = get_resource_context_class(file_name)
        class_names_list.append(class_name)

    generate_setup_resources_file(path, class_names_list, "setup_resources")