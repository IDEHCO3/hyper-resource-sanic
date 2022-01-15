from sanic.response import json
from src.middlewares.security import authentication,permission
from tests.resources.hidreletrica import HidreletricaResource, HidreletricaCollectionResource

def hidreletrica_routes(app):
    
    @app.route(HidreletricaResource.router_id())
    async def hidreletrica_id(request, id):
        r = HidreletricaResource(request)
        return await r.get_representation(id)
    
    @app.route(HidreletricaResource.router_id_path())
    async def hidreletrica_resource_id_path(request, id, path):
        r = HidreletricaResource(request)
        return await r.get_representation_given_path(id, path)

    @app.route(HidreletricaResource.router_id(), methods=['HEAD'])
    async def head_hidreletrica_id(request, id):
        r = HidreletricaResource(request)
        return await r.head(id)
    
    @app.route(HidreletricaResource.router_id_path(), methods=['HEAD'])
    async def hidreletrica_resource_id_path(request, id, path):
        r = HidreletricaResource(request)
        return await r.head_given_path(id, path)
    
    @app.route(HidreletricaResource.router_id(), methods=['OPTIONS'])
    async def options_hidreletrica_id(request, id):
        r = HidreletricaResource(request)
        return await r.options(id)
    
    @app.route(HidreletricaResource.router_id_path(), methods=['OPTIONS'])
    async def options_hidreletrica_resource_id_path(request, id, path):
        r = HidreletricaResource(request)
        return await r.options_given_path(id, path)
            
    @app.route(HidreletricaCollectionResource.router_list())
    async def hidreletrica_list(request):
        cr = HidreletricaCollectionResource(request)
        return await cr.get_representation()
        
    @app.route(HidreletricaCollectionResource.router_list_path())
    async def hidreletrica_list_path(request, path):
        cr = HidreletricaCollectionResource(request)
        return await cr.get_representation_given_path(path)

    @app.route(HidreletricaCollectionResource.router_list(), methods=['HEAD'] )
    async def head_hidreletrica_list(request):
        cr = HidreletricaCollectionResource(request)
        return await cr.head()

    @app.route(HidreletricaCollectionResource.router_list_path(), methods=['HEAD'] )
    async def head_hidreletrica_list_path(request, path):
        cr = HidreletricaCollectionResource(request)
        return await cr.head_given_path(path)
   
    @app.route(HidreletricaCollectionResource.router_list(), methods=['OPTIONS'] )
    async def options_hidreletrica_list(request):
        cr = HidreletricaCollectionResource(request)
        return await cr.options()

    @app.route(HidreletricaCollectionResource.router_list_path(), methods=['OPTIONS'] )
    async def options_hidreletrica_list_path(request, path):
        cr = HidreletricaCollectionResource(request)
        return await cr.options_given_path(path)     

    @app.route(HidreletricaResource.router_id(), methods=['PATCH'])
    @authentication()
    @permission()
    async def patch_hidreletrica_id(request, id):
        r = HidreletricaResource(request)
        return await r.patch(id)

    @app.route(HidreletricaResource.router_id(), methods=['PUT'])
    @authentication()
    @permission()
    async def put_hidreletrica_id(request, id):
        r = HidreletricaResource(request)
        return await r.put(id)

    @app.route(HidreletricaCollectionResource.router_list(), methods=['POST'])
    @authentication()
    @permission()
    async def post_hidreletrica(request):
        r = HidreletricaCollectionResource(request)
        return await r.post()

    @app.route(HidreletricaResource.router_id(), methods=['DELETE'])
    @authentication()
    @permission()
    async def delete_hidreletrica_id(request, id):
        r = HidreletricaResource(request)
        return await r.delete(id)
