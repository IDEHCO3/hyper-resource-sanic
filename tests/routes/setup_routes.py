from src.hyper_resource.abstract_resource import AbstractResource
from tests.routes.ferrovia import ferrovia_routes
from tests.routes.hidreletrica import hidreletrica_routes
from tests.routes.terra_indigena import terra_indigena_routes
from tests.routes.unidade_federacao import unidade_federacao_routes
from tests.resources.ferrovia import FerroviaResource, FerroviaCollectionResource
from tests.resources.hidreletrica import HidreletricaResource, HidreletricaCollectionResource
from tests.resources.terra_indigena import TerraIndigenaResource, TerraIndigenaCollectionResource
from tests.resources.unidade_federacao import UnidadeFederacaoResource, UnidadeFederacaoCollectionResource
def setup_all_routes(app):
    ferrovia_routes(app)
    hidreletrica_routes(app)
    terra_indigena_routes(app)
    unidade_federacao_routes(app)
    
AbstractResource.MAP_MODEL_FOR_ROUTE = {
        FerroviaResource.model_class: ferrovia_routes,
        HidreletricaResource.model_class: hidreletrica_routes,
        TerraIndigenaResource.model_class: terra_indigena_routes,
        UnidadeFederacaoResource.model_class: unidade_federacao_routes,
    }