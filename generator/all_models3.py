# coding: utf-8
from sqlalchemy import CHAR, Column, Float, Integer, Numeric, SmallInteger, String, Text
from geoalchemy2.types import Geometry
from sqlalchemy.ext.declarative import declarative_base

Base = declarative_base()
metadata = Base.metadata


class AdmEdifPubMilitarA(Base):
    __tablename__ = 'adm_edif_pub_militar_a'
    __table_args__ = {'schema': 'bcim'}

    id_objeto = Column(Integer, primary_key=True)
    nome = Column(String(100))
    nomeabrev = Column(String(50))
    geometriaaproximada = Column(String(3))
    tipoedifmil = Column(String(26))
    tipousoedif = Column(String(21))
    situacaofisica = Column(Text)
    operacional = Column(String(12))
    matconstr = Column(String(18))
    geom = Column(Geometry('POLYGON', 4674, from_text='ST_GeomFromEWKT', name='geometry'), index=True)
    id_produtor = Column(Integer)
    id_elementoprodutor = Column(Integer)
    cd_insumo_orgao = Column(Integer)
    nr_insumo_mes = Column(SmallInteger)
    nr_insumo_ano = Column(SmallInteger)
    tx_insumo_documento = Column(String(60))


class AdmEdifPubMilitarP(Base):
    __tablename__ = 'adm_edif_pub_militar_p'
    __table_args__ = {'schema': 'bcim'}

    id_objeto = Column(Integer, primary_key=True)
    nome = Column(String(100))
    nomeabrev = Column(String(50))
    geometriaaproximada = Column(String(3))
    tipoedifmil = Column(String(26))
    tipousoedif = Column(String(21))
    situacaofisica = Column(Text)
    operacional = Column(String(12))
    matconstr = Column(String(18))
    geom = Column(Geometry('POINT', 4674, from_text='ST_GeomFromEWKT', name='geometry'), index=True)
    id_produtor = Column(Integer)
    id_elementoprodutor = Column(Integer)
    cd_insumo_orgao = Column(Integer)
    nr_insumo_mes = Column(SmallInteger)
    nr_insumo_ano = Column(SmallInteger)
    tx_insumo_documento = Column(String(60))


class AdmPostoFiscalP(Base):
    __tablename__ = 'adm_posto_fiscal_p'
    __table_args__ = {'schema': 'bcim'}

    id_objeto = Column(Integer, primary_key=True)
    nome = Column(String(100))
    nomeabrev = Column(String(50))
    geometriaaproximada = Column(String(3))
    operacional = Column(String(12))
    situacaofisica = Column(Text)
    tipopostofisc = Column(String(22))
    geom = Column(Geometry('POINT', 4674, from_text='ST_GeomFromEWKT', name='geometry'), index=True)
    id_produtor = Column(Integer)
    id_elementoprodutor = Column(Integer)
    cd_insumo_orgao = Column(Integer)
    nr_insumo_mes = Column(SmallInteger)
    nr_insumo_ano = Column(SmallInteger)
    tx_insumo_documento = Column(String(60))


class EcoEdifAgropecExtVegetalPescaP(Base):
    __tablename__ = 'eco_edif_agropec_ext_vegetal_pesca_p'
    __table_args__ = {'schema': 'bcim'}

    id_objeto = Column(Integer, primary_key=True)
    nome = Column(String(100))
    nomeabrev = Column(String(50))
    geometriaaproximada = Column(String(3))
    operacional = Column(String(12))
    situacaofisica = Column(Text)
    tipoedifagropec = Column(String(50))
    matconstr = Column(String(18))
    geom = Column(Geometry('POINT', 4674, from_text='ST_GeomFromEWKT', name='geometry'), index=True)
    id_produtor = Column(Integer)
    id_elementoprodutor = Column(Integer)
    cd_insumo_orgao = Column(Integer)
    nr_insumo_mes = Column(SmallInteger)
    nr_insumo_ano = Column(SmallInteger)
    tx_insumo_documento = Column(String(60))


class EcoExtMineralA(Base):
    __tablename__ = 'eco_ext_mineral_a'
    __table_args__ = {'schema': 'bcim'}

    id_objeto = Column(Integer, primary_key=True)
    nome = Column(String(100))
    nomeabrev = Column(String(50))
    geometriaaproximada = Column(String(3))
    tiposecaocnae = Column(String(50))
    operacional = Column(String(12))
    situacaofisica = Column(Text)
    tipoextmin = Column(String(20))
    tipoprodutoresiduo = Column(String(40))
    tipopocomina = Column(String(15))
    procextracao = Column(String(12))
    formaextracao = Column(String(12))
    atividade = Column(String(12))
    geom = Column(Geometry('POLYGON', 4674, from_text='ST_GeomFromEWKT', name='geometry'), index=True)
    id_produtor = Column(Integer)
    id_elementoprodutor = Column(Integer)
    cd_insumo_orgao = Column(Integer)
    nr_insumo_mes = Column(SmallInteger)
    nr_insumo_ano = Column(SmallInteger)
    tx_insumo_documento = Column(String(60))


class EcoExtMineralP(Base):
    __tablename__ = 'eco_ext_mineral_p'
    __table_args__ = {'schema': 'bcim'}

    id_objeto = Column(Integer, primary_key=True)
    nome = Column(String(100))
    nomeabrev = Column(String(50))
    geometriaaproximada = Column(String(3))
    tiposecaocnae = Column(String(50))
    operacional = Column(String(12))
    situacaofisica = Column(Text)
    tipoextmin = Column(String(20))
    tipoprodutoresiduo = Column(String(40))
    tipopocomina = Column(String(15))
    procextracao = Column(String(12))
    formaextracao = Column(String(12))
    atividade = Column(String(12))
    geom = Column(Geometry('POINT', 4674, from_text='ST_GeomFromEWKT', name='geometry'), index=True)
    id_produtor = Column(Integer)
    id_elementoprodutor = Column(Integer)
    cd_insumo_orgao = Column(Integer)
    nr_insumo_mes = Column(SmallInteger)
    nr_insumo_ano = Column(SmallInteger)
    tx_insumo_documento = Column(String(60))


class EncEstGeradEnergiaEletricaP(Base):
    __tablename__ = 'enc_est_gerad_energia_eletrica_p'
    __table_args__ = {'schema': 'bcim'}

    id_objeto = Column(Integer, primary_key=True)
    nome = Column(String(100))
    nomeabrev = Column(String(50))
    geometriaaproximada = Column(String(3))
    codigoestacao = Column(String(30))
    potenciaoutorgada = Column(Integer)
    potenciafiscalizada = Column(Integer)
    operacional = Column(String(12))
    situacaofisica = Column(Text)
    tipoestgerad = Column(String(15))
    destenergelet = Column(String(56))
    geom = Column(Geometry('POINT', 4674, from_text='ST_GeomFromEWKT', name='geometry'), index=True)
    id_produtor = Column(Integer)
    id_elementoprodutor = Column(Integer)
    cd_insumo_orgao = Column(Integer)
    nr_insumo_mes = Column(SmallInteger)
    nr_insumo_ano = Column(SmallInteger)
    tx_insumo_documento = Column(String(60))


