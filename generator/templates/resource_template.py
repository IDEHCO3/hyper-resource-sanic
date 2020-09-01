template = f"""
from src.hyper_resource.abstract_resource import AbstractResource
from src.hyper_resource.abstract_collection_resource import AbstractCollectionResource
from src.models.{file_name} import {class_name}

class {class_name}Resource(AbstractResource):
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