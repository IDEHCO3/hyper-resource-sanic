import os

from generator.pre_generator import is_geo_class
from generator.util import convert_camel_case_to_underline
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

class {class_name}Resource({inherit_class_feature}):
   def __init__(self, request):
        super().__init__(request)
    
   def entity_class(self):
       return {class_name}
        
class {class_name}CollectionResource({inherit_class_feature_col}):
    def __init__(self, request):
        super().__init__(request)
    
    def entity_class(self):
        return {class_name}
"""
    return template

def generate_resource_file(path, file_name, class_name, is_geo: bool = False):
    #from templates.resource_template import template
    # file_with_path = f'{path}{file_name}.py'
    file_with_path = os.path.join(path, f'{file_name}.py')
    with open(file_with_path, 'w') as file:
        file.write(get_template(file_name, class_name, is_geo))

def generate_all_resource_files(clsmembers):#, is_geo: bool = False):
    path = os.path.join(os.getcwd(), 'src', 'resources')
    try:
        os.mkdir(path)
    except FileExistsError:
        pass

    for class_name_class in clsmembers:
        is_geo = is_geo_class(class_name_class[1])
        class_name = class_name_class[0]
        file_name = convert_camel_case_to_underline(class_name)
        generate_resource_file(path, file_name, class_name, is_geo)