class EncHidreletricaP(Base):
    __tablename__ = 'enc_hidreletrica_p'
    __table_args__ = {'schema': 'bcim'}

    id_objeto = Column(Integer, primary_key=True)
    nome = Column(String(100))
    nomeabrev = Column(String(50))
    geometriaaproximada = Column(String(3))
    potenciaoutorgada = Column(Integer)
    potenciafiscalizada = Column(Integer)
    codigohidreletrica = Column(String(30))
    operacional = Column(String(12))
    situacaofisica = Column(Text)
    geom = Column(Geometry('POINT', 4674, from_text='ST_GeomFromEWKT', name='geometry'), index=True)
    id_produtor = Column(Integer)
    id_elementoprodutor = Column(Integer)
    cd_insumo_orgao = Column(Integer)
    nr_insumo_mes = Column(SmallInteger)
    nr_insumo_ano = Column(SmallInteger)
    tx_insumo_documento = Column(String(60))


class EncTermeletricaP(Base):
    __tablename__ = 'enc_termeletrica_p'
    __table_args__ = {'schema': 'bcim'}

    id_objeto = Column(Integer, primary_key=True)
    nome = Column(String(100))
    nomeabrev = Column(String(50))
    geometriaaproximada = Column(String(3))
    potenciaoutorgada = Column(Integer)
    potenciafiscalizada = Column(Integer)
    combrenovavel = Column(String(3))
    tipomaqtermica = Column(String(33))
    geracao = Column(String(20))
    tipocombustivel = Column(String(17))
    operacional = Column(String(12))
    situacaofisica = Column(Text)
    geom = Column(Geometry('POINT', 4674, from_text='ST_GeomFromEWKT', name='geometry'), index=True)
    id_produtor = Column(Integer)
    id_elementoprodutor = Column(Integer)
    cd_insumo_orgao = Column(Integer)
    nr_insumo_mes = Column(SmallInteger)
    nr_insumo_ano = Column(SmallInteger)
    tx_insumo_documento = Column(String(60))


class HidBancoAreiaA(Base):
    __tablename__ = 'hid_banco_areia_a'
    __table_args__ = {'schema': 'bcim'}

    id_objeto = Column(Integer, primary_key=True)
    nome = Column(String(100))
    nomeabrev = Column(String(50))
    geometriaaproximada = Column(String(3))
    tipobanco = Column(String(14))
    situacaoemagua = Column(String(17))
    materialpredominante = Column(String(27))
    geom = Column(Geometry('POLYGON', 4674, from_text='ST_GeomFromEWKT', name='geometry'), index=True)
    id_produtor = Column(Integer)
    id_elementoprodutor = Column(Integer)
    cd_insumo_orgao = Column(Integer)
    nr_insumo_mes = Column(SmallInteger)
    nr_insumo_ano = Column(SmallInteger)
    tx_insumo_documento = Column(String(60))


class HidBarragemL(Base):
    __tablename__ = 'hid_barragem_l'
    __table_args__ = {'schema': 'bcim'}

    id_objeto = Column(Integer, primary_key=True)
    nome = Column(String(100))
    nomeabrev = Column(String(50))
    geometriaaproximada = Column(String(3))
    matconstr = Column(String(18))
    usoprincipal = Column(String(15))
    operacional = Column(String(12))
    situacaofisica = Column(Text)
    geom = Column(Geometry('LINESTRING', 4674, from_text='ST_GeomFromEWKT', name='geometry'), index=True)
    id_produtor = Column(Integer)
    id_elementoprodutor = Column(Integer)
    cd_insumo_orgao = Column(Integer)
    nr_insumo_mes = Column(SmallInteger)
    nr_insumo_ano = Column(SmallInteger)
    tx_insumo_documento = Column(String(60))


class HidBarragemP(Base):
    __tablename__ = 'hid_barragem_p'
    __table_args__ = {'schema': 'bcim'}

    id_objeto = Column(Integer, primary_key=True)
    nome = Column(String(100))
    nomeabrev = Column(String(50))
    geometriaaproximada = Column(String(3))
    matconstr = Column(String(18))
    usoprincipal = Column(String(15))
    operacional = Column(String(12))
    situacaofisica = Column(Text)
    geom = Column(Geometry('POINT', 4674, from_text='ST_GeomFromEWKT', name='geometry'), index=True)
    id_produtor = Column(Integer)
    id_elementoprodutor = Column(Integer)
    cd_insumo_orgao = Column(Integer)
    nr_insumo_mes = Column(SmallInteger)
    nr_insumo_ano = Column(SmallInteger)
    tx_insumo_documento = Column(String(60))


class HidCorredeiraL(Base):
    __tablename__ = 'hid_corredeira_l'
    __table_args__ = {'schema': 'bcim'}

    id_objeto = Column(Integer, primary_key=True)
    nome = Column(String(100))
    nomeabrev = Column(String(50))
    geometriaaproximada = Column(String(3))
    geom = Column(Geometry('LINESTRING', 4674, from_text='ST_GeomFromEWKT', name='geometry'), index=True)
    id_produtor = Column(Integer)
    id_elementoprodutor = Column(Integer)
    cd_insumo_orgao = Column(Integer)
    nr_insumo_mes = Column(SmallInteger)
    nr_insumo_ano = Column(SmallInteger)
    tx_insumo_documento = Column(String(60))


class HidCorredeiraP(Base):
    __tablename__ = 'hid_corredeira_p'
    __table_args__ = {'schema': 'bcim'}

    id_objeto = Column(Integer, primary_key=True)
    nome = Column(String(100))
    nomeabrev = Column(String(50))
    geometriaaproximada = Column(String(3))
    geom = Column(Geometry('POINT', 4674, from_text='ST_GeomFromEWKT', name='geometry'), index=True)
    id_produtor = Column(Integer)
    id_elementoprodutor = Column(Integer)
    cd_insumo_orgao = Column(Integer)
    nr_insumo_mes = Column(SmallInteger)
    nr_insumo_ano = Column(SmallInteger)
    tx_insumo_documento = Column(String(60))


class HidIlhaA(Base):
    __tablename__ = 'hid_ilha_a'
    __table_args__ = {'schema': 'bcim'}

    id_objeto = Column(Integer, primary_key=True)
    nome = Column(String(100))
    nomeabrev = Column(String(50))
    geometriaaproximada = Column(String(3))
    tipoilha = Column(String(8))
    geom = Column(Geometry('POLYGON', 4674, from_text='ST_GeomFromEWKT', name='geometry'), index=True)
    id_produtor = Column(Integer)
    id_elementoprodutor = Column(Integer)
    cd_insumo_orgao = Column(Integer)
    nr_insumo_mes = Column(SmallInteger)
    nr_insumo_ano = Column(SmallInteger)
    tx_insumo_documento = Column(String(60))


