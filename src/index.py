import aiohttp
#import matplotlib.pyplot as plt
from aiohttp import ClientSession
from databases import Database
from environs import Env
from sanic import Sanic, response
from sanic.request import Request
from sanic.response import text
from sanic_openapi import swagger_blueprint

from settings import VOCAB_DIR
from src.aiohttp_client import ClientIOHTTP
from src.orm.database_postgis import DialectDbPostgis
from src.resources.setup_resources import setup_all_resources
from src.routes.setup_routes import setup_all_routes
from src.routes.entry_point import api_entry_point
from src.orm.database_postgresql import DialectDbPostgresql
from sanic_cors import CORS, cross_origin

#Create Sanic app
app = Sanic(__name__)
CORS(app, automatic_options=False)
# app.blueprint(swagger_blueprint)
#Setup env
env = Env()
env.read_env()  # read .env file, if it exists
port = env.str("PORT", "8002")
host = env.str("HOST", "127.0.0.1")
debug=env.bool("DEBUG", False)
access_log = env.bool("ACESS_LOG", False)
MIME_TYPE_JSONLD = "application/ld+json"

@app.middleware("request")
async def print_on_request(request):
    pass

def get_entry_point_header(request: Request):
    base_iri = request.scheme + '://' + request.host
    _headers = {
        'Access-Control-Expose-Headers': 'Link',
        'Link': f"<{base_iri}>; rel=\"https://schema.org/EntryPoint\", "
                f"<{base_iri}.jsonld>; rel=\"http://www.w3.org/ns/json-ld#context\"; type=\"application/ld+json\""
    }
    return _headers

@app.route("/", methods=["GET"])
def handle_request(request: Request):
    return response.json(api_entry_point(), headers=get_entry_point_header(request), status=200)

@app.route("/", methods=["OPTIONS"])
def handle_request_options(request: Request):
    return response.json(api_entry_point_context(api_entry_point()), headers=get_entry_point_header(request), status=200)
    # return response.json(api_entry_point(), headers=_headers, status=200)

@app.route("/", methods=["HEAD"])
def handle_request_options(request: Request):
    return response.empty(headers=get_entry_point_header(request), status=200)
def api_entry_point_context(entry_point_content):
    d = {
        "@context": {
            "schema": "https://schema.org/",
            "geojson": "https://purl.org/geojson/vocab#",
        }
    }
    for key, value in entry_point_content.items():
        d["@context"].update({
            key: {
                "@id": "geojson:FeatureCollection",
                "@type": "@id",
                # key: value
            }
        })
    return d

@app.route("/core")
def handle_request(request: Request):
    return response.file(VOCAB_DIR, mime_type=MIME_TYPE_JSONLD)

async def initIOHTTPSession(loop):
    ClientIOHTTP().session = aiohttp.ClientSession(loop=loop)  # app.aiohttp_session

@app.listener('before_server_start')
async def init_session(app, loop):
    app.aiohttp_session = aiohttp.ClientSession(loop=loop)
    await initIOHTTPSession(loop)
    print(ClientIOHTTP().session)

@app.listener("after_server_start")
async def connect_to_db(*args, **kwargs):
    print("Connection to database ...")
    await app.db.connect()
    print("Database connected")

    
#@app.listener("after_server_stop")
#async def disconnect_from_db(*args, **kwargs):
#    await app.db.disconnect()
@app.listener('after_server_stop')
async def finish(app, loop):
    await app.db.disconnect()
    loop.close()

def setup_database():
    app.db = Database(env.str("URLDB"), ssl=False, min_size=1, max_size=20)
    app.dialect_db_class = DialectDbPostgresql
    
def setup_routes():
    setup_all_routes(app)

def setup_resources():
    setup_all_resources()
    
def init():
    setup_database()
    setup_resources()
    setup_routes()

if __name__ == "__main__":
    init()
    print(f"Starting server at port: {port}")
    app.run(host=host, port=port, debug=True, access_log=True)
