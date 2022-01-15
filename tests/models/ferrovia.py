# -*- coding: latin-1 -*-
from geoalchemy2 import Geometry
from sqlalchemy import CHAR, Column, Float, Boolean, Integer, Numeric, SmallInteger, String, Text, Date, DateTime, ForeignKey
from sqlalchemy.orm import relationship
from sqlalchemy.sql.sqltypes import NullType
from sqlalchemy.ext.declarative import declarative_base
from src.orm.models import Base
from src.orm.geo_models import AlchemyGeoBase


class Ferrovia(AlchemyGeoBase, Base): 
   __tablename__ = 'ferroviaria'
   __table_args__ = {'schema': ''}

   id_objeto = Column('id_objeto',Integer(),primary_key=True,nullable=False)
   nome = Column('nome',String(length=100),nullable=True)
   nomeabrev = Column('nomeabrev',String(length=50),nullable=True)
   geometriaaproximada = Column('geometriaaproximada',String(length=3),nullable=True)
   codtrechoferrov = Column('codtrechoferrov',String(length=25),nullable=True)
   posicaorelativa = Column('posicaorelativa',String(length=15),nullable=True)
   tipotrechoferrov = Column('tipotrechoferrov',String(length=12),nullable=True)
   bitola = Column('bitola',String(length=27),nullable=True)
   eletrificada = Column('eletrificada',String(length=12),nullable=True)
   nrlinhas = Column('nrlinhas',String(length=12),nullable=True)
   emarruamento = Column('emarruamento',String(length=12),nullable=True)
   jurisdicao = Column('jurisdicao',Text(),nullable=True)
   administracao = Column('administracao',Text(),nullable=True)
   concessionaria = Column('concessionaria',String(length=100),nullable=True)
   operacional = Column('operacional',String(length=12),nullable=True)
   cargasuportmaxima = Column('cargasuportmaxima',Float(precision=53),nullable=True)
   situacaofisica = Column('situacaofisica',Text(),nullable=True)
   geom = Column('geom',Geometry(geometry_type='LINESTRING', srid=4674, from_text='ST_GeomFromEWKT', name='geometry'),nullable=True)

   @classmethod
   def geo_column_name(cls) -> str:
       return 'geom'