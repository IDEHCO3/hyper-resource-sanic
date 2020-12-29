from src.hyper_resource.abstract_collection_resource import AbstractCollectionResource


class SpatialCollectionResource(AbstractCollectionResource):
    def __init__(self, request):
        super().__init__(request)