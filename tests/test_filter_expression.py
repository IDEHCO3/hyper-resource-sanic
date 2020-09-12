#(hyper-resource-sanic-JWRMp1xC-py3.7) C:\desenv\python-des\hyper-resource-sanic\tests>pytest -q  test_filter_expression.py
from typing import Dict, Tuple, Sequence, List
import unittest
from sqlalchemy import Column, Integer, String
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm.attributes import InstrumentedAttribute
from src.url_interpreter.interpreter import *
from src.models.unidade_federacao_a import *
import pytest
import asyncio
Base = declarative_base()
class AlchemyBase:
    @classmethod     
    def schema(cls) -> str:
        return cls.__table_args__ ["schema"]
    @classmethod
    def table_name(cls) -> str:
        return cls.__table__.name

    @classmethod
    def primary_key(cls) -> str:
        return next(c.key for c in cls.__table__.columns if c.primary_key)

    @classmethod
    def attribute_names(cls) ->List[str]:
        return [ value.key for key, value in cls.__dict__.items() if isinstance(value, InstrumentedAttribute)]
    
    @classmethod
    def has_attribute(cls, attribute_name) -> bool:
        return attribute_name in cls.attribute_names()

    @classmethod
    def attribute_column_type(cls, attribute_name) -> tuple:
        lst_a_c_t = cls.list_attribute_column_type()
        return next(a_c_t for a_c_t in lst_a_c_t if a_c_t[0] == attribute_name)
        #next((x for x in lst if ...), [default value])

    @classmethod
    def list_attribute_column(cls) -> List[Tuple]:
        return [ (key, value.prop.columns[0].name) for key, value in cls.__dict__.items() if isinstance(value, InstrumentedAttribute)]

    @classmethod
    def list_attribute_column_type(cls) -> List[Tuple]:
        return [(key, value.prop.columns[0].name, value.prop.columns[0].type.__str__()) for key, value in cls.__dict__.items() if isinstance(value, InstrumentedAttribute)]

    @classmethod
    def column_names(cls)-> List[str]:
        return [col.name for col in cls.__table__.columns]
    
    @classmethod
    def column_names_as_enum(cls) -> str:
        return ",".join(cls.columns_name())
SERVIDOR = "127.0.0.1"
PORTA= "8002"
class UnidadeFederativa(AlchemyBase, Base):
    __tablename__ = "lim_unidade_federacao_a"
    __table_args__ = {"schema": "bcim"}
    id = Column("id_objeto", Integer(), primary_key=True)
    nome = Column("nome", String(length=100), nullable=False)
    nomeabrev = Column("nomeabrev", String(length=60))
    geometriaaproximada = Column("geometriaaproximada", String(length=10))
    sigla = Column("sigla", String(length=3), nullable=False)
    geocodigo = Column("geocodigo", String(length=3))
    #sqlalchemy.Column("geom", Geometry("MULTIPOLYGON"))


class TestFilterExpression():
    def test_nextWord(self):
        interp = Interpreter("/id/gt/5/and/id/lte/101", UnidadeFederativa)
        assert interp.nextWord() == "id"
        assert interp.nextWord() == "gt"
        assert interp.nextWord() == "5"
        assert interp.nextWord() == "and"
        assert interp.nextWord() == "id"
        assert interp.nextWord() == "lte"
        assert interp.nextWord() == "101"
        assert interp.nextWord() is None
        interp = Interpreter("/sigla/in/'rj','es','go'/and/geom/within/Point(1,2)", UnidadeFederativa)
        assert interp.nextWord() == "sigla"
        assert interp.nextWord() == "in"
        assert interp.nextWord() == "'rj','es','go'"
        assert interp.nextWord() == "and"
        assert interp.nextWord() == "geom"
        assert interp.nextWord() == "within"
        assert interp.nextWord() == "Point(1,2)"
        assert interp.nextWord() is None

    @pytest.mark.asyncio
    async def test_translate(self):
       interp = Interpreter("/id/gt/5/and/id/lte/101", UnidadeFederativa)
       assert await interp.translate() == "id_objeto>5 and id_objeto<=101"
       interp = Interpreter("/id/gt/5/and/id/lte/101/or/(/id/eq/200/and/sigla/eq/RJ/)", UnidadeFederativa)
       assert await interp.translate() == "id_objeto>5 and id_objeto<=101 or  ( id_objeto=200 and sigla='RJ' ) "
       interp = Interpreter("/(/id/gt/5/and/id/lte/101/)/or/(/id/eq/200/and/sigla/eq/RJ/)", UnidadeFederativa)
       assert await interp.translate() == " ( id_objeto>5 and id_objeto<=101 )  or  ( id_objeto=200 and sigla='RJ' ) "
       interp = Interpreter("/sigla/in/RJ,SP,MG,ES/", UnidadeFederativa)
       assert await interp.translate() == "sigla in ('RJ','SP','MG','ES')"
       interp = Interpreter("/(/id/gt/5/and/id/lte/101/)/or/(/id/eq/200/and/sigla/eq/RJ/)/and/sigla/in/RJ,SP,MG,ES/", UnidadeFederativa)
       assert await interp.translate() == " ( id_objeto>5 and id_objeto<=101 )  or  ( id_objeto=200 and sigla='RJ' )  and sigla in ('RJ','SP','MG','ES')"
       interp = Interpreter(f"sigla/eq/(/http://{SERVIDOR}:{PORTA}/unidade-federacao-a-list/RJ/sigla/)/or/(/geocodigo/eq/31/)/", UnidadeFederacaoA)
       assert await interp.translate() == "sigla='RJ' or  ( geocodigo='31' ) "
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
