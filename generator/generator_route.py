from environs import Env
from generator.util import convert_camel_case_to_underline, convert_camel_case_to_hifen
import os
#Setup env
env = Env()
env.read_env()  # read .env file, if it exists
port = env.str("PORT", "8000")
host = env.str("HOST", "127.0.0.1")
debug=env.bool("DEBUG", False)
access_log = env.bool("ACESS_LOG", False)
protocol = env.str("PROTOCOL", "http:")

def get_template(file_name, file_name_hyfen, class_name):
    template = f"""from sanic.response import json
from src.resources.{file_name} import {class_name}Resource, {class_name}CollectionResource

def {file_name}_routes(app):
    
    @app.route('/{file_name_hyfen}-list/<id:int>')
    async def {file_name}_id(request, id):
        r = {class_name}Resource(request)
        return await r.get_representation(id)
    
    @app.route('/{file_name_hyfen}-list/<id:int>/<path:path>')
    async def {file_name}_resource_id_path(request, id, path):
        r = {class_name}Resource(request)
        return await r.get_representation(id, path)

    @app.route("/{file_name_hyfen}-list")
    async def {file_name}_list(request):
        cr = {class_name}CollectionResource(request)
        return await cr.get_representation()
        
    @app.route("/{file_name_hyfen}-list/<path:path>")
    async def {file_name}_list_path(request, path):
        cr = {class_name}CollectionResource(request)
        return await cr.get_representation_given_path(path)

    @app.route("/{file_name_hyfen}-list", methods=['HEAD'] )
    async def head_{file_name}_list(request):
        cr = {class_name}CollectionResource(request)
        return await cr.head()

    @app.route("/{file_name_hyfen}-list/<path:path>", methods=['HEAD'] )
    async def head_{file_name}_list_path(request, path):
        cr = {class_name}CollectionResource(request)
        return await cr.head_given_path(path)
"""
    return template

def generate_route_file(path, file_name, file_name_hyfen, class_name):
    file_with_path = os.path.join(path, f'{file_name}.py')
    with open(file_with_path, 'w') as file:
        file.write(get_template(file_name, file_name_hyfen, class_name))

def generate_entry_point_file(path, file_name, file_names_hyfen, class_names):
    file_with_path = os.path.join(path, f'{file_name}.py')
    with open(file_with_path, 'w') as file:
        file.write('def api_entry_point():\n')
        file.write('    return {\n')
        for i in range(0, len(file_names_hyfen)):
            s = f'      "{file_names_hyfen[i]}-list": "{protocol}//{host}:{port}/{file_names_hyfen[i]}-list",\n'
            file.write(s)
        file.write('    }\n')

def generate_setup_routes_file(path, file_name="setup_routes", file_names=[], class_names=[]):
    file_with_path = os.path.join(path, f'{file_name}.py')
    with open(file_with_path, 'w') as file:
        for i in range(0, len(file_names)):
            file.write(f'from src.routes.{file_names[i]} import {file_names[i]}_routes\n')
        file.write('def setup_all_routes(app):\n')
        for i in range(0, len(file_names)):
            file.write(f'    {file_names[i]}_routes(app)\n')

def generate_all_router_files(clsmembers):
    path = os.path.join(os.getcwd(), 'src', 'routes')
    try:
        os.mkdir(path)
    except FileExistsError:
        pass
    for class_name_class in clsmembers:
        class_name = class_name_class[0]
        file_name = convert_camel_case_to_underline(class_name)
        file_name_hyfen = convert_camel_case_to_hifen(class_name)
        generate_route_file(path, file_name, file_name_hyfen, class_name)

def generate_all_entry_point_file(clsmembers):
    path = os.path.join(os.getcwd(), 'src', 'routes')
    try:
        os.mkdir(path)
    except FileExistsError:
        pass
    class_names = [class_name_class[0] for class_name_class in clsmembers]
    file_names_hyfen = [convert_camel_case_to_hifen(class_name_class[0]) for class_name_class in clsmembers]
    generate_entry_point_file(path, "entry_point", file_names_hyfen, class_names)
    file_names = [convert_camel_case_to_underline(class_name_class[0]) for class_name_class in clsmembers]
    generate_setup_routes_file(path,"setup_routes",file_names, class_names)