class HidMassaDaguaA(Base):
    __tablename__ = 'hid_massa_dagua_a'
    __table_args__ = {'schema': 'bcim'}

    id_objeto = Column(Integer, primary_key=True)
    nome = Column(String(100))
    nomeabrev = Column(String(50))
    geometriaaproximada = Column(String(3))
    tipomassadagua = Column(String(18))
    salinidade = Column(String(16))
    regime = Column(String(31))
    geom = Column(Geometry('POLYGON', 4674, from_text='ST_GeomFromEWKT', name='geometry'), index=True)
    id_produtor = Column(Integer)
    id_elementoprodutor = Column(Integer)
    cd_insumo_orgao = Column(Integer)
    nr_insumo_mes = Column(SmallInteger)
    nr_insumo_ano = Column(SmallInteger)
    tx_insumo_documento = Column(String(60))


class HidQuedaDaguaL(Base):
    __tablename__ = 'hid_queda_dagua_l'
    __table_args__ = {'schema': 'bcim'}

    id_objeto = Column(Integer, primary_key=True)
    nome = Column(String(100))
    nomeabrev = Column(String(50))
    geometriaaproximada = Column(String(3))
    altura = Column(Float(53))
    tipoqueda = Column(String(15))
    geom = Column(Geometry('LINESTRING', 4674, from_text='ST_GeomFromEWKT', name='geometry'), index=True)
    id_produtor = Column(Integer)
    id_elementoprodutor = Column(Integer)
    cd_insumo_orgao = Column(Integer)
    nr_insumo_mes = Column(SmallInteger)
    nr_insumo_ano = Column(SmallInteger)
    tx_insumo_documento = Column(String(60))


class HidRecifeA(Base):
    __tablename__ = 'hid_recife_a'
    __table_args__ = {'schema': 'bcim'}

    id_objeto = Column(Integer, primary_key=True)
    nome = Column(String(100))
    nomeabrev = Column(String(50))
    geometriaaproximada = Column(String(3))
    tiporecife = Column(String(16))
    situamare = Column(String(35))
    situacaocosta = Column(String(12))
    geom = Column(Geometry('POLYGON', 4674, from_text='ST_GeomFromEWKT', name='geometry'), index=True)
    id_produtor = Column(Integer)
    id_elementoprodutor = Column(Integer)
    cd_insumo_orgao = Column(Integer)
    nr_insumo_mes = Column(SmallInteger)
    nr_insumo_ano = Column(SmallInteger)
    tx_insumo_documento = Column(String(60))


class HidRochaEmAguaA(Base):
    __tablename__ = 'hid_rocha_em_agua_a'
    __table_args__ = {'schema': 'bcim'}

    id_objeto = Column(Integer, primary_key=True)
    nome = Column(String(100))
    nomeabrev = Column(String(50))
    geometriaaproximada = Column(String(3))
    alturalamina = Column(Float(53))
    situacaoemagua = Column(String(17))
    geom = Column(Geometry('POLYGON', 4674, from_text='ST_GeomFromEWKT', name='geometry'), index=True)
    id_produtor = Column(Integer)
    id_elementoprodutor = Column(Integer)
    cd_insumo_orgao = Column(Integer)
    nr_insumo_mes = Column(SmallInteger)
    nr_insumo_ano = Column(SmallInteger)
    tx_insumo_documento = Column(String(60))


class HidSumidouroVertedouroP(Base):
    __tablename__ = 'hid_sumidouro_vertedouro_p'
    __table_args__ = {'schema': 'bcim'}

    id_objeto = Column(Integer, primary_key=True)
    nome = Column(String(100))
    nomeabrev = Column(String(50))
    geometriaaproximada = Column(String(3))
    causa = Column(String(25))
    tiposumvert = Column(String(12))
    geom = Column(Geometry('POINT', 4674, from_text='ST_GeomFromEWKT', name='geometry'), index=True)
    id_produtor = Column(Integer)
    id_elementoprodutor = Column(Integer)
    cd_insumo_orgao = Column(Integer)
    nr_insumo_mes = Column(SmallInteger)
    nr_insumo_ano = Column(SmallInteger)
    tx_insumo_documento = Column(String(60))


class HidTerrenoSujeitoInundacaoA(Base):
    __tablename__ = 'hid_terreno_sujeito_inundacao_a'
    __table_args__ = {'schema': 'bcim'}

    id_objeto = Column(Integer, primary_key=True)
    nome = Column(String(100))
    nomeabrev = Column(String(50))
    geometriaaproximada = Column(String(3))
    periodicidadeinunda = Column(String(20))
    geom = Column(Geometry('POLYGON', 4674, from_text='ST_GeomFromEWKT', name='geometry'), index=True)
    id_produtor = Column(Integer)
    id_elementoprodutor = Column(Integer)
    cd_insumo_orgao = Column(Integer)
    nr_insumo_mes = Column(SmallInteger)
    nr_insumo_ano = Column(SmallInteger)
    tx_insumo_documento = Column(String(60))


class HidTrechoDrenagemL(Base):
    __tablename__ = 'hid_trecho_drenagem_l'
    __table_args__ = {'schema': 'bcim'}

    id_objeto = Column(Integer, primary_key=True)
    nome = Column(String(100))
    nomeabrev = Column(String(50))
    geometriaaproximada = Column(String(3))
    dentrodepoligono = Column(String(3))
    compartilhado = Column(String(3))
    eixoprincipal = Column(String(3))
    caladomax = Column(Float(53))
    larguramedia = Column(Float(53))
    velocidademedcorrente = Column(Float(53))
    profundidademedia = Column(Float(53))
    coincidecomdentrode = Column(String(35))
    navegabilidade = Column(String(16))
    regime = Column(String(31))
    geom = Column(Geometry('LINESTRING', 4674, from_text='ST_GeomFromEWKT', name='geometry'), index=True)
    id_produtor = Column(Integer)
    id_elementoprodutor = Column(Integer)
    cd_insumo_orgao = Column(Integer)
    nr_insumo_mes = Column(SmallInteger)
    nr_insumo_ano = Column(SmallInteger)
    tx_insumo_documento = Column(String(60))


class HidTrechoMassaDaguaA(Base):
    __tablename__ = 'hid_trecho_massa_dagua_a'
    __table_args__ = {'schema': 'bcim'}

    id_objeto = Column(Integer, primary_key=True)
    nome = Column(String(100))
    nomeabrev = Column(String(50))
    geometriaaproximada = Column(String(3))
    tipotrechomassa = Column(String(13))
    salinidade = Column(String(16))
    regime = Column(String(31))
    geom = Column(Geometry('POLYGON', 4674, from_text='ST_GeomFromEWKT', name='geometry'), index=True)
    id_produtor = Column(Integer)
    id_elementoprodutor = Column(Integer)
    cd_insumo_orgao = Column(Integer)
    nr_insumo_mes = Column(SmallInteger)
    nr_insumo_ano = Column(SmallInteger)
    tx_insumo_documento = Column(String(60))


