from src.hyper_resource.abstract_resource import AbstractResource
from tests.resources.ferrovia import FerroviaResource, FerroviaCollectionResource
from tests.resources.hidreletrica import HidreletricaResource, HidreletricaCollectionResource
from tests.resources.terra_indigena import TerraIndigenaResource, TerraIndigenaCollectionResource
from tests.resources.unidade_federacao import UnidadeFederacaoResource, UnidadeFederacaoCollectionResource

def setup_all_resources():
    AbstractResource.MAP_MODEL_FOR_CONTEXT = {
        FerroviaResource.model_class: FerroviaResource.context_class,
        HidreletricaResource.model_class: HidreletricaResource.context_class,
        TerraIndigenaResource.model_class: TerraIndigenaResource.context_class,
        UnidadeFederacaoResource.model_class: UnidadeFederacaoResource.context_class,
    }