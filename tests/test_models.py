from typing import List
from unittest import TestCase
from sqlalchemy import CHAR, Column, Float, Integer, Numeric, SmallInteger, String, Text, Date, ForeignKey
from sqlalchemy.orm import relationship
from sqlalchemy.sql.sqltypes import NullType
from sqlalchemy.ext.declarative import declarative_base
from src.orm.models import AlchemyBase, Base


class Pessoa(AlchemyBase, Base):
   __tablename__ = 'pessoa'
   __table_args__ = {'schema': 'pessoal'}
   nome = Column('nome',String(length=100),nullable=False)
   data_nascimento = Column('data_nascimento',Date(),nullable=True)
   id_pessoa = Column('id_pessoa',Integer(),primary_key=True,nullable=False)
   cpf = Column('cpf',CHAR(length=11),nullable=True)
   gastos = relationship("Gasto")
   id_local_residencia = Column('id_local_residencia', ForeignKey('pessoal.local_residencia.id_local_residencia'), nullable=False)
   local_residencia = relationship("LocalResidencia",uselist=False , foreign_keys=[id_local_residencia])
   #local_residencia = relationship("LocalResidencia", id_local_residencia)

class Gasto(AlchemyBase, Base):
   __tablename__ = 'gasto'
   __table_args__ = {'schema': 'pessoal'}
   id_gasto = Column('id_gasto',Integer(),primary_key=True,nullable=False)
   valor = Column('valor',Float(),nullable=False)
   data = Column('data',Date(),nullable=False)
   pessoa = Column('id_pessoa', ForeignKey('pessoal.pessoa.id_pessoa'), nullable=True)
   id_tipo_gasto = Column('id_tipo_gasto', ForeignKey('pessoal.tipo_gasto.id_tipo_gasto'), nullable=False)
   tipo_gasto = relationship("TipoGasto", uselist=False, foreign_keys=[id_tipo_gasto])

class TipoGasto(AlchemyBase, Base):
   __tablename__ = 'tipo_gasto'
   __table_args__ = {'schema': 'pessoal'}

   id_tipo_gasto = Column('id_tipo_gasto',Integer(),primary_key=True,nullable=False)
   descricao = Column('descricao',String(),nullable=False)
   id_tipo_gasto_pai = Column(ForeignKey('pessoal.tipo_gasto.id_tipo_gasto'), nullable=True)
   tipo_gasto_pai = relationship("TipoGasto", uselist=False, foreign_keys=[id_tipo_gasto_pai])

class LocalResidencia(AlchemyBase, Base):
    __tablename__ = 'local_residencia'
    __table_args__ = {'schema': 'pessoal'}
    id_local_residencia = Column('id_local_residencia', Integer(), primary_key=True, nullable=False)
    nome_estado = Column('nome_estado', String(), nullable=False)
    nome_municipio = Column('nome_municipio', String(), nullable=False)


#pessoa-list/nome,local_residencia,gastos.valor,gastos.data,gastos.tipo_gasto.descricao
class TestModels(TestCase):

    def test_all_attribute_names(self):
        pass

    def test_all_attributes_with_dereferenceable(self):
        s1 = set(Pessoa.all_attributes_with_dereferenceable())
        s2 = {'nome', 'data_nascimento', 'cpf', 'gastos', 'gastos.valor','gastos.data', 'gastos.tipo_gasto','gastos.tipo_gasto.id_tipo_gasto', 'gastos.tipo_gasto.descricao', 'gastos.tipo_gasto.id_tipo_gasto_pai', 'local_residencia', 'local_residencia.id_local_residencia', 'local_residencia.nome_estado', 'local_residencia.nome_municipio'}

        self.assertEqual(s2.difference(s1), {})
    """
    def test_attributes_from_path_not_exist(self):
        path = 'nome,cpf,gastos'
        self.assertEqual(0, len(Pessoa.attributes_from_path_not_exist(path)), f"All attributes {path} from path in Pessoa")
        path = 'nome,cpf,gastos.valor,gastos.data'
        self.assertEqual(0, len(Pessoa.attributes_from_path_not_exist(path)),
                         f"All attributes {path} from path in Pessoa")
        path = 'nome,cpf,gastos.valor,gastos.data,gastos.tipo_gasto'
        self.assertEqual(0, len(Pessoa.attributes_from_path_not_exist(path)),
                         f"All attributes {path} from path in Pessoa")
        path = 'nome,cpf,gastos.valor,gastos.data,gastos.tipo_gasto.descricao'
        self.assertEqual(0, len(Pessoa.attributes_from_path_not_exist(path)),
                         f"All attributes {path} from path in Pessoa")
        path = 'nome,cpf,gastos.valor,gastos.data,gastos.tipo_gasto.sem_valor'
        self.assertEqual('gastos.tipo_gasto.sem_valor', Pessoa.attributes_from_path_not_exist(path)[0],
                         f"The attributes {Pessoa.attributes_from_path_not_exist(path)[0]} not exists")
    """