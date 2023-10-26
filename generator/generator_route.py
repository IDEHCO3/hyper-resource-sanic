from environs import Env
from generator.util import convert_camel_case_to_underline, convert_camel_case_to_hifen, convert_underline_to_camel_case
import os
#Setup env
from settings import ROUTERS_DIR

env = Env()
env.read_env()  # read .env file, if it exists
port = env.str("PORT", "8000")
host = env.str("HOST", "127.0.0.1")
debug=env.bool("DEBUG", False)
access_log = env.bool("ACESS_LOG", False)
protocol = env.str("PROTOCOL", "http:")

def get_template(file_name, file_name_hyfen, class_name):
    template = f"""from sanic.response import json
from src.middlewares.security import authentication,permission
from src.resources.{file_name} import {class_name}Resource, {class_name}CollectionResource

def {file_name}_routes(app):
    
    @app.route({class_name}Resource.router_id())
    async def {file_name}_id(request, id):
        r = {class_name}Resource(request)
        return await r.get_representation(id)
    
    @app.route({class_name}Resource.router_id_path())
    async def {file_name}_resource_id_path(request, id, path):
        r = {class_name}Resource(request)
        return await r.get_representation_given_path(id, path)

    @app.route({class_name}Resource.router_id(), methods=['HEAD'])
    async def head_{file_name}_id(request, id):
        r = {class_name}Resource(request)
        return await r.head(id)
    
    @app.route({class_name}Resource.router_id_path(), methods=['HEAD'])
    async def {file_name}_resource_id_path(request, id, path):
        r = {class_name}Resource(request)
        return await r.head_given_path(id, path)
    
    @app.route({class_name}Resource.router_id(), methods=['OPTIONS'])
    async def options_{file_name}_id(request, id):
        r = {class_name}Resource(request)
        return await r.options(id)
    
    @app.route({class_name}Resource.router_id_path(), methods=['OPTIONS'])
    async def options_{file_name}_resource_id_path(request, id, path):
        r = {class_name}Resource(request)
        return await r.options_given_path(id, path)
            
    @app.route({class_name}CollectionResource.router_list())
    async def {file_name}_list(request):
        cr = {class_name}CollectionResource(request)
        return await cr.get_representation()
        
    @app.route({class_name}CollectionResource.router_list_path())
    async def {file_name}_list_path(request, path):
        cr = {class_name}CollectionResource(request)
        return await cr.get_representation_given_path(path)

    @app.route({class_name}CollectionResource.router_list(), methods=['HEAD'] )
    async def head_{file_name}_list(request):
        cr = {class_name}CollectionResource(request)
        return await cr.head()

    @app.route({class_name}CollectionResource.router_list_path(), methods=['HEAD'] )
    async def head_{file_name}_list_path(request, path):
        cr = {class_name}CollectionResource(request)
        return await cr.head_given_path(path)
   
    @app.route({class_name}CollectionResource.router_list(), methods=['OPTIONS'] )
    async def options_{file_name}_list(request):
        cr = {class_name}CollectionResource(request)
        return await cr.options()

    @app.route({class_name}CollectionResource.router_list_path(), methods=['OPTIONS'] )
    async def options_{file_name}_list_path(request, path):
        cr = {class_name}CollectionResource(request)
        return await cr.options_given_path(path)     
"""
    return template
def get_template_patch(file_name, file_name_hyfen, class_name):
    return f"""
    @app.route({class_name}Resource.router_id(), methods=['PATCH'])
    @authentication()
    @permission()
    async def patch_{file_name}_id(request, id):
        r = {class_name}Resource(request)
        return await r.patch(id)
"""
def get_template_put(file_name, file_name_hyfen, class_name):
    return f"""
    @app.route({class_name}Resource.router_id(), methods=['PUT'])
    @authentication()
    @permission()
    async def put_{file_name}_id(request, id):
        r = {class_name}Resource(request)
        return await r.put(id)
"""

def get_template_post(file_name, file_name_hyfen, class_name):
    return f"""
    @app.route({class_name}CollectionResource.router_list(), methods=['POST'])
    @authentication()
    @permission()
    async def post_{file_name}(request):
        r = {class_name}CollectionResource(request)
        return await r.post()
"""

