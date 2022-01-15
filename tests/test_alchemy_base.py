from geoalchemy2 import Geometry
from sqlalchemy import CHAR, Column, Float, Integer, Numeric, SmallInteger, String, Text, Date
from sqlalchemy.orm import relationship
from sqlalchemy.sql.sqltypes import NullType
from sqlalchemy.ext.declarative import declarative_base
from src.orm.models import AlchemyBase, Base
from src.orm.geo_models import AlchemyGeoBase
import unittest
import pytest
#URLDB=sqlite:///hyper-db.sqlite
class Ator(AlchemyBase, Base):
   __tablename__ = 'ator'
   __table_args__ = {'schema': 'adm'}
   nome = Column('nome',String(length=500),nullable=False)
   status_adesao = Column('status_adesao',String(length=30),nullable=False)
   documento_solicitacao = Column('documento_solicitacao',Text(),nullable=True)
   capacitacao = Column('capacitacao',String(length=20),nullable=True)
   modalidade = Column('modalidade',String(length=20),nullable=True)
   observacao = Column('observacao',Text(),nullable=True)
   id_ator = Column('id_ator',Integer(),primary_key=True,nullable=False)
   no_implementado = Column('no_implementado',String(length=20),nullable=True)
   data_oficio = Column('data_oficio',Date(),nullable=True)
   esfera = Column('esfera',String(length=20),nullable=True)
   nome_instituicao_origem = Column('nome_instituicao_origem',String(length=100),nullable=True)
   data_adesao = Column('data_adesao',Date(),nullable=True)
   data_interesse = Column('data_interesse',Date(),nullable=True)
   sigla = Column('sigla',String(length=10),nullable=True)

class Representante(AlchemyBase, Base):
   __tablename__ = 'representante'
   __table_args__ = {'schema': 'adm'}

   id_representante = Column('id_representante',Integer(),primary_key=True,nullable=False)
   nome = Column('nome',String(length=150),nullable=False)
   email1 = Column('email1',String(length=70),nullable=True)
   funcao_cargo = Column('funcao_cargo',String(length=100),nullable=True)
   area_setor = Column('area_setor',String(length=150),nullable=True)
   telefone1 = Column('telefone1',String(length=25),nullable=True)
   telefone2 = Column('telefone2',String(length=25),nullable=True)
   celular_telefone3 = Column('celular_telefone3',String(length=25),nullable=True)
   email2 = Column('email2',String(length=50),nullable=True)
   jacare_gestor = Column('gestor',String(length=20),nullable=True)
   capacitado = Column('capacitado',String(length=20),nullable=True)
   #id_ator = Column('id_ator', Integer(), nullable=False)
   #ator = relationship('Ator',foreign_keys=[id_ator])
   #id_capacitacao = Column('id_capacitacao', Integer(), nullable=True)
   #capacitacao = relationship('Capacitacao',foreign_keys=[id_capacitacao])
   def nome_abreviado(self)->str:
      return self.nome[:-1]


class Hidreletrica(Base):
    __tablename__ = 'hidreletrica'
    __table_args__ = {'schema': ''}

    id_objeto = Column(Integer, primary_key=True)
    nome = Column(String(100))
    geometriaaproximada = Column(String(3))
    potenciaoutorgada = Column(Integer)
    potenciafiscalizada = Column(Integer)
    codigohidreletrica = Column(String(30))
    operacional = Column(String(12))
    situacaofisica = Column(Text)
    geom = Column(Geometry('POINT', 4674, from_text='ST_GeomFromEWKT', name='geometry'), index=True)

class TerraIndigena(Base):
    __tablename__ = 'terra_indigena'

    id_objeto = Column(Integer, primary_key=True)
    nome = Column(String(100))
    nomeabrev = Column(String(50))
    geometriaaproximada = Column(String(3))
    perimetrooficial = Column(Float(53))
    areaoficialha = Column(Float(53))
    grupoetnico = Column(String(100))
    datasituacaojuridica = Column(String(20))
    situacaojuridica = Column(String(23))
    nometi = Column(String(100))
    geom = Column(Geometry('MULTIPOLYGON', 4674, from_text='ST_GeomFromEWKT', name='geometry'), index=True)
    codigofunai = Column(Integer)

class UnidadeFederacao(Base):
    __tablename__ = 'unidade_federacao'
    __table_args__ = {'schema': ''}

    id_objeto = Column(Integer, primary_key=True)
    nome = Column(String(100))
    nomeabrev = Column(String(50))
    geometriaaproximada = Column(String(3))
    sigla = Column(String(3))
    geocodigo = Column(String(15))
    geom = Column(Geometry('MULTIPOLYGON', 4674, from_text='ST_GeomFromEWKT', name='geometry'), index=True)

class Ferrovia(Base):
    __tablename__ = 'ferroviaria'
    __table_args__ = {'schema': ''}

    id_objeto = Column(Integer, primary_key=True)
    nome = Column(String(100))
    nomeabrev = Column(String(50))
    geometriaaproximada = Column(String(3))
    codtrechoferrov = Column(String(25))
    posicaorelativa = Column(String(15))
    tipotrechoferrov = Column(String(12))
    bitola = Column(String(27))
    eletrificada = Column(String(12))
    nrlinhas = Column(String(12))
    emarruamento = Column(String(12))
    jurisdicao = Column(Text)
    administracao = Column(Text)
    concessionaria = Column(String(100))
    operacional = Column(String(12))
    cargasuportmaxima = Column(Float(53))
    situacaofisica = Column(Text)
    geom = Column(Geometry('LINESTRING', 4674, from_text='ST_GeomFromEWKT', name='geometry'), index=True)

class TestAlchemyBase(unittest.TestCase):
    def test_column_names_with_alias_as_enum(self):
        assert Representante.column_names_with_alias_as_enum().find("id_representante as id_representante") == -1


    def test_is_projection_from_path(self):
       """
       Valids path for a NonSpatialResource or FeatureResource expects:
         where state/1/ is the model.\n
         only attributes: state/1/name or state/1/name,geom \n
         only functions: state/1/transform/3005/area \n
         attribute and functions: state/1/geom/transform/3005/area \n
       Anything different is invalid path
       """
       p1 = 'nome'
       rep = Representante()
       assert rep.is_projection_from_path(p1) == True
       p2 = 'nome,area_setor'
       assert rep.is_projection_from_path(p2) == True
       p3 = 'nome,area_setor,atributoinexistente'
       assert rep.is_projection_from_path(p3) == False
       p4 = 'nome/upper'
       assert rep.is_projection_from_path(p4) == False

    def test_is_operation_from_path(self):
       p1 = 'nome'
       rep = Representante()
       assert rep.is_operation_from_path(p1) == False
       p1 = 'nome,area_setor'
       assert rep.is_operation_from_path(p1) == False
       p1 = 'nome,ator,atributoinexistente'
       assert rep.is_operation_from_path(p1) == False
       p1 = 'nome/upper'
       assert rep.is_operation_from_path(p1) == True
       p1 = 'nome/upper/lower'
       assert rep.is_operation_from_path(p1) == True
       p1 = 'nome_abreviado'
       assert rep.is_operation_from_path(p1) == True
       p1 = 'nome_abreviado_sem_acento'
       assert rep.is_operation_from_path(p1) == False

    def test_validate_path(self):
       path = 'projection/nome,sigla'
       assert type(UnidadeFederacao.validate_path(path), str)

    def test_path_as_list(self):
       path ='nome/data'
       assert  UnidadeFederacao.path_as_list(path) == ['nome', 'data']
       path = 'nome/data/'
       assert UnidadeFederacao.path_as_list(path) == ['nome', 'data']
       path = 'geom/contains'
       assert UnidadeFederacao.path_as_list(path) == ['geom', 'contains']
       path = 'geom/contains/(/http://unidade-federacao/rj/geom/)/'
       self.assertEquals(UnidadeFederacao.path_as_list(path),['geom', 'contains', 'http://unidade-federacao/rj/geom'])
