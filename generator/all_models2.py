# coding: utf-8
from sqlalchemy import Boolean, CHAR, Column, Date, Float, ForeignKey, Integer, String, text
from sqlalchemy.orm import relationship
from sqlalchemy.ext.declarative import declarative_base

Base = declarative_base()
metadata = Base.metadata


class Grupo(Base):
    __tablename__ = 'grupo'
    __table_args__ = {'schema': 'pessoal'}

    id_grupo = Column(Integer, primary_key=True, server_default=text("nextval('pessoal.s_grupo'::regclass)"))
    nome = Column(String, nullable=False)
    descricao = Column(String)


class LocalResidencia(Base):
    __tablename__ = 'local_residencia'
    __table_args__ = {'schema': 'pessoal'}

    id_local_residencia = Column(Integer, primary_key=True)
    nome_estado = Column(String)
    nome_municipio = Column(String)


class TipoGasto(Base):
    __tablename__ = 'tipo_gasto'
    __table_args__ = {'schema': 'pessoal'}

    id_tipo_gasto = Column(Integer, primary_key=True, server_default=text("nextval('pessoal.s_tipo_gasto'::regclass)"))
    descricao = Column(String, nullable=False, unique=True)
    id_tipo_gasto_pai = Column(ForeignKey('pessoal.tipo_gasto.id_tipo_gasto'))

    tipo_gasto_pai = relationship('TipoGasto', remote_side=[id_tipo_gasto])


class Pessoa(Base):
    __tablename__ = 'pessoa'
    __table_args__ = {'schema': 'pessoal'}

    nome = Column(String(100), nullable=False, unique=True)
    data_nascimento = Column(Date)
    id_pessoa = Column(Integer, primary_key=True, server_default=text("nextval('pessoal.s_pessoa'::regclass)"))
    cpf = Column(CHAR(11))
    is_usuario = Column(Boolean, server_default=text("false"))
    senha = Column(String)
    email = Column(String, unique=True)
    id_local_residencia = Column(ForeignKey('pessoal.local_residencia.id_local_residencia'))

    local_residencia = relationship('LocalResidencia')


class Gasto(Base):
    __tablename__ = 'gasto'
    __table_args__ = {'schema': 'pessoal'}

    id_gasto = Column(Integer, primary_key=True, server_default=text("nextval('pessoal.s_gasto'::regclass)"))
    valor = Column(Float, nullable=False)
    data = Column(Date, nullable=False)
    id_pessoa = Column(ForeignKey('pessoal.pessoa.id_pessoa'))
    id_tipo_gasto = Column(ForeignKey('pessoal.tipo_gasto.id_tipo_gasto'), nullable=False, index=True)

    pessoa = relationship('Pessoa')
    tipo_gasto = relationship('TipoGasto')


class PessoaGrupo(Base):
    __tablename__ = 'pessoa_grupo'
    __table_args__ = {'schema': 'pessoal'}

    id_pessoa_grupo = Column(Integer, primary_key=True, server_default=text("nextval('pessoal.s_pessoa_grupo'::regclass)"))
    id_grupo = Column(ForeignKey('pessoal.grupo.id_grupo'), nullable=False, index=True)
    id_pessoa = Column(ForeignKey('pessoal.pessoa.id_pessoa'), nullable=False)
    data_entrada = Column(Date)

    grupo = relationship('Grupo')
    pessoa = relationship('Pessoa')
