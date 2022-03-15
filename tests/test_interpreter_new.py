#(hyper-resource-sanic-JWRMp1xC-py3.7) C:\desenv\python-des\hyper-resource-sanic\tests>pytest -q test_filter_expression.py
from typing import Dict, Tuple, Sequence, List
import unittest
from sqlalchemy import Column, Integer, String
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm.attributes import InstrumentedAttribute
from geoalchemy2 import Geometry
from src.orm.database_postgis import DialectDbPostgis
from src.models.lim_unidade_federacao_a import LimUnidadeFederacaoA
import pytest
import asyncio

from src.orm.models import AlchemyBase
from src.url_interpreter.interpreter_new import InterpreterNew

SERVIDOR = "127.0.0.1"
PORTA= "8000"
"""
class UnidadeFederativa(AlchemyBase):
    __tablename__ = "lim_unidade_federacao_a"
    __table_args__ = {"schema": "bcim"}
    id = Column("id_objeto", Integer(), primary_key=True)
    nome = Column("nome", String(length=100), nullable=False)
    nomeabrev = Column("nomeabrev", String(length=60))
    geometriaaproximada = Column("geometriaaproximada", String(length=10))
    sigla = Column("sigla", String(length=3), nullable=False)
    geocodigo = Column("geocodigo", String(length=3))
    #sqlalchemy.Column("geom", Geometry("MULTIPOLYGON"))
"""

