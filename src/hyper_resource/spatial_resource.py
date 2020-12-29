from src.hyper_resource.abstract_resource import AbstractResource

class SpatialResource(AbstractResource):
    def __init__(self, request):
        super().__init__(request)