class LimMunicipioA(Base):
    __tablename__ = 'lim_municipio_a'
    __table_args__ = {'schema': 'bcim'}

    id_objeto = Column(Integer, primary_key=True)
    nome = Column(String(100))
    nomeabrev = Column(String(50))
    geometriaaproximada = Column(String(3))
    geocodigo = Column(String(15))
    anodereferencia = Column(Integer)
    geom = Column(Geometry('MULTIPOLYGON', 4674, from_text='ST_GeomFromEWKT', name='geometry'), index=True)
    id_produtor = Column(Integer)
    id_elementoprodutor = Column(Integer)
    cd_insumo_orgao = Column(Integer)
    nr_insumo_mes = Column(SmallInteger)
    nr_insumo_ano = Column(SmallInteger)
    tx_insumo_documento = Column(String(60))


class LimOutrosLimitesOficiaisL(Base):
    __tablename__ = 'lim_outros_limites_oficiais_l'
    __table_args__ = {'schema': 'bcim'}

    id_objeto = Column(Integer, primary_key=True)
    nome = Column(String(100))
    nomeabrev = Column(String(50))
    geometriaaproximada = Column(String(3))
    coincidecomdentrode = Column(String(50))
    extensao = Column(Float(53))
    obssituacao = Column(String(100))
    tipooutlimofic = Column(String(50))
    geom = Column(Geometry('LINESTRING', 4674, from_text='ST_GeomFromEWKT', name='geometry'), index=True)
    id_produtor = Column(Integer)
    id_elementoprodutor = Column(Integer)
    cd_insumo_orgao = Column(Integer)
    nr_insumo_mes = Column(SmallInteger)
    nr_insumo_ano = Column(SmallInteger)
    tx_insumo_documento = Column(String(60))


class LimPaisA(Base):
    __tablename__ = 'lim_pais_a'
    __table_args__ = {'schema': 'bcim'}

    id_objeto = Column(Integer, primary_key=True)
    nome = Column(String(100))
    nomeabrev = Column(String(50))
    geometriaaproximada = Column(String(3))
    sigla = Column(String(3))
    codiso3166 = Column(CHAR(3))
    geom = Column(Geometry('MULTIPOLYGON', 4674, from_text='ST_GeomFromEWKT', name='geometry'), index=True)
    id_produtor = Column(Integer)
    id_elementoprodutor = Column(Integer)
    cd_insumo_orgao = Column(Integer)
    nr_insumo_mes = Column(SmallInteger)
    nr_insumo_ano = Column(SmallInteger)
    tx_insumo_documento = Column(String(60))


class LimTerraIndigenaA(Base):
    __tablename__ = 'lim_terra_indigena_a'
    __table_args__ = {'schema': 'bcim'}

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
    id_produtor = Column(Integer)
    id_elementoprodutor = Column(Integer)
    codigofunai = Column(Integer)
    cd_insumo_orgao = Column(Integer)
    nr_insumo_mes = Column(SmallInteger)
    nr_insumo_ano = Column(SmallInteger)
    tx_insumo_documento = Column(String(60))


class LimTerraIndigenaP(Base):
    __tablename__ = 'lim_terra_indigena_p'
    __table_args__ = {'schema': 'bcim'}

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
    geom = Column(Geometry('POINT', 4674, from_text='ST_GeomFromEWKT', name='geometry'), index=True)
    id_produtor = Column(Integer)
    id_elementoprodutor = Column(Integer)
    codigofunai = Column(Integer)
    cd_insumo_orgao = Column(Integer)
    nr_insumo_mes = Column(SmallInteger)
    nr_insumo_ano = Column(SmallInteger)
    tx_insumo_documento = Column(String(60))


class LimUnidadeConservacaoNaoSnucA(Base):
    __tablename__ = 'lim_unidade_conservacao_nao_snuc_a'
    __table_args__ = {'schema': 'bcim'}

    id_objeto = Column(Integer, primary_key=True)
    nome = Column(String(100))
    nomeabrev = Column(String(50))
    geometriaaproximada = Column(String(3))
    anocriacao = Column(Integer)
    sigla = Column(String(6))
    areaoficial = Column(String(15))
    administracao = Column(Text)
    classificacao = Column(String(100))
    atolegal = Column(String(100))
    geom = Column(Geometry('MULTIPOLYGON', 4674, from_text='ST_GeomFromEWKT', name='geometry'), index=True)
    id_produtor = Column(Integer)
    id_elementoprodutor = Column(Integer)
    cd_insumo_orgao = Column(Integer)
    nr_insumo_mes = Column(SmallInteger)
    nr_insumo_ano = Column(SmallInteger)
    tx_insumo_documento = Column(String(60))


class LimUnidadeFederacaoA(Base):
    __tablename__ = 'lim_unidade_federacao_a'
    __table_args__ = {'schema': 'bcim'}

    id_objeto = Column(Integer, primary_key=True)
    nome = Column(String(100))
    nomeabrev = Column(String(50))
    geometriaaproximada = Column(String(3))
    sigla = Column(String(3))
    geocodigo = Column(String(15))
    geom = Column(Geometry('MULTIPOLYGON', 4674, from_text='ST_GeomFromEWKT', name='geometry'), index=True)
    id_produtor = Column(Integer)
    id_elementoprodutor = Column(Integer)
    cd_insumo_orgao = Column(Integer)
    nr_insumo_mes = Column(SmallInteger)
    nr_insumo_ano = Column(SmallInteger)
    tx_insumo_documento = Column(String(60))
    regiao = Column(String)


class LimUnidadeProtecaoIntegralA(Base):
    __tablename__ = 'lim_unidade_protecao_integral_a'
    __table_args__ = {'schema': 'bcim'}

    id_objeto = Column(Integer, primary_key=True)
    nome = Column(String(100))
    nomeabrev = Column(String(50))
    geometriaaproximada = Column(String(3))
    anocriacao = Column(Integer)
    sigla = Column(String(6))
    areaoficial = Column(String(15))
    administracao = Column(Text)
    atolegal = Column(String(100))
    tipounidprotinteg = Column(String(100))
    geom = Column(Geometry('MULTIPOLYGON', 4674, from_text='ST_GeomFromEWKT', name='geometry'), index=True)
    id_produtor = Column(Integer)
    id_elementoprodutor = Column(Integer)
    cd_insumo_orgao = Column(Integer)
    nr_insumo_mes = Column(SmallInteger)
    nr_insumo_ano = Column(SmallInteger)
    tx_insumo_documento = Column(String(60))


