from src.hyper_resource.abstract_collection_resource import AbstractCollectionResource
from src.hyper_resource.context.geocontext import GeoCollectionContext


class SpatialCollectionResource(AbstractCollectionResource):
    def __init__(self, request):
        super().__init__(request)
        self.context_class = GeoCollectionContext