def get_template_delete(file_name, file_name_hyfen, class_name):
    return f"""
    @app.route({class_name}Resource.router_id(), methods=['DELETE'])
    @authentication()
    @permission()
    async def delete_{file_name}_id(request, id):
        r = {class_name}Resource(request)
        return await r.delete(id)
"""

def generate_route_file(path, file_name, file_name_hyfen, class_name, has_patch=False, has_post=False, has_delete=False):
    file_with_path = os.path.join(path, f'{file_name}.py')
    with open(file_with_path, 'w') as file:
        file.write(get_template(file_name, file_name_hyfen, class_name))
        if has_patch:
            file.write(get_template_patch(file_name, file_name_hyfen, class_name))
            file.write(get_template_put(file_name, file_name_hyfen, class_name))
        if has_post:
            file.write(get_template_post(file_name, file_name_hyfen, class_name))
        if has_delete:
            file.write(get_template_delete(file_name, file_name_hyfen, class_name))

def generate_entry_point_file(path, file_name, file_names_hyfen, class_names):
    file_with_path = os.path.join(path, f'{file_name}.py')
    with open(file_with_path, 'w') as file:
        file.write('from sanic.request import Request\n\n')
        file.write('def api_entry_point(request: Request):\n')
        file.write('    return {\n')
        for i in range(0, len(file_names_hyfen)):
            s = f'      "{file_names_hyfen[i]}-list": f"{protocol}//' + '{request.host}' + f':{port}/{file_names_hyfen[i]}-list",\n'
            file.write(s)
        file.write('    }\n')

def generate_setup_routes_file(path, file_name="setup_routes", file_names=[], class_names=[]):
    TAB = " " * 4
    file_with_path = os.path.join(path, f'{file_name}.py')
    with open(file_with_path, 'w') as file:
        file.write(f'from src.hyper_resource.abstract_resource import AbstractResource\n')
        for i in range(0, len(file_names)):
            file.write(f'from src.routes.{file_names[i]} import {file_names[i]}_routes\n')

        for i in range(0, len(file_names)):
            camel_case_name = convert_underline_to_camel_case(file_names[i])
            file.write(f'from src.resources.{file_names[i]} import {camel_case_name}Resource, {camel_case_name}CollectionResource\n')

        file.write('def setup_all_routes(app):\n')
        for i in range(0, len(file_names)):
            file.write(f'    {file_names[i]}_routes(app)\n')

        file.write(TAB + '\nAbstractResource.MAP_MODEL_FOR_ROUTE = {\n')
        for class_name in file_names:
            camel_case_name = convert_underline_to_camel_case(class_name)
            file.write((TAB * 2) + f"{camel_case_name}Resource.model_class: {class_name}_routes,\n")
        file.write(TAB + '}')

def generate_all_router_files(clsmembers, has_patch=False, has_post=False, has_delete=False):
    path = ROUTERS_DIR#os.path.join(os.getcwd(), 'src', 'routes')
    try:
        os.mkdir(path)
    except FileExistsError:
        pass
    for class_name_class in clsmembers:
        class_name = class_name_class[0]
        file_name = convert_camel_case_to_underline(class_name)
        file_name_hyfen = convert_camel_case_to_hifen(class_name)
        generate_route_file(path, file_name, file_name_hyfen, class_name, has_patch, has_post, has_delete)

def generate_all_entry_point_file(clsmembers):
    path = ROUTERS_DIR#os.path.join(os.getcwd(), 'src', 'routes')
    try:
        os.mkdir(path)
    except FileExistsError:
        pass
    class_names = [class_name_class[0] for class_name_class in clsmembers]
    file_names_hyfen = [convert_camel_case_to_hifen(class_name_class[0]) for class_name_class in clsmembers]
    generate_entry_point_file(path, "entry_point", file_names_hyfen, class_names)
    file_names = [convert_camel_case_to_underline(class_name_class[0]) for class_name_class in clsmembers]
    generate_setup_routes_file(path,"setup_routes",file_names, class_names)