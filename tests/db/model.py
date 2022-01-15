from geoalchemy2 import Geometry
from sqlalchemy import CHAR, Column, Float, Integer, Numeric, SmallInteger, String, Text, Date
from src.orm.models import AlchemyBase, Base
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
