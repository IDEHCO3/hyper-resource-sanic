import os
from util import convert_camel_case_to_underline
def get_template(file_name, class_name):
    template = f"""
from src.hyper_resource.non_spatial_resource import NonSpatialResource
from src.hyper_resource.abstract_collection_resource import AbstractCollectionResource
from src.models.{file_name} import {class_name}

class {class_name}Resource(NonSpatialResource):
   def __init__(self, request):
        super().__init__(request)
    
   def entity_class(self):
       return {class_name}
        
class {class_name}CollectionResource(AbstractCollectionResource):
    def __init__(self, request):
        super().__init__(request)
    
    def entity_class(self):
        return {class_name}
"""
    return template

def generate_resource_file(path, file_name, class_name):
    #from templates.resource_template import template
    file_with_path = f'{path}{file_name}.py'
    with open(file_with_path, 'w') as file:
        file.write(get_template(file_name, class_name))

def generate_all_resource_files(clsmembers):
    path = r'' + os.getcwd()+ '/src/resources/'
    for class_name_class in clsmembers:
        class_name = class_name_class[0]
        file_name = convert_camel_case_to_underline(class_name)
        generate_resource_file(path, file_name, class_name)