class TestInterpreterNew():
    db = DialectDbPostgis(None, LimUnidadeFederacaoA.__table__, LimUnidadeFederacaoA)
    """
    def test_nextWord(self):
        interp = InterpreterNew("/id/gt/5/and/id/lte/101", LimUnidadeFederacaoA, DialectDbPostgis)
        assert interp.nextWord() == "id"
        assert interp.nextWord() == "gt"
        assert interp.nextWord() == "5"
        assert interp.nextWord() == "and"
        assert interp.nextWord() == "id"
        assert interp.nextWord() == "lte"
        assert interp.nextWord() == "101"
        assert interp.nextWord() is None
        interp = Interpreter("/sigla/in/'rj','es','go'/and/geom/within/Point(1,2)", LimUnidadeFederacaoA, DialectDbPostgis)
        assert interp.nextWord() == "sigla"
        assert interp.nextWord() == "in"
        assert interp.nextWord() == "'rj','es','go'"
        assert interp.nextWord() == "and"
        assert interp.nextWord() == "geom"
        assert interp.nextWord() == "within"
        assert interp.nextWord() == "Point(1,2)"
        assert interp.nextWord() is None

    def test_iterate_token(self):
        st = 'geom/buffer/1.2/bbcontains/Point(1,2)'
        interp = InterpreterNew(st, LimUnidadeFederacaoA, DialectDbPostgis)
        assert interp.prev_token(0) == None
        assert interp.nextWord() == 'geom'
        assert interp.word == 'geom'
        assert interp.sub_expression == st
        assert interp.current_token().word == 'geom'
        assert interp.current_token().category == 'attribute'
        assert interp.current_token().tipe == Geometry
        interp.token = interp.current_token()
        interp.nextWord()
        assert interp.word == 'buffer'
        assert interp.current_token().word == 'buffer'
        assert interp.current_token().category == 'operation'
        assert interp.current_token().tipe == Geometry
        interp.token = interp.current_token()
        interp.nextWord()
        assert interp.word == '1.2'
        assert interp.current_token().word == '1.2'
        #assert interp.current_token().category == OPERATION_ARG_CATEGORY
        #assert interp.current_token().tipe == None
    """
    def test_words(self):

        s1 = "geom/buffer/1.2/bbcontains/Point(1,2)/"
        interp = InterpreterNew(s1, LimUnidadeFederacaoA, self.db)
        print(interp.words())
        assert len(interp.words()) == 5
        assert interp.words()[0] == 'geom' and interp.words()[1] == 'buffer' and interp.words()[2] == '1.2'
        assert interp.words()[3] == 'bbcontains' and interp.words()[4] == 'Point(1,2)'
        s1 = "geom/buffer/1.2/bbcontains/(/http://127.0.0.1/bc250/hidreletricas/1/)/"
        interp = InterpreterNew(s1, LimUnidadeFederacaoA, self.db)
        assert len(interp.words()) == 5
        assert interp.words()[0] == 'geom' and interp.words()[1] == 'buffer' and interp.words()[2] == '1.2'
        assert interp.words()[3] == 'bbcontains'
        assert interp.words()[4] == 'http://127.0.0.1/bc250/hidreletricas/1'
        s1 = "geom/buffer/1.2/bbcontains/(/http://127.0.0.1/bc250/hidreletricas/1/)/and/geom/within/geom1"
        interp = InterpreterNew(s1, LimUnidadeFederacaoA, self.db)
        assert len(interp.words()) == 9
        assert interp.words()[0] == 'geom' and interp.words()[1] == 'buffer' and interp.words()[2] == '1.2'
        assert interp.words()[3] == 'bbcontains'
        assert interp.words()[4] == 'http://127.0.0.1/bc250/hidreletricas/1'
        assert interp.words()[5] == 'and' and interp.words()[6] =='geom' and interp.words()[7] == 'within'
        assert interp.words()[8] == 'geom1'
        s = "api/bcim/aldeias-indigenas/filter/geom/within/(/http://127.0.0.1/bcim/unidades-federativas/ES/)/collect/geom/buffer/0.2/union/(/http://127.0.0.1/api/bcim/aldeias-indigenas/filter/geom/within/(/http://127.0.0.1//bcim/unidades-federativas/AM/)/collect/geom/buffer/0.2/)/"
        interp = InterpreterNew(s, LimUnidadeFederacaoA, self.db)
        assert interp.words()[0] == 'api' and interp.words()[1] == 'bcim' and interp.words()[2] == 'aldeias-indigenas'
        assert interp.words()[3] == 'filter' and interp.words()[4] == 'geom' and interp.words()[5] == 'within'
        assert interp.words()[6] == 'http://127.0.0.1/bcim/unidades-federativas/ES' and interp.words()[7] == 'collect' and interp.words()[8] == 'geom'
        assert interp.words()[9] == 'buffer' and interp.words()[10] == '0.2' and interp.words()[11] == 'union'
        #assert interp.words[12] == 'http://127.0.0.1/api/bcim/aldeias-indigenas/filter/geom/within/(/http://127.0.0.1//bcim/unidades-federativas/AM/)/'


    @pytest.mark.asyncio
    async def test_translate(self):

       interp = InterpreterNew("/id_objeto/gt/5/and/id_objeto/lte/101", LimUnidadeFederacaoA, self.db)
       assert await interp.translate() == "id_objeto>5 and id_objeto<=101"
       interp = InterpreterNew("/id_objeto/gt/5/and/id_objeto/lte/101/or/(/id_objeto/eq/200/and/sigla/eq/RJ/)/", LimUnidadeFederacaoA, self.db)
       assert await interp.translate() == "id_objeto>5 and id_objeto<=101 or  ( id_objeto=200 and sigla='RJ' ) "
       interp = InterpreterNew("/(/id_objeto/gt/5/and/id_objeto/lte/56407/)/or/(/id_objeto/eq/56406/and/sigla/eq/RJ/)/", LimUnidadeFederacaoA, self.db)
       assert await interp.translate() == " ( id_objeto>5 and id_objeto<=56407 )  or  ( id_objeto=56406 and sigla='RJ' ) "
       interp = InterpreterNew("/sigla/in/RJ,SP,MG,ES/", LimUnidadeFederacaoA, self.db)
       assert await interp.translate() == "sigla in ('RJ','SP','MG','ES')"
       interp = InterpreterNew("/(/id_objeto/gt/5/and/id_objeto/lte/101/)/or/(/id_objeto/eq/200/and/sigla/eq/RJ/)/and/sigla/in/RJ,SP,MG,ES/", LimUnidadeFederacaoA, self.db)
       assert await interp.translate() == " ( id_objeto>5 and id_objeto<=101 )  or  ( id_objeto=200 and sigla='RJ' )  and sigla in ('RJ','SP','MG','ES')"
       # interp = Interpreter(f"sigla/eq/(/http://{SERVIDOR}:{PORTA}/lim-unidade-federacao-a-list/56406/sigla/)/or/(/geocodigo/eq/31/)/", LimUnidadeFederacaoA, DialectDbPostgis)
       # assert await interp.translate() == "sigla= ( 'RJ' )  or  ( geocodigo='31' ) "
       #EXEMPLO: http://127.0.0.1:8000/lim-unidade-federacao-a-list/filter/geom/buffer/1.2/contains/Point(1,2)/and/sigla/in/RJ,ES,MG,SP

    @pytest.mark.asyncio
    async def test_translate_lookup(self):
        interp = InterpreterNew("/sigla/eq/MG", LimUnidadeFederacaoA, self.db)
        assert await interp.translate_lookup() == "sigla = 'MG' "
        interp = InterpreterNew("/id_objeto/gt/5/and/id_objeto/lte/101", LimUnidadeFederacaoA, self.db)
        assert await interp.translate_lookup() == "id_objeto > 5 and id_objeto <= 101 "
        interp = InterpreterNew("/id_objeto/gt/5/and/id_objeto/lte/101/or/(/id_objeto/eq/200/and/sigla/eq/RJ/)/",
                                LimUnidadeFederacaoA, self.db)
        assert await interp.translate_lookup() == "id_objeto > 5 and id_objeto <= 101 or ( id_objeto = 200 and sigla = 'RJ' ) "
        interp = InterpreterNew("/sigla/in/RJ,SP,MG,ES/", LimUnidadeFederacaoA, self.db)
        assert await interp.translate_lookup() == "sigla in ('RJ','SP','MG','ES') "
        interp = InterpreterNew(
            "/(/id_objeto/gt/5/and/id_objeto/lte/101/)/or/(/id_objeto/eq/200/and/sigla/eq/RJ/)/and/sigla/in/RJ,SP,MG,ES/",
            LimUnidadeFederacaoA, self.db)
        assert await interp.translate_lookup() == "( id_objeto > 5 and id_objeto <= 101 ) or ( id_objeto = 200 and sigla = 'RJ' ) and sigla in ('RJ','SP','MG','ES') "
        interp = InterpreterNew("/geom/transform/3005/area/gt/100000", LimUnidadeFederacaoA, self.db)
        assert await interp.translate_lookup() == "ST_Area(ST_Transform(geom,3005))> 100000.0 "
        interp = InterpreterNew("/geom/transform/3005/area/gt/100000/and/sigla/in/RJ,ES", LimUnidadeFederacaoA, self.db)
        assert await interp.translate_lookup() == "ST_Area(ST_Transform(geom,3005))> 100000.0 and sigla in ('RJ','ES') "
        interp = InterpreterNew("/(/geom/transform/3005/area/gt/100000/and/sigla/in/RJ,ES/)/", LimUnidadeFederacaoA, self.db)
        assert await interp.translate_lookup() == "( ST_Area(ST_Transform(geom,3005))> 100000.0 and sigla in ('RJ','ES') ) "
        interp = InterpreterNew("/(/geom/transform/3005/area/gt/100000/and/sigla/in/RJ,ES/)/or/geom/transform/3005/area/neq/100", LimUnidadeFederacaoA,
                                self.db)
        assert await interp.translate_lookup() == "( ST_Area(ST_Transform(geom,3005))> 100000.0 and sigla in ('RJ','ES') ) or ST_Area(ST_Transform(geom,3005))<> 100.0 "

    @pytest.mark.asyncio
    async def test_translate_collect(self):
        interp = InterpreterNew("", LimUnidadeFederacaoA, self.db)
        print("ererererer")
        collect: str = await interp.translate_collect('collect/sigla,nome&geom/transform/3005/area', '')
        assert collect == 'sigla as sigla,nome as nome, ST_Area(ST_Transform(geom,3005)) as area'
    # @pytest.mark.asyncio
    # async def test_translate_with_operation(self):
    #     interp = Interpreter("/geom/area/lt/10", LimUnidadeFederacaoA, DialectDbPostgis)
    #     assert await interp.translate() == "ST_Area(bcim.lim_unidade_federacao_a.geom)<10"

"""
@pytest.mark.asyncio
async def test_translate():
    interp = Interpreter("/id/gt/5/and/id/lte/101", UnidadeFederativa)
    res = await interp.translate()
    assert res == "id_objeto>5 and id_objeto<=101"
    interp = Interpreter(f"sigla/eq/(/http://{SERVIDOR}:{PORTA}/unidade-federacao-a-list/RJ/sigla/)/or/(/geocodigo/eq/"31"/)/",UnidadeFederacaoA)
    res = await interp.translate()
    assert res == "sigla='RJ' or ( geocodigo='31')"
"""