class LimUnidadeUsoSustentavelA(Base):
    __tablename__ = 'lim_unidade_uso_sustentavel_a'
    __table_args__ = {'schema': 'bcim'}

    id_objeto = Column(Integer, primary_key=True)
    nome = Column(String(100))
    nomeabrev = Column(String(50))
    geometriaaproximada = Column(String(3))
    anocriacao = Column(Integer)
    sigla = Column(String(6))
    areaoficial = Column(String(15))
    administracao = Column(Text)
    atolegal = Column(String(100))
    tipounidusosust = Column(String(100))
    geom = Column(Geometry('MULTIPOLYGON', 4674, from_text='ST_GeomFromEWKT', name='geometry'), index=True)
    id_produtor = Column(Integer)
    id_elementoprodutor = Column(Integer)
    cd_insumo_orgao = Column(Integer)
    nr_insumo_mes = Column(SmallInteger)
    nr_insumo_ano = Column(SmallInteger)
    tx_insumo_documento = Column(String(60))


class LocAglomeradoRuralIsoladoP(Base):
    __tablename__ = 'loc_aglomerado_rural_isolado_p'
    __table_args__ = {'schema': 'bcim'}

    id_objeto = Column(Integer, primary_key=True)
    nome = Column(String(100))
    nomeabrev = Column(String(50))
    geometriaaproximada = Column(String(3))
    tipoaglomrurisol = Column(String(35))
    geom = Column(Geometry('POINT', 4674, from_text='ST_GeomFromEWKT', name='geometry'), index=True)
    id_produtor = Column(Integer)
    id_elementoprodutor = Column(Integer)
    cd_insumo_orgao = Column(Integer)
    nr_insumo_mes = Column(SmallInteger)
    nr_insumo_ano = Column(SmallInteger)
    tx_insumo_documento = Column(String(60))


class LocAldeiaIndigenaP(Base):
    __tablename__ = 'loc_aldeia_indigena_p'
    __table_args__ = {'schema': 'bcim'}

    id_objeto = Column(Integer, primary_key=True)
    nome = Column(String(100))
    nomeabrev = Column(String(50))
    geometriaaproximada = Column(String(3))
    codigofunai = Column(String(15))
    terraindigena = Column(String(100))
    etnia = Column(String(100))
    geom = Column(Geometry('POINT', 4674, from_text='ST_GeomFromEWKT', name='geometry'), index=True)
    id_produtor = Column(Integer)
    id_elementoprodutor = Column(Integer)
    cd_insumo_orgao = Column(Integer)
    nr_insumo_mes = Column(SmallInteger)
    nr_insumo_ano = Column(SmallInteger)
    tx_insumo_documento = Column(String(60))


class LocAreaEdificadaA(Base):
    __tablename__ = 'loc_area_edificada_a'
    __table_args__ = {'schema': 'bcim'}

    id_objeto = Column(Integer, primary_key=True)
    nome = Column(String(100))
    nomeabrev = Column(String(50))
    geometriaaproximada = Column(String(3))
    geocodigo = Column(String(15))
    geom = Column(Geometry('MULTIPOLYGON', 4674, from_text='ST_GeomFromEWKT', name='geometry'), index=True)
    id_produtor = Column(Integer)
    id_elementoprodutor = Column(Integer)
    cd_insumo_orgao = Column(Integer)
    nr_insumo_mes = Column(SmallInteger)
    nr_insumo_ano = Column(SmallInteger)
    tx_insumo_documento = Column(String(60))


class LocCapitalP(Base):
    __tablename__ = 'loc_capital_p'
    __table_args__ = {'schema': 'bcim'}

    id_objeto = Column(Integer, primary_key=True)
    nome = Column(String(100))
    nomeabrev = Column(String(50))
    geometriaaproximada = Column(String(3))
    tipocapital = Column(String(20))
    geom = Column(Geometry('POINT', 4674, from_text='ST_GeomFromEWKT', name='geometry'), index=True)
    id_produtor = Column(Integer)
    id_elementoprodutor = Column(Integer)
    cd_insumo_orgao = Column(Integer)
    nr_insumo_mes = Column(SmallInteger)
    nr_insumo_ano = Column(SmallInteger)
    tx_insumo_documento = Column(String(60))


class LocCidadeP(Base):
    __tablename__ = 'loc_cidade_p'
    __table_args__ = {'schema': 'bcim'}

    id_objeto = Column(Integer, primary_key=True)
    nome = Column(String(100))
    nomeabrev = Column(String(50))
    geometriaaproximada = Column(String(3))
    geom = Column(Geometry('POINT', 4674, from_text='ST_GeomFromEWKT', name='geometry'), index=True)
    id_produtor = Column(Integer)
    id_elementoprodutor = Column(Integer)
    cd_insumo_orgao = Column(Integer)
    nr_insumo_mes = Column(SmallInteger)
    nr_insumo_ano = Column(SmallInteger)
    tx_insumo_documento = Column(String(60))


class LocVilaP(Base):
    __tablename__ = 'loc_vila_p'
    __table_args__ = {'schema': 'bcim'}

    id_objeto = Column(Integer, primary_key=True)
    nome = Column(String(100))
    nomeabrev = Column(String(50))
    geometriaaproximada = Column(String(3))
    geom = Column(Geometry('POINT', 4674, from_text='ST_GeomFromEWKT', name='geometry'), index=True)
    id_produtor = Column(Integer)
    id_elementoprodutor = Column(Integer)
    cd_insumo_orgao = Column(Integer)
    nr_insumo_mes = Column(SmallInteger)
    nr_insumo_ano = Column(SmallInteger)
    tx_insumo_documento = Column(String(60))


class RelCurvaBatimetricaL(Base):
    __tablename__ = 'rel_curva_batimetrica_l'
    __table_args__ = {'schema': 'bcim'}

    id_objeto = Column(Integer, primary_key=True)
    profundidade = Column(Integer)
    geom = Column(Geometry('LINESTRING', 4674, from_text='ST_GeomFromEWKT', name='geometry'), index=True)
    id_produtor = Column(Integer)
    id_elementoprodutor = Column(Integer)
    cd_insumo_orgao = Column(Integer)
    nr_insumo_mes = Column(SmallInteger)
    nr_insumo_ano = Column(SmallInteger)
    tx_insumo_documento = Column(String(60))


class RelCurvaNivelL(Base):
    __tablename__ = 'rel_curva_nivel_l'
    __table_args__ = {'schema': 'bcim'}

    id_objeto = Column(Integer, primary_key=True)
    cota = Column(Integer)
    depressao = Column(String(3))
    geometriaaproximada = Column(String(3))
    indice = Column(String(16))
    geom = Column(Geometry('LINESTRING', 4674, from_text='ST_GeomFromEWKT', name='geometry'), index=True)
    id_produtor = Column(Integer)
    id_elementoprodutor = Column(Integer)
    cd_insumo_orgao = Column(Integer)
    nr_insumo_mes = Column(SmallInteger)
    nr_insumo_ano = Column(SmallInteger)
    tx_insumo_documento = Column(String(60))


class RelDunaA(Base):
    __tablename__ = 'rel_duna_a'
    __table_args__ = {'schema': 'bcim'}

    id_objeto = Column(Integer, primary_key=True)
    nome = Column(String(100))
    nomeabrev = Column(String(50))
    geometriaaproximada = Column(String(3))
    fixa = Column(String(3))
    geom = Column(Geometry('POLYGON', 4674, from_text='ST_GeomFromEWKT', name='geometry'), index=True)
    id_produtor = Column(Integer)
    id_elementoprodutor = Column(Integer)
    cd_insumo_orgao = Column(Integer)
    nr_insumo_mes = Column(SmallInteger)
    nr_insumo_ano = Column(SmallInteger)
    tx_insumo_documento = Column(String(60))


class RelElementoFisiograficoNaturalL(Base):
    __tablename__ = 'rel_elemento_fisiografico_natural_l'
    __table_args__ = {'schema': 'bcim'}

    id_objeto = Column(Integer, primary_key=True)
    nome = Column(String(100))
    nomeabrev = Column(String(50))
    geometriaaproximada = Column(String(3))
    tipoelemnat = Column(String(12))
    geom = Column(Geometry('LINESTRING', 4674, from_text='ST_GeomFromEWKT', name='geometry'), index=True)
    id_produtor = Column(Integer)
    id_elementoprodutor = Column(Integer)
    cd_insumo_orgao = Column(Integer)
    nr_insumo_mes = Column(SmallInteger)
    nr_insumo_ano = Column(SmallInteger)
    tx_insumo_documento = Column(String(60))


class RelElementoFisiograficoNaturalP(Base):
    __tablename__ = 'rel_elemento_fisiografico_natural_p'
    __table_args__ = {'schema': 'bcim'}

    id_objeto = Column(Integer, primary_key=True)
    nome = Column(String(100))
    nomeabrev = Column(String(50))
    geometriaaproximada = Column(String(3))
    tipoelemnat = Column(String(12))
    geom = Column(Geometry('POINT', 4674, from_text='ST_GeomFromEWKT', name='geometry'), index=True)
    id_produtor = Column(Integer)
    id_elementoprodutor = Column(Integer)
    cd_insumo_orgao = Column(Integer)
    nr_insumo_mes = Column(SmallInteger)
    nr_insumo_ano = Column(SmallInteger)
    tx_insumo_documento = Column(String(60))


class RelPicoP(Base):
    __tablename__ = 'rel_pico_p'
    __table_args__ = {'schema': 'bcim'}

    id_objeto = Column(Integer, primary_key=True)
    nome = Column(String(100))
    nomeabrev = Column(String(50))
    geometriaaproximada = Column(String(3))
    geom = Column(Geometry('POINT', 4674, from_text='ST_GeomFromEWKT', name='geometry'), index=True)
    id_produtor = Column(Integer)
    id_elementoprodutor = Column(Integer)
    cd_insumo_orgao = Column(Integer)
    nr_insumo_mes = Column(SmallInteger)
    nr_insumo_ano = Column(SmallInteger)
    tx_insumo_documento = Column(String(60))


class RelPontoCotadoAltimetricoP(Base):
    __tablename__ = 'rel_ponto_cotado_altimetrico_p'
    __table_args__ = {'schema': 'bcim'}

    id_objeto = Column(Integer, primary_key=True)
    geometriaaproximada = Column(String(3))
    cota = Column(Float(53))
    cotacomprovada = Column(String(3))
    geom = Column(Geometry('POINT', 4674, from_text='ST_GeomFromEWKT', name='geometry'), index=True)
    id_produtor = Column(Integer)
    id_elementoprodutor = Column(Integer)
    cd_insumo_orgao = Column(Integer)
    nr_insumo_mes = Column(SmallInteger)
    nr_insumo_ano = Column(SmallInteger)
    tx_insumo_documento = Column(String(60))


class RelPontoCotadoBatimetricoP(Base):
    __tablename__ = 'rel_ponto_cotado_batimetrico_p'
    __table_args__ = {'schema': 'bcim'}

    id_objeto = Column(Integer, primary_key=True)
    profundidade = Column(Float(53))
    geom = Column(Geometry('POINT', 4674, from_text='ST_GeomFromEWKT', name='geometry'), index=True)
    id_produtor = Column(Integer)
    id_elementoprodutor = Column(Integer)
    cd_insumo_orgao = Column(Integer)
    nr_insumo_mes = Column(SmallInteger)
    nr_insumo_ano = Column(SmallInteger)
    tx_insumo_documento = Column(String(60))


class TraEclusaL(Base):
    __tablename__ = 'tra_eclusa_l'
    __table_args__ = {'schema': 'bcim'}

    id_objeto = Column(Integer, primary_key=True)
    nome = Column(String(100))
    nomeabrev = Column(String(50))
    geometriaaproximada = Column(String(3))
    desnivel = Column(Float(53))
    largura = Column(Float(53))
    extensao = Column(Float(53))
    calado = Column(Float(53))
    matconstr = Column(String(18))
    operacional = Column(String(12))
    situacaofisica = Column(Text)
    geom = Column(Geometry('LINESTRING', 4674, from_text='ST_GeomFromEWKT', name='geometry'), index=True)
    id_produtor = Column(Integer)
    id_elementoprodutor = Column(Integer)
    cd_insumo_orgao = Column(Integer)
    nr_insumo_mes = Column(SmallInteger)
    nr_insumo_ano = Column(SmallInteger)
    tx_insumo_documento = Column(String(60))


class TraEdifConstAeroportuariaP(Base):
    __tablename__ = 'tra_edif_const_aeroportuaria_p'
    __table_args__ = {'schema': 'bcim'}

    id_objeto = Column(Integer, primary_key=True)
    nome = Column(String(100))
    nomeabrev = Column(String(50))
    geometriaaproximada = Column(String(3))
    operacional = Column(String(12))
    situacaofisica = Column(Text)
    administracao = Column(Text)
    matconstr = Column(String(18))
    tipoedifaero = Column(String(23))
    geom = Column(Geometry('POINT', 4674, from_text='ST_GeomFromEWKT', name='geometry'), index=True)
    id_produtor = Column(Integer)
    id_elementoprodutor = Column(Integer)
    cd_insumo_orgao = Column(Integer)
    nr_insumo_mes = Column(SmallInteger)
    nr_insumo_ano = Column(SmallInteger)
    tx_insumo_documento = Column(String(60))


class TraEdifConstPortuariaP(Base):
    __tablename__ = 'tra_edif_const_portuaria_p'
    __table_args__ = {'schema': 'bcim'}

    id_objeto = Column(Integer, primary_key=True)
    nome = Column(String(100))
    nomeabrev = Column(String(50))
    geometriaaproximada = Column(String(3))
    tipoedifport = Column(String(23))
    administracao = Column(Text)
    matconstr = Column(String(18))
    operacional = Column(String(12))
    situacaofisica = Column(Text)
    geom = Column(Geometry('POINT', 4674, from_text='ST_GeomFromEWKT', name='geometry'), index=True)
    id_produtor = Column(Integer)
    id_elementoprodutor = Column(Integer)
    cd_insumo_orgao = Column(Integer)
    nr_insumo_mes = Column(SmallInteger)
    nr_insumo_ano = Column(SmallInteger)
    tx_insumo_documento = Column(String(60))


class TraEdifMetroFerroviariaP(Base):
    __tablename__ = 'tra_edif_metro_ferroviaria_p'
    __table_args__ = {'schema': 'bcim'}

    id_objeto = Column(Integer, primary_key=True)
    nome = Column(String(100))
    nomeabrev = Column(String(50))
    geometriaaproximada = Column(String(3))
    multimodal = Column(String(12))
    funcaoedifmetroferrov = Column(String(44))
    operacional = Column(String(12))
    situacaofisica = Column(Text)
    administracao = Column(Text)
    matconstr = Column(String(18))
    geom = Column(Geometry('POINT', 4674, from_text='ST_GeomFromEWKT', name='geometry'), index=True)
    id_produtor = Column(Integer)
    id_elementoprodutor = Column(Integer)
    cd_insumo_orgao = Column(Integer)
    nr_insumo_mes = Column(SmallInteger)
    nr_insumo_ano = Column(SmallInteger)
    tx_insumo_documento = Column(String(60))


class TraPistaPontoPousoP(Base):
    __tablename__ = 'tra_pista_ponto_pouso_p'
    __table_args__ = {'schema': 'bcim'}

    id_objeto = Column(Integer, primary_key=True)
    nome = Column(String(100))
    geometriaaproximada = Column(String(3))
    nomeabrev = Column(String(50))
    largura = Column(Float(53))
    extensao = Column(Float(53))
    operacional = Column(String(12))
    situacaofisica = Column(Text)
    homologacao = Column(String(12))
    tipopista = Column(String(14))
    usopista = Column(String(15))
    revestimento = Column(Text)
    geom = Column(Geometry('POINT', 4674, from_text='ST_GeomFromEWKT', name='geometry'), index=True)
    id_produtor = Column(Integer)
    id_elementoprodutor = Column(Integer)
    cd_insumo_orgao = Column(Integer)
    nr_insumo_mes = Column(SmallInteger)
    nr_insumo_ano = Column(SmallInteger)
    tx_insumo_documento = Column(String(60))


class TraPonteL(Base):
    __tablename__ = 'tra_ponte_l'
    __table_args__ = {'schema': 'bcim'}

    id_objeto = Column(Integer, primary_key=True)
    nome = Column(String(100))
    geometriaaproximada = Column(String(3))
    nomeabrev = Column(String(50))
    tipoponte = Column(String(12))
    modaluso = Column(String(15))
    situacaofisica = Column(Text)
    operacional = Column(String(12))
    matconstr = Column(String(18))
    vaolivrehoriz = Column(Float(53))
    vaovertical = Column(Float(53))
    cargasuportmaxima = Column(Float(53))
    nrpistas = Column(Integer)
    nrfaixas = Column(Integer)
    extensao = Column(Float(53))
    largura = Column(Float(53))
    posicaopista = Column(String(13))
    geom = Column(Geometry('LINESTRING', 4674, from_text='ST_GeomFromEWKT', name='geometry'), index=True)
    id_produtor = Column(Integer)
    id_elementoprodutor = Column(Integer)
    cd_insumo_orgao = Column(Integer)
    nr_insumo_mes = Column(SmallInteger)
    nr_insumo_ano = Column(SmallInteger)
    tx_insumo_documento = Column(String(60))


class TraSinalizacaoP(Base):
    __tablename__ = 'tra_sinalizacao_p'
    __table_args__ = {'schema': 'bcim'}

    id_objeto = Column(Integer, primary_key=True)
    nome = Column(String(100))
    nomeabrev = Column(String(50))
    geometriaaproximada = Column(String(3))
    operacional = Column(String(12))
    situacaofisica = Column(Text)
    tiposinal = Column(String(21))
    geom = Column(Geometry('POINT', 4674, from_text='ST_GeomFromEWKT', name='geometry'), index=True)
    id_produtor = Column(Integer)
    id_elementoprodutor = Column(Integer)
    cd_insumo_orgao = Column(Integer)
    nr_insumo_mes = Column(SmallInteger)
    nr_insumo_ano = Column(SmallInteger)
    tx_insumo_documento = Column(String(60))


class TraTravessiaL(Base):
    __tablename__ = 'tra_travessia_l'
    __table_args__ = {'schema': 'bcim'}

    id_objeto = Column(Integer, primary_key=True)
    nome = Column(String(100))
    geometriaaproximada = Column(String(3))
    nomeabrev = Column(String(50))
    tipotravessia = Column(String(18))
    geom = Column(Geometry('LINESTRING', 4674, from_text='ST_GeomFromEWKT', name='geometry'), index=True)
    id_produtor = Column(Integer)
    id_elementoprodutor = Column(Integer)
    cd_insumo_orgao = Column(Integer)
    nr_insumo_mes = Column(SmallInteger)
    nr_insumo_ano = Column(SmallInteger)
    tx_insumo_documento = Column(String(60))


class TraTravessiaP(Base):
    __tablename__ = 'tra_travessia_p'
    __table_args__ = {'schema': 'bcim'}

    id_objeto = Column(Integer, primary_key=True)
    nome = Column(String(100))
    geometriaaproximada = Column(String(3))
    nomeabrev = Column(String(50))
    tipotravessia = Column(String(18))
    geom = Column(Geometry('POINT', 4674, from_text='ST_GeomFromEWKT', name='geometry'), index=True)
    id_produtor = Column(Integer)
    id_elementoprodutor = Column(Integer)
    cd_insumo_orgao = Column(Integer)
    nr_insumo_mes = Column(SmallInteger)
    nr_insumo_ano = Column(SmallInteger)
    tx_insumo_documento = Column(String(60))


