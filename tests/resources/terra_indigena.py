
from src.hyper_resource.feature_resource import FeatureResource
from src.hyper_resource.feature_collection_resource import FeatureCollectionResource
from tests.models.terra_indigena import TerraIndigena
from tests.contexts.terra_indigena import TerraIndigenaDetailContext, TerraIndigenaCollectionContext

class TerraIndigenaResource(FeatureResource):
   model_class = TerraIndigena
   context_class = TerraIndigenaDetailContext
   def __init__(self, request):
        super().__init__(request)
    
   def entity_class(self):
       return TerraIndigena
        
class TerraIndigenaCollectionResource(FeatureCollectionResource):
    model_class = TerraIndigena
    context_class = TerraIndigenaCollectionContext    
    
    def __init__(self, request):
        super().__init__(request)
    
    def entity_class(self):
        return TerraIndigena
