
from src.hyper_resource.feature_resource import FeatureResource
from src.hyper_resource.feature_collection_resource import FeatureCollectionResource
from tests.models.hidreletrica import Hidreletrica
from tests.contexts.hidreletrica import HidreletricaDetailContext, HidreletricaCollectionContext

class HidreletricaResource(FeatureResource):
   model_class = Hidreletrica
   context_class = HidreletricaDetailContext
   def __init__(self, request):
        super().__init__(request)
    
   def entity_class(self):
       return Hidreletrica
        
class HidreletricaCollectionResource(FeatureCollectionResource):
    model_class = Hidreletrica
    context_class = HidreletricaCollectionContext    
    
    def __init__(self, request):
        super().__init__(request)
    
    def entity_class(self):
        return Hidreletrica
