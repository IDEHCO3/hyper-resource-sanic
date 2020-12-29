from src.hyper_resource.spatial_resource import SpatialResource


class FeatureResource(SpatialResource):
    def __init__(self, request):
        super().__init__(request)