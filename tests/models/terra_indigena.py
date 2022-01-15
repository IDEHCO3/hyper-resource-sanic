# -*- coding: latin-1 -*-
from geoalchemy2 import Geometry
from sqlalchemy import CHAR, Column, Float, Boolean, Integer, Numeric, SmallInteger, String, Text, Date, DateTime, ForeignKey
from sqlalchemy.orm import relationship
from sqlalchemy.sql.sqltypes import NullType
from sqlalchemy.ext.declarative import declarative_base
from src.orm.models import Base
from src.orm.geo_models import AlchemyGeoBase


class TerraIndigena(AlchemyGeoBase, Base): 
   __tablename__ = 'terra_indigena'
   __table_args__ = {'schema': ''}

   id_objeto = Column('id_objeto',Integer(),primary_key=True,nullable=False)
   nome = Column('nome',String(length=100),nullable=True)
   nomeabrev = Column('nomeabrev',String(length=50),nullable=True)
   geometriaaproximada = Column('geometriaaproximada',String(length=3),nullable=True)
   perimetrooficial = Column('perimetrooficial',Float(precision=53),nullable=True)
   areaoficialha = Column('areaoficialha',Float(precision=53),nullable=True)
   grupoetnico = Column('grupoetnico',String(length=100),nullable=True)
   datasituacaojuridica = Column('datasituacaojuridica',String(length=20),nullable=True)
   situacaojuridica = Column('situacaojuridica',String(length=23),nullable=True)
   nometi = Column('nometi',String(length=100),nullable=True)
   geom = Column('geom',Geometry(geometry_type='MULTIPOLYGON', srid=4674, from_text='ST_GeomFromEWKT', name='geometry'),nullable=True)
   codigofunai = Column('codigofunai',Integer(),nullable=True)

   @classmethod
   def geo_column_name(cls) -> str:
       return 'geom'