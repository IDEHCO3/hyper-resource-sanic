from sanic.response import json
from src.middlewares.security import authentication,permission
from tests.resources.terra_indigena import TerraIndigenaResource, TerraIndigenaCollectionResource

def terra_indigena_routes(app):
    
    @app.route(TerraIndigenaResource.router_id())
    async def terra_indigena_id(request, id):
        r = TerraIndigenaResource(request)
        return await r.get_representation(id)
    
    @app.route(TerraIndigenaResource.router_id_path())
    async def terra_indigena_resource_id_path(request, id, path):
        r = TerraIndigenaResource(request)
        return await r.get_representation_given_path(id, path)

    @app.route(TerraIndigenaResource.router_id(), methods=['HEAD'])
    async def head_terra_indigena_id(request, id):
        r = TerraIndigenaResource(request)
        return await r.head(id)
    
    @app.route(TerraIndigenaResource.router_id_path(), methods=['HEAD'])
    async def terra_indigena_resource_id_path(request, id, path):
        r = TerraIndigenaResource(request)
        return await r.head_given_path(id, path)
    
    @app.route(TerraIndigenaResource.router_id(), methods=['OPTIONS'])
    async def options_terra_indigena_id(request, id):
        r = TerraIndigenaResource(request)
        return await r.options(id)
    
    @app.route(TerraIndigenaResource.router_id_path(), methods=['OPTIONS'])
    async def options_terra_indigena_resource_id_path(request, id, path):
        r = TerraIndigenaResource(request)
        return await r.options_given_path(id, path)
            
    @app.route(TerraIndigenaCollectionResource.router_list())
    async def terra_indigena_list(request):
        cr = TerraIndigenaCollectionResource(request)
        return await cr.get_representation()
        
    @app.route(TerraIndigenaCollectionResource.router_list_path())
    async def terra_indigena_list_path(request, path):
        cr = TerraIndigenaCollectionResource(request)
        return await cr.get_representation_given_path(path)

    @app.route(TerraIndigenaCollectionResource.router_list(), methods=['HEAD'] )
    async def head_terra_indigena_list(request):
        cr = TerraIndigenaCollectionResource(request)
        return await cr.head()

    @app.route(TerraIndigenaCollectionResource.router_list_path(), methods=['HEAD'] )
    async def head_terra_indigena_list_path(request, path):
        cr = TerraIndigenaCollectionResource(request)
        return await cr.head_given_path(path)
   
    @app.route(TerraIndigenaCollectionResource.router_list(), methods=['OPTIONS'] )
    async def options_terra_indigena_list(request):
        cr = TerraIndigenaCollectionResource(request)
        return await cr.options()

    @app.route(TerraIndigenaCollectionResource.router_list_path(), methods=['OPTIONS'] )
    async def options_terra_indigena_list_path(request, path):
        cr = TerraIndigenaCollectionResource(request)
        return await cr.options_given_path(path)     

    @app.route(TerraIndigenaResource.router_id(), methods=['PATCH'])
    @authentication()
    @permission()
    async def patch_terra_indigena_id(request, id):
        r = TerraIndigenaResource(request)
        return await r.patch(id)

    @app.route(TerraIndigenaResource.router_id(), methods=['PUT'])
    @authentication()
    @permission()
    async def put_terra_indigena_id(request, id):
        r = TerraIndigenaResource(request)
        return await r.put(id)

    @app.route(TerraIndigenaCollectionResource.router_list(), methods=['POST'])
    @authentication()
    @permission()
    async def post_terra_indigena(request):
        r = TerraIndigenaCollectionResource(request)
        return await r.post()

    @app.route(TerraIndigenaResource.router_id(), methods=['DELETE'])
    @authentication()
    @permission()
    async def delete_terra_indigena_id(request, id):
        r = TerraIndigenaResource(request)
        return await r.delete(id)
