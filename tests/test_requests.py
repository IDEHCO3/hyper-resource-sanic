# pytest -q --disable-pytest-warnings test_requests.py
import json
import pytest
from databases import Database
from sanic import Sanic, response
from sanic.request import Request
from settings import VOCAB_DIR
from src.orm.database_postgresql import DialectDbPostgresql
from src.resources.setup_resources import setup_all_resources
from src.routes.entry_point import api_entry_point
from src.routes.setup_routes import setup_all_routes
from src.aiohttp_client import ClientIOHTTP
from environs import Env
import aiohttp

CONTENT_TYPE_HEADER_KEY = "content-type"
APPLICATION_JSON_MIME_TYPE = "application/json"
APPLICATION_GEOJSON_MIME_TYPE = "application/geo+json"

FEATURE_TYPE_KEY = "type"
FEATURE_COLLECTION_TYPE_KEY = "type"
FEATURE_COLLECTION_FEATURES_KEY = "features"

# sudo apt-get install libpq5=10.19-0ubuntu0.18.04.1 # for ubuntu > 18.04 (before install GDAL)
# sudo apt-get install -y libpq-dev libgdal-dev
# need python > 3.7
# pip3 install setuptools==57.5.0 # fonte: https://stackoverflow.com/questions/69123406/error-building-pygdal-unknown-distribution-option-use-2to3-fixers-and-use-2

@pytest.fixture
def app():
    sanic_app = Sanic("HyperResource")

    env = Env()
    env.read_env()  # read .env file, if it exists
    port = env.str("PORT", "8002")
    host = env.str("HOST", "127.0.0.1")
    debug = env.bool("DEBUG", False)
    access_log = env.bool("ACESS_LOG", False)
    MIME_TYPE_JSONLD = "application/ld+json"

    @sanic_app.middleware("request")
    async def print_on_request(request):
        pass

    @sanic_app.route("/")
    def handle_request(request: Request):
        base_iri = request.scheme + '://' + request.host

        _headers = {'Access-Control-Expose-Headers': 'Link', 'Link': f'<{base_iri}>;rel=https://schema.org/EntryPoint'}
        print(_headers)
        # return response.json(api_entry_point())
        return response.json(api_entry_point(), headers=_headers, status=200)

    @sanic_app.route("/core")
    def handle_request(request: Request):
        return response.file(VOCAB_DIR, mime_type=MIME_TYPE_JSONLD)

    async def initIOHTTPSession(loop):
        ClientIOHTTP().session = aiohttp.ClientSession(loop=loop)  # app.aiohttp_session

    @sanic_app.listener('before_server_start')
    async def init_session(app, loop):
        app.aiohttp_session = aiohttp.ClientSession(loop=loop)
        await initIOHTTPSession(loop)
        print(ClientIOHTTP().session)

    @sanic_app.listener("after_server_start")
    async def connect_to_db(*args, **kwargs):
        print("Connection to database ...")
        await sanic_app.db.connect()
        print("Database connected")

    @sanic_app.listener('after_server_stop')
    async def finish(app, loop):
        await app.db.disconnect()
        # loop.close()

    def setup_database():
        sanic_app.db = Database(env.str("URLDB"), ssl=False, min_size=1, max_size=20)
        sanic_app.dialect_db_class = DialectDbPostgresql

    def setup_routes():
        setup_all_routes(sanic_app)

    def setup_resources():
        setup_all_resources()

    def init():
        setup_database()
        setup_resources()
        setup_routes()

    init()

    return sanic_app

# -------------------------------------------------- COMMOM FUNCTIONS --------------------------------------------------
def get_header_keys(response):
    return [header_key.lower() for header_key in list(response.headers.keys())]

def has_content_type_header(response):
    header_keys = get_header_keys(response)
    return CONTENT_TYPE_HEADER_KEY in header_keys

def is_content_type_json(response):
    return response.headers.get(CONTENT_TYPE_HEADER_KEY) == APPLICATION_JSON_MIME_TYPE

# ----------------------------------------------- COMMOM FUNCTIONS (END) -----------------------------------------------

# -------------------------------------------- FEATURE COLLECTION FUNCTIONS --------------------------------------------
def is_feature_collection_content(response):
    data = json.loads(response.body)
    return FEATURE_COLLECTION_TYPE_KEY in data and FEATURE_COLLECTION_FEATURES_KEY in data

def get_features_quantity(response):
    data = json.loads(response.body)
    return len(data[FEATURE_COLLECTION_FEATURES_KEY])
# ----------------------------------------- FEATURE COLLECTION FUNCTIONS (END) -----------------------------------------

def test_basic_api_entrypoint(app):
    request, response = app.test_client.get("/")

    assert request.method.lower() == "get"
    assert json.loads(response.body) == api_entry_point()
    assert response.status == 200

# http://localhost:8000/lim-unidade-federacao-a-list
def test_basic_feature_collection(app):
    request, response = app.test_client.get("/lim-unidade-federacao-a-list")

    assert request.method.lower() == "get"
    assert CONTENT_TYPE_HEADER_KEY in get_header_keys(response)
    # assert response.headers.get(CONTENT_TYPE_HEADER_KEY) == APPLICATION_GEOJSON_MIME_TYPE
    assert is_feature_collection_content(response) == True
    assert get_features_quantity(response) == 27
    assert response.status == 200