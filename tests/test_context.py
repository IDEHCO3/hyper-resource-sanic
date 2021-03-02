#  pytest -q test_context.py
import json
from unittest import TestCase

from databases import Database

from src.contexts.con_gasto import ConGastoCollectionContext
from src.contexts.lim_unidade_federacao_a import LimUnidadeFederacaoACollectionContext
from src.hyper_resource.abstract_resource import AbstractResource
from src.models.con_gasto import ConGasto
from src.models.con_tipo_gasto import ConTipoGasto
from src.models.con_usuario import ConUsuario
from src.models.lim_unidade_federacao_a import LimUnidadeFederacaoA
from src.orm.database_postgis import DialectDbPostgis
from environs import Env

from src.resources.con_gasto import ConGastoResource
from src.resources.con_tipo_gasto import ConTipoGastoResource
from src.resources.con_usuario import ConUsuarioResource

env = Env()
env.read_env()  # read .env file, if it exists
port = env.str("PORT", "8002")
host = env.str("HOST", "127.0.0.1")
debug=env.bool("DEBUG", False)
access_log = env.bool("ACESS_LOG", False)



EXPECTED_GEO_CONTEXT = {
    "@context": {
        "geojson": "https://purl.org/geojson/vocab#",
        "Feature": "geojson:Feature",
        "coordinates": {
            "@container": "@list",
            "@id": "geojson:coordinates"
        },
        "type": "@type",
        "geometry": "geojson:geometry",
        "properties": "geojson:properties",
        "hr": "http://127.0.0.1:8000/core",
        "schema": "http://schema.org/",
        "Multipolygon": "geojson:Multipolygon",
        "id_objeto": "schema:Integer",
        "nome": "schema:Text",
        "nomeabrev": "schema:Text",
        "geometriaaproximada": "schema:Text",
        "sigla": "schema:Text",
        "geocodigo": "schema:Text",
        "id_produtor": "schema:Integer",
        "id_elementoprodutor": "schema:Integer",
        "cd_insumo_orgao": "schema:Integer",
        "nr_insumo_mes": "schema:Integer",
        "nr_insumo_ano": "schema:Integer",
        "tx_insumo_documento": "schema:Text",
        "features": {
            "@container": "@set",
            "@id": "geojson:features"
        }
    }
}

EXPECTED_RELATIONSHIP_CONTEXT = {
    "@context": {
        "hr": "http://127.0.0.1:8000/core",
        "schema": "http://schema.org/",
        "id": "schema:Integer",
        "data": "schema:Date",
        "tipo_gasto": {
            "@type": "@id",
            "@id": "schema:Thing"
        },
        "usuario": {
            "@type": "@id",
            "@id": "schema:Person"
        },
        "valor": "schema:Float",
        "detalhe": "schema:Text"
    }
}

class TestBasicContext():
    def test_simple_path_context(self):
        dialect = DialectDbPostgis(Database(env.str("URLDB"), ssl=False, min_size=1, max_size=20), LimUnidadeFederacaoA.__table__, LimUnidadeFederacaoA )

        context = LimUnidadeFederacaoACollectionContext(
            dialect,
            LimUnidadeFederacaoA.__table__,
            LimUnidadeFederacaoA
        ).get_basic_context()

        TestCase().assertDictEqual(EXPECTED_GEO_CONTEXT, context)
        # assert json.dumps(context) == json.dumps(EXPECTED_CONTEXT)

    def test_relationship_context(self):
        AbstractResource.MAP_MODEL_FOR_CONTEXT = {
            ConGastoResource.model_class: ConGastoResource.context_class,
            ConTipoGastoResource.model_class: ConTipoGastoResource.context_class,
            ConUsuarioResource.model_class: ConUsuarioResource.context_class,
        }
        dialect = DialectDbPostgis(Database(env.str("URLDB"), ssl=False, min_size=1, max_size=20), ConGasto.__table__, ConGasto )

        context = ConGastoCollectionContext(dialect, ConGasto.__table__, ConGasto).get_basic_context()

        TestCase().assertDictEqual(EXPECTED_RELATIONSHIP_CONTEXT, context)