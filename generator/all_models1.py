# coding: utf-8
from sqlalchemy import Boolean, Column, Date, ForeignKey, Integer, String, Text, text
from sqlalchemy.orm import relationship
from sqlalchemy.ext.declarative import declarative_base

Base = declarative_base()
metadata = Base.metadata


class Ator(Base):
    __tablename__ = 'ator'
    __table_args__ = {'schema': 'adm', 'comment': 'Produtor ou provedor de dados geoespaciais do governo federal, estadual, distrital ou municipal, que estará representando um nó (ou com interesse) do Diretorio Brasileiro de Dados Geoespaciais (DBDG), da Infraestrutura Nacional  de Dados Espaciais (INDE), a partir dos quais poderão disponibilizar seus dados, metadados e geoserviços via Portal SIG Brasil.'}

    nome = Column(String(500), nullable=False)
    status_adesao = Column(String(30), nullable=False)
    documento_solicitacao = Column(Text)
    capacitacao = Column(String(20))
    modalidade = Column(String(20))
    observacao = Column(Text)
    id_ator = Column(Integer, primary_key=True, server_default=text("nextval('adm.s_ator'::regclass)"))
    no_implementado = Column(String(20))
    data_oficio = Column(Date)
    esfera = Column(String(20))
    nome_instituicao_origem = Column(String(100))
    data_adesao = Column(Date)
    data_interesse = Column(Date)
    sigla = Column(String(10))


class Capacitacao(Base):
    __tablename__ = 'capacitacao'
    __table_args__ = {'schema': 'adm'}

    id_capacitacao = Column(Integer, primary_key=True)
    nome = Column(String(50), nullable=False)
    descricao = Column(String(300))
    data_inicio = Column(Date, nullable=False)
    data_fim = Column(Date, nullable=False)
    data = Column(Date, comment='Data da capacitacao - nao eh mais necessario, pois existe a coluna data_inicio e data_fim')


class Usuario(Base):
    __tablename__ = 'usuario'
    __table_args__ = {'schema': 'adm'}

    id_usuario = Column(Integer, primary_key=True, server_default=text("nextval('adm.s_usuario'::regclass)"))
    nome = Column(String(100))
    email = Column(String(50), nullable=False, unique=True)
    senha = Column(String(50), nullable=False)
    is_administrador = Column(Boolean, server_default=text("false"))


class Documentacao(Base):
    __tablename__ = 'documentacao'
    __table_args__ = {'schema': 'adm'}

    id_documentacao = Column(Integer, primary_key=True, server_default=text("nextval('adm.s_documentacao'::regclass)"))
    arquivo = Column(String(255), nullable=False, unique=True)
    data = Column(Date)
    ator = Column(ForeignKey('adm.ator.id_ator'), nullable=False)

    ator1 = relationship('Ator')


class HistoricoContatoAtor(Base):
    __tablename__ = 'historico_contato_ator'
    __table_args__ = {'schema': 'adm'}

    id_historico_contato_ator = Column(Integer, primary_key=True)
    data = Column(Date)
    nome_contato = Column(String)
    email_contato = Column(String)
    descricao = Column(Text)
    id_ator = Column(ForeignKey('adm.ator.id_ator'))

    ator = relationship('Ator')


class PublicacaoInformacaoGeoespacial(Base):
    __tablename__ = 'publicacao_informacao_geoespacial'
    __table_args__ = {'schema': 'adm'}

    tem_metadados = Column(String(20))
    tem_geoservicos = Column(String(20))
    tem_download = Column(String(20))
    tem_vinde = Column(String(20))
    id_publicacao_informacao_geoespacial = Column(Integer, primary_key=True, server_default=text("nextval('adm.s_publicacao_informacao_geoespacial'::regclass)"))
    id_ator = Column(ForeignKey('adm.ator.id_ator'), nullable=False)

    ator = relationship('Ator')


class Representante(Base):
    __tablename__ = 'representante'
    __table_args__ = {'schema': 'adm'}

    id_representante = Column(Integer, primary_key=True, server_default=text("nextval('adm.s_representante'::regclass)"))
    nome = Column(String(150), nullable=False)
    email1 = Column(String(70))
    funcao_cargo = Column(String(100))
    area_setor = Column(String(150))
    telefone1 = Column(String(25))
    telefone2 = Column(String(25))
    celular_telefone3 = Column(String(25))
    id_ator = Column(ForeignKey('adm.ator.id_ator'), nullable=False)
    email2 = Column(String(50))
    gestor = Column(String(20))
    capacitado = Column(String(20))
    id_capacitacao = Column(ForeignKey('adm.capacitacao.id_capacitacao'), index=True)

    ator = relationship('Ator')
    capacitacao = relationship('Capacitacao')
