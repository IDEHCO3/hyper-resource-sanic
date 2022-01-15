
from src.hyper_resource.feature_resource import FeatureResource
from src.hyper_resource.feature_collection_resource import FeatureCollectionResource
from tests.models.unidade_federacao import UnidadeFederacao
from tests.contexts.unidade_federacao import UnidadeFederacaoDetailContext, UnidadeFederacaoCollectionContext

class UnidadeFederacaoResource(FeatureResource):
   model_class = UnidadeFederacao
   context_class = UnidadeFederacaoDetailContext
   def __init__(self, request):
        super().__init__(request)
    
   def entity_class(self):
       return UnidadeFederacao
        
class UnidadeFederacaoCollectionResource(FeatureCollectionResource):
    model_class = UnidadeFederacao
    context_class = UnidadeFederacaoCollectionContext    
    
    def __init__(self, request):
        super().__init__(request)
    
    def entity_class(self):
        return UnidadeFederacao
