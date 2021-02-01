from src.hyper_resource.abstract_resource import AbstractResource
from src.hyper_resource.context.geocontext import GeoDetailContext


class SpatialResource(AbstractResource):
    def __init__(self, request):
        super().__init__(request)
        self.context_class = GeoDetailContext