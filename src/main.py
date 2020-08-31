# -*- coding: utf-8 -*-
import asyncio
from databases import Database
from environs import Env
from sanic import Sanic, response
from sanic.response import text
from sanic_openapi import swagger_blueprint
#from src.middlewares.security import setup_middlewares
from src.routes.setor_censitario import setor_censitario_routes
from src.routes.unidade_federativa import unidades_federativas_routes
from src.orm.database_postgresql import DialectDbPostgresql
import logging

#Create Sanic app
app = Sanic(__name__)
app.blueprint(swagger_blueprint)

#Setup env
env = Env()
env.read_env()  # read .env file, if it exists
port = env.str("PORT", "8000")
host = env.str("HOST", "127.0.0.1")
debug=env.bool("DEBUG", False)
access_log = env.bool("ACESS_LOG", False)
protocol = env.str("PROTOCOL", "http:")
echo=env.str("ECHO", "")

@app.middleware('request')
async def print_on_request(request):
    print(request.path)
   
@app.route('/')
def handle_request(request):
    print(app.db.url.dialect)
    porta = f":{port}"if port else ""
    return response.json({
        "unidades-federativas": f"{protocol}//{host}{porta}/unidades-federativas",
        "setores-censitarios": f"{protocol}//{host}{porta}/setores-censitarios",
    })

@app.listener('after_server_start')
async def connect_to_db(*args, **kwargs):
    print("Connection to database ...")
    await app.db.connect()
    print("Database connected")
    
@app.listener('after_server_stop')
async def disconnect_from_db(*args, **kwargs):
    await app.db.disconnect()

def setup_database():
    app.db = Database(env.str("URLDB"), ssl=False, min_size=1, max_size=20)
    app.db.echo= True
    app.dialect_db_class = DialectDbPostgresql
    #app.Session = sessionmaker(bind=app.db)

def setup_routes():
    setor_censitario_routes(app)
    unidades_federativas_routes(app) 

def init():
    #app.config.from_object(Settings)
    setup_database()
    setup_routes()

if __name__ == '__main__':
    init()
    
    print(f"Starting server at port: {port}")
    app.run(host=host, port=port, debug=False, access_log=False)
"""
@app.route('/string/<id:int>')
async def string_collection(request, id):
    print('/string/<id:int>' + ' => ' + str(id))
    return text("request.path: " + request.path + " request.url: " + request.url)
@app.route('/string/<id:int>/<predicate:path>')
async def string_collection(request, id, predicate):
    print('/string/<id:int>/<predicate:path> ' + str(id )+ ' path: ' + predicate)
    print(id)
    print(predicate)
    return text("request.path: " + request.path + " request.url: " + request.url)
@app.route('/string')
async def string_collection(request):
    print('/string')
    return text("request.path: " + request.path + " request.url: " + request.url)

@app.route('/string/<parameters:path>')
async def string_handler(request, parameters):
    print('/string/<parameters:path>' + ' => '+ parameters)
    return text("request.path: " + request.path + " request.url: " + request.url)
    #return text('String - {}'.format(string_arg))

@app.route('/int/<integer_arg:int>')
async def integer_handler(request, integer_arg):
    return text('Integer - {}'.format(integer_arg))

@app.route('/number/<number_arg:number>')
async def number_handler(request, number_arg):
    return text('Number - {}'.format(number_arg))

@app.route('/alpha/<alpha_arg:alpha>')
async def number_handler(request, alpha_arg):
    return text('Alpha - {}'.format(alpha_arg))

@app.route('/path/<path_arg:path>')
async def number_handler(request, path_arg):
    return text('Path - {}'.format(path_arg))

@app.route('/uuid/<uuid_arg:uuid>')
async def number_handler(request, uuid_arg):
    return text('Uuid - {}'.format(uuid_arg))

@app.route('/person/<name:[A-z]+>')
async def person_handler(request, name):
    return text('Person - {}'.format(name))

@app.route('/folder/<folder_id:[A-z0-9]{0,4}>')
async def folder_handler(request, folder_id):
    return text('Folder - {}'.format(folder_id))
"""