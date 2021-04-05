from geoalchemy2 import Geometry
from sqlalchemy import CHAR, Column, Float, Integer, Numeric, SmallInteger, String, Text, Date
from sqlalchemy.orm import relationship
from sqlalchemy.sql.sqltypes import NullType
from sqlalchemy.ext.declarative import declarative_base
from src.orm.models import AlchemyBase, Base
from src.orm.geo_models import AlchemyGeoBase
import unittest
import pytest
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
   id_ator = Column('id_ator',Integer(),nullable=False)
   email2 = Column('email2',String(length=50),nullable=True)
   jacare_gestor = Column('gestor',String(length=20),nullable=True)
   capacitado = Column('capacitado',String(length=20),nullable=True)
   id_capacitacao = Column('id_capacitacao',Integer(),nullable=True)
   #ator = relationship('Ator')
   #capacitacao = relationship('Capacitacao')
   def nome_abreviado(self)->str:
      return self.nome[:-1]

class UnidadeFederacao(AlchemyGeoBase, Base):
   __tablename__ = 'lim_unidade_federacao_a'
   __table_args__ = {'schema': 'bcim'}

   id_objeto = Column('id_objeto',Integer(),primary_key=True,nullable=False)
   nome = Column('nome',String(length=100),nullable=True)
   nomeabrev = Column('nomeabrev',String(length=50),nullable=True)
   geometriaaproximada = Column('geometriaaproximada',String(length=3),nullable=True)
   sigla = Column('sigla',String(length=3),nullable=True)
   geocodigo = Column('geocodigo',String(length=15),nullable=True)
   geom = Column('geom',Geometry(geometry_type='MULTIPOLYGON', srid=4674, from_text='ST_GeomFromEWKT', name='geometry'),nullable=True)
   id_produtor = Column('id_produtor',Integer(),nullable=True)
   id_elementoprodutor = Column('id_elementoprodutor',Integer(),nullable=True)
   cd_insumo_orgao = Column('cd_insumo_orgao',Integer(),nullable=True)
   nr_insumo_mes = Column('nr_insumo_mes',SmallInteger(),nullable=True)
   nr_insumo_ano = Column('nr_insumo_ano',SmallInteger(),nullable=True)
   tx_insumo_documento = Column('tx_insumo_documento',String(length=60),nullable=True)

   @classmethod
   def geo_column_name(cls) -> str:
       return 'geom'

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
       p2 = 'nome,ator'
       assert rep.is_projection_from_path(p2) == True
       p3 = 'nome,ator,atributoinexistente'
       assert rep.is_projection_from_path(p3) == False
       p4 = 'nome/upper'
       assert rep.is_projection_from_path(p4) == False
    def test_is_operation_from_path(self):
       p1 = 'nome'
       rep = Representante()
       assert rep.is_operation_from_path(p1) == False
       p1 = 'nome,ator'
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
