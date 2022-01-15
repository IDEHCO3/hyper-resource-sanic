
from src.hyper_resource.feature_resource import FeatureResource
from src.hyper_resource.feature_collection_resource import FeatureCollectionResource
from tests.models.ferrovia import Ferrovia
from tests.contexts.ferrovia import FerroviaDetailContext, FerroviaCollectionContext

class FerroviaResource(FeatureResource):
   model_class = Ferrovia
   context_class = FerroviaDetailContext
   def __init__(self, request):
        super().__init__(request)
    
   def entity_class(self):
       return Ferrovia
        
class FerroviaCollectionResource(FeatureCollectionResource):
    model_class = Ferrovia
    context_class = FerroviaCollectionContext    
    
    def __init__(self, request):
        super().__init__(request)
    
    def entity_class(self):
        return Ferrovia
