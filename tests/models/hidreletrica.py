# -*- coding: latin-1 -*-
from geoalchemy2 import Geometry
from sqlalchemy import CHAR, Column, Float, Boolean, Integer, Numeric, SmallInteger, String, Text, Date, DateTime, ForeignKey
from sqlalchemy.orm import relationship
from sqlalchemy.sql.sqltypes import NullType
from sqlalchemy.ext.declarative import declarative_base
from src.orm.models import Base
from src.orm.geo_models import AlchemyGeoBase


class Hidreletrica(AlchemyGeoBase, Base): 
   __tablename__ = 'hidreletrica'
   __table_args__ = {'schema': ''}

   id_objeto = Column('id_objeto',Integer(),primary_key=True,nullable=False)
   nome = Column('nome',String(length=100),nullable=True)
   geometriaaproximada = Column('geometriaaproximada',String(length=3),nullable=True)
   potenciaoutorgada = Column('potenciaoutorgada',Integer(),nullable=True)
   potenciafiscalizada = Column('potenciafiscalizada',Integer(),nullable=True)
   codigohidreletrica = Column('codigohidreletrica',String(length=30),nullable=True)
   operacional = Column('operacional',String(length=12),nullable=True)
   situacaofisica = Column('situacaofisica',Text(),nullable=True)
   geom = Column('geom',Geometry(geometry_type='POINT', srid=4674, from_text='ST_GeomFromEWKT', name='geometry'),nullable=True)

   @classmethod
   def geo_column_name(cls) -> str:
       return 'geom'