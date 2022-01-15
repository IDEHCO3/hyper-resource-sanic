from sanic.response import json
from src.middlewares.security import authentication,permission
from tests.resources.unidade_federacao import UnidadeFederacaoResource, UnidadeFederacaoCollectionResource

def unidade_federacao_routes(app):
    
    @app.route(UnidadeFederacaoResource.router_id())
    async def unidade_federacao_id(request, id):
        r = UnidadeFederacaoResource(request)
        return await r.get_representation(id)
    
    @app.route(UnidadeFederacaoResource.router_id_path())
    async def unidade_federacao_resource_id_path(request, id, path):
        r = UnidadeFederacaoResource(request)
        return await r.get_representation_given_path(id, path)

    @app.route(UnidadeFederacaoResource.router_id(), methods=['HEAD'])
    async def head_unidade_federacao_id(request, id):
        r = UnidadeFederacaoResource(request)
        return await r.head(id)
    
    @app.route(UnidadeFederacaoResource.router_id_path(), methods=['HEAD'])
    async def unidade_federacao_resource_id_path(request, id, path):
        r = UnidadeFederacaoResource(request)
        return await r.head_given_path(id, path)
    
    @app.route(UnidadeFederacaoResource.router_id(), methods=['OPTIONS'])
    async def options_unidade_federacao_id(request, id):
        r = UnidadeFederacaoResource(request)
        return await r.options(id)
    
    @app.route(UnidadeFederacaoResource.router_id_path(), methods=['OPTIONS'])
    async def options_unidade_federacao_resource_id_path(request, id, path):
        r = UnidadeFederacaoResource(request)
        return await r.options_given_path(id, path)
            
    @app.route(UnidadeFederacaoCollectionResource.router_list())
    async def unidade_federacao_list(request):
        cr = UnidadeFederacaoCollectionResource(request)
        return await cr.get_representation()
        
    @app.route(UnidadeFederacaoCollectionResource.router_list_path())
    async def unidade_federacao_list_path(request, path):
        cr = UnidadeFederacaoCollectionResource(request)
        return await cr.get_representation_given_path(path)

    @app.route(UnidadeFederacaoCollectionResource.router_list(), methods=['HEAD'] )
    async def head_unidade_federacao_list(request):
        cr = UnidadeFederacaoCollectionResource(request)
        return await cr.head()

    @app.route(UnidadeFederacaoCollectionResource.router_list_path(), methods=['HEAD'] )
    async def head_unidade_federacao_list_path(request, path):
        cr = UnidadeFederacaoCollectionResource(request)
        return await cr.head_given_path(path)
   
    @app.route(UnidadeFederacaoCollectionResource.router_list(), methods=['OPTIONS'] )
    async def options_unidade_federacao_list(request):
        cr = UnidadeFederacaoCollectionResource(request)
        return await cr.options()

    @app.route(UnidadeFederacaoCollectionResource.router_list_path(), methods=['OPTIONS'] )
    async def options_unidade_federacao_list_path(request, path):
        cr = UnidadeFederacaoCollectionResource(request)
        return await cr.options_given_path(path)     

    @app.route(UnidadeFederacaoResource.router_id(), methods=['PATCH'])
    @authentication()
    @permission()
    async def patch_unidade_federacao_id(request, id):
        r = UnidadeFederacaoResource(request)
        return await r.patch(id)

    @app.route(UnidadeFederacaoResource.router_id(), methods=['PUT'])
    @authentication()
    @permission()
    async def put_unidade_federacao_id(request, id):
        r = UnidadeFederacaoResource(request)
        return await r.put(id)

    @app.route(UnidadeFederacaoCollectionResource.router_list(), methods=['POST'])
    @authentication()
    @permission()
    async def post_unidade_federacao(request):
        r = UnidadeFederacaoCollectionResource(request)
        return await r.post()

    @app.route(UnidadeFederacaoResource.router_id(), methods=['DELETE'])
    @authentication()
    @permission()
    async def delete_unidade_federacao_id(request, id):
        r = UnidadeFederacaoResource(request)
        return await r.delete(id)
