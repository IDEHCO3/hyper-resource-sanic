
import asyncio
from databases import Database
from environs import Env
from sanic import Sanic, response
from sanic.response import text
from sanic_openapi import swagger_blueprint
from src.routes.setup_routes import setup_all_routes
from src.routes.entry_point import api_entry_point
from src.orm.database_postgresql import DialectDbPostgresql
from sanic_cors import CORS, cross_origin

#Create Sanic app
app = Sanic(__name__)
CORS(app)
app.blueprint(swagger_blueprint)

#Setup env
env = Env()
env.read_env()  # read .env file, if it exists
port = env.str("PORT", "8002")
host = env.str("HOST", "127.0.0.1")
debug=env.bool("DEBUG", False)
access_log = env.bool("ACESS_LOG", False)

@app.middleware("request")
async def print_on_request(request):
    pass
   
@app.route("/")
def handle_request(request):
    return response.json(api_entry_point())

@app.listener("after_server_start")
async def connect_to_db(*args, **kwargs):
    print("Connection to database ...")
    await app.db.connect()
    print("Database connected")
    
@app.listener("after_server_stop")
async def disconnect_from_db(*args, **kwargs):
    await app.db.disconnect()

def setup_database():
    app.db = Database(env.str("URLDB"), ssl=False, min_size=1, max_size=20)
    app.dialect_db_class = DialectDbPostgresql
    
def setup_routes():
    setup_all_routes(app)
    
def init():
    setup_database()
    setup_routes()

if __name__ == "__main__":
    init()
    print(f"Starting server at port: {port}")
    app.run(host=host, port=port, debug=True, access_log=True)