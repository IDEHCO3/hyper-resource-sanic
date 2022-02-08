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

def test_basic_test_client(app):
    request, response = app.test_client.get("/")

    assert request.method.lower() == "get"
    # assert response.body == b"foo"
    assert response.status == 200