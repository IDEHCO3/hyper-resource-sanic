from sanic.response import json
from src.middlewares.security import authentication,permission
from tests.resources.ferrovia import FerroviaResource, FerroviaCollectionResource

def ferrovia_routes(app):
    
    @app.route(FerroviaResource.router_id())
    async def ferrovia_id(request, id):
        r = FerroviaResource(request)
        return await r.get_representation(id)
    
    @app.route(FerroviaResource.router_id_path())
    async def ferrovia_resource_id_path(request, id, path):
        r = FerroviaResource(request)
        return await r.get_representation_given_path(id, path)

    @app.route(FerroviaResource.router_id(), methods=['HEAD'])
    async def head_ferrovia_id(request, id):
        r = FerroviaResource(request)
        return await r.head(id)
    
    @app.route(FerroviaResource.router_id_path(), methods=['HEAD'])
    async def ferrovia_resource_id_path(request, id, path):
        r = FerroviaResource(request)
        return await r.head_given_path(id, path)
    
    @app.route(FerroviaResource.router_id(), methods=['OPTIONS'])
    async def options_ferrovia_id(request, id):
        r = FerroviaResource(request)
        return await r.options(id)
    
    @app.route(FerroviaResource.router_id_path(), methods=['OPTIONS'])
    async def options_ferrovia_resource_id_path(request, id, path):
        r = FerroviaResource(request)
        return await r.options_given_path(id, path)
            
    @app.route(FerroviaCollectionResource.router_list())
    async def ferrovia_list(request):
        cr = FerroviaCollectionResource(request)
        return await cr.get_representation()
        
    @app.route(FerroviaCollectionResource.router_list_path())
    async def ferrovia_list_path(request, path):
        cr = FerroviaCollectionResource(request)
        return await cr.get_representation_given_path(path)

    @app.route(FerroviaCollectionResource.router_list(), methods=['HEAD'] )
    async def head_ferrovia_list(request):
        cr = FerroviaCollectionResource(request)
        return await cr.head()

    @app.route(FerroviaCollectionResource.router_list_path(), methods=['HEAD'] )
    async def head_ferrovia_list_path(request, path):
        cr = FerroviaCollectionResource(request)
        return await cr.head_given_path(path)
   
    @app.route(FerroviaCollectionResource.router_list(), methods=['OPTIONS'] )
    async def options_ferrovia_list(request):
        cr = FerroviaCollectionResource(request)
        return await cr.options()

    @app.route(FerroviaCollectionResource.router_list_path(), methods=['OPTIONS'] )
    async def options_ferrovia_list_path(request, path):
        cr = FerroviaCollectionResource(request)
        return await cr.options_given_path(path)     

    @app.route(FerroviaResource.router_id(), methods=['PATCH'])
    @authentication()
    @permission()
    async def patch_ferrovia_id(request, id):
        r = FerroviaResource(request)
        return await r.patch(id)

    @app.route(FerroviaResource.router_id(), methods=['PUT'])
    @authentication()
    @permission()
    async def put_ferrovia_id(request, id):
        r = FerroviaResource(request)
        return await r.put(id)

    @app.route(FerroviaCollectionResource.router_list(), methods=['POST'])
    @authentication()
    @permission()
    async def post_ferrovia(request):
        r = FerroviaCollectionResource(request)
        return await r.post()

    @app.route(FerroviaResource.router_id(), methods=['DELETE'])
    @authentication()
    @permission()
    async def delete_ferrovia_id(request, id):
        r = FerroviaResource(request)
        return await r.delete(id)