class TraTrechoDutoL(Base):
    __tablename__ = 'tra_trecho_duto_l'
    __table_args__ = {'schema': 'bcim'}

    id_objeto = Column(Integer, primary_key=True)
    nome = Column(String(100))
    nomeabrev = Column(String(50))
    geometriaaproximada = Column(String(3))
    nrdutos = Column(Integer)
    tipotrechoduto = Column(String(22))
    mattransp = Column(String(12))
    setor = Column(String(21))
    posicaorelativa = Column(String(15))
    matconstr = Column(String(18))
    situacaoespacial = Column(String(11))
    operacional = Column(String(12))
    situacaofisica = Column(Text)
    geom = Column(Geometry('LINESTRING', 4674, from_text='ST_GeomFromEWKT', name='geometry'), index=True)
    id_produtor = Column(Integer)
    id_elementoprodutor = Column(Integer)
    cd_insumo_orgao = Column(Integer)
    nr_insumo_mes = Column(SmallInteger)
    nr_insumo_ano = Column(SmallInteger)
    tx_insumo_documento = Column(String(60))


class TraTrechoFerroviarioL(Base):
    __tablename__ = 'tra_trecho_ferroviario_l'
    __table_args__ = {'schema': 'bcim'}

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
    id_produtor = Column(Integer)
    id_elementoprodutor = Column(Integer)
    cd_insumo_orgao = Column(Integer)
    nr_insumo_mes = Column(SmallInteger)
    nr_insumo_ano = Column(SmallInteger)
    tx_insumo_documento = Column(String(60))


class TraTrechoHidroviarioL(Base):
    __tablename__ = 'tra_trecho_hidroviario_l'
    __table_args__ = {'schema': 'bcim'}

    id_objeto = Column(Integer, primary_key=True)
    nome = Column(String(100))
    nomeabrev = Column(String(50))
    geometriaaproximada = Column(String(3))
    extensaotrecho = Column(Float(53))
    caladomaxseca = Column(Float(53))
    operacional = Column(String(12))
    situacaofisica = Column(Text)
    regime = Column(String(31))
    geom = Column(Geometry('LINESTRING', 4674, from_text='ST_GeomFromEWKT', name='geometry'), index=True)
    id_produtor = Column(Integer)
    id_elementoprodutor = Column(Integer)
    cd_insumo_orgao = Column(Integer)
    nr_insumo_mes = Column(SmallInteger)
    nr_insumo_ano = Column(SmallInteger)
    tx_insumo_documento = Column(String(60))


class TraTrechoRodoviarioL(Base):
    __tablename__ = 'tra_trecho_rodoviario_l'
    __table_args__ = {'schema': 'bcim'}

    id_objeto = Column(Integer, primary_key=True)
    codtrechorodov = Column(String(25))
    tipotrechorod = Column(Text)
    jurisdicao = Column(Text)
    administracao = Column(Text)
    concessionaria = Column(String(100))
    revestimento = Column(Text)
    operacional = Column(String(12))
    situacaofisica = Column(Text)
    nrpistas = Column(Integer)
    nrfaixas = Column(Integer)
    trafego = Column(Text)
    capaccarga = Column(Numeric(19, 6))
    geom = Column(Geometry('LINESTRING', 4674, from_text='ST_GeomFromEWKT', name='geometry'), index=True)
    id_produtor = Column(Integer)
    id_elementoprodutor = Column(Integer)
    geometriaaproximada = Column(String(3))
    canteirodivisorio = Column(String(3))


class TraTunelL(Base):
    __tablename__ = 'tra_tunel_l'
    __table_args__ = {'schema': 'bcim'}

    id_objeto = Column(Integer, primary_key=True)
    nome = Column(String(100))
    geometriaaproximada = Column(String(3))
    nomeabrev = Column(String(50))
    modaluso = Column(String(15))
    nrpistas = Column(Integer)
    nrfaixas = Column(Integer)
    extensao = Column(Float(53))
    altura = Column(Float(53))
    largura = Column(Float(53))
    posicaopista = Column(String(13))
    situacaofisica = Column(Text)
    operacional = Column(String(12))
    matconstr = Column(String(18))
    tipotunel = Column(String(28))
    geom = Column(Geometry('LINESTRING', 4674, from_text='ST_GeomFromEWKT', name='geometry'), index=True)
    id_produtor = Column(Integer)
    id_elementoprodutor = Column(Integer)
    cd_insumo_orgao = Column(Integer)
    nr_insumo_mes = Column(SmallInteger)
    nr_insumo_ano = Column(SmallInteger)
    tx_insumo_documento = Column(String(60))


class VegBrejoPantanoA(Base):
    __tablename__ = 'veg_brejo_pantano_a'
    __table_args__ = {'schema': 'bcim'}

    id_objeto = Column(Integer, primary_key=True)
    nome = Column(String(100))
    nomeabrev = Column(String(50))
    geometriaaproximada = Column(String(3))
    alturamediaindividuos = Column(Float(53))
    classificacaoporte = Column(String(12))
    tipobrejopantano = Column(String(27))
    denso = Column(String(12))
    antropizada = Column(String(23))
    geom = Column(Geometry('POLYGON', 4674, from_text='ST_GeomFromEWKT', name='geometry'), index=True)
    id_produtor = Column(Integer)
    id_elementoprodutor = Column(Integer)
    cd_insumo_orgao = Column(Integer)
    nr_insumo_mes = Column(SmallInteger)
    nr_insumo_ano = Column(SmallInteger)
    tx_insumo_documento = Column(String(60))


class VegMangueA(Base):
    __tablename__ = 'veg_mangue_a'
    __table_args__ = {'schema': 'bcim'}

    id_objeto = Column(Integer, primary_key=True)
    nome = Column(String(100))
    nomeabrev = Column(String(50))
    geometriaaproximada = Column(String(3))
    alturamediaindividuos = Column(Float(53))
    classificacaoporte = Column(String(12))
    denso = Column(String(12))
    antropizada = Column(String(23))
    geom = Column(Geometry('POLYGON', 4674, from_text='ST_GeomFromEWKT', name='geometry'), index=True)
    id_produtor = Column(Integer)
    id_elementoprodutor = Column(Integer)
    cd_insumo_orgao = Column(Integer)
    nr_insumo_mes = Column(SmallInteger)
    nr_insumo_ano = Column(SmallInteger)
    tx_insumo_documento = Column(String(60))


class VegVegRestingaA(Base):
    __tablename__ = 'veg_veg_restinga_a'
    __table_args__ = {'schema': 'bcim'}

    id_objeto = Column(Integer, primary_key=True)
    nome = Column(String(100))
    nomeabrev = Column(String(50))
    geometriaaproximada = Column(String(3))
    alturamediaindividuos = Column(Float(53))
    classificacaoporte = Column(String(12))
    denso = Column(String(12))
    antropizada = Column(String(23))
    geom = Column(Geometry('POLYGON', 4674, from_text='ST_GeomFromEWKT', name='geometry'), index=True)
    id_produtor = Column(Integer)
    id_elementoprodutor = Column(Integer)
    cd_insumo_orgao = Column(Integer)
    nr_insumo_mes = Column(SmallInteger)
    nr_insumo_ano = Column(SmallInteger)
    tx_insumo_documento = Column(String(60))
