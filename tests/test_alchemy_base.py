from sqlalchemy import CHAR, Column, Float, Integer, Numeric, SmallInteger, String, Text, Date
from sqlalchemy.orm import relationship
from sqlalchemy.sql.sqltypes import NullType
from sqlalchemy.ext.declarative import declarative_base
from src.orm.models import AlchemyBase, Base

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
   ator = relationship('Ator')
   capacitacao = relationship('Capacitacao')

class TestAlchemyBase():
    def test_column_names_with_alias_as_enum(self):
        assert Representante.column_names_with_alias_as_enum().find("id_representante as id_representante") == -1