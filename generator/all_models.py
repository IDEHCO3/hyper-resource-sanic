# coding: utf-8
from sqlalchemy import CHAR, Column, Float, Integer, Numeric, SmallInteger, String, Text
from sqlalchemy.sql.sqltypes import NullType
from sqlalchemy.ext.declarative import declarative_base

Base = declarative_base()
metadata = Base.metadata


class EdifPubMilitarA(Base):
    __tablename__ = 'adm_edif_pub_militar_a'
    __table_args__ = {'schema': 'bcim'}

    id = Column('id_objeto', Integer, primary_key=True)
    nome = Column(String(100))
    nomeabrev = Column(String(50))
    geometriaaproximada = Column(String(3))
    tipoedifmil = Column(String(26))
    tipousoedif = Column(String(21))
    situacaofisica = Column(Text)
    operacional = Column(String(12))
    matconstr = Column(String(18))



class EdifPubMilitarP(Base):
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


class PostoFiscalP(Base):
    __tablename__ = 'adm_posto_fiscal_p'
    __table_args__ = {'schema': 'bcim'}

    id_objeto = Column(Integer, primary_key=True)
    nome = Column(String(100))
    nomeabrev = Column(String(50))
    geometriaaproximada = Column(String(3))
    operacional = Column(String(12))
    situacaofisica = Column(Text)
    tipopostofisc = Column(String(22))

class EdifAgropecExtVegetalPescaP(Base):
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
    

class ExtMineralA(Base):
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
    
class ExtMineralP(Base):
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
    
class EstGeradEnergiaEletricaP(Base):
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
    

class etricaP(Base):
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
    
class TermeletricaP(Base):
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
    

class BancoAreiaA(Base):
    __tablename__ = 'hid_banco_areia_a'
    __table_args__ = {'schema': 'bcim'}

    id_objeto = Column(Integer, primary_key=True)
    nome = Column(String(100))
    nomeabrev = Column(String(50))
    geometriaaproximada = Column(String(3))
    tipobanco = Column(String(14))
    situacaoemagua = Column(String(17))
    materialpredominante = Column(String(27))
    

class BarragemL(Base):
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
    

class BarragemP(Base):
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
    

class CorredeiraL(Base):
    __tablename__ = 'hid_corredeira_l'
    __table_args__ = {'schema': 'bcim'}

    id_objeto = Column(Integer, primary_key=True)
    nome = Column(String(100))
    nomeabrev = Column(String(50))
    geometriaaproximada = Column(String(3))
    

class CorredeiraP(Base):
    __tablename__ = 'hid_corredeira_p'
    __table_args__ = {'schema': 'bcim'}

    id_objeto = Column(Integer, primary_key=True)
    nome = Column(String(100))
    nomeabrev = Column(String(50))
    geometriaaproximada = Column(String(3))
    

class IlhaA(Base):
    __tablename__ = 'hid_ilha_a'
    __table_args__ = {'schema': 'bcim'}

    id_objeto = Column(Integer, primary_key=True)
    nome = Column(String(100))
    nomeabrev = Column(String(50))
    geometriaaproximada = Column(String(3))
    tipoilha = Column(String(8))
    

class MassaDaguaA(Base):
    __tablename__ = 'hid_massa_dagua_a'
    __table_args__ = {'schema': 'bcim'}

    id_objeto = Column(Integer, primary_key=True)
    nome = Column(String(100))
    nomeabrev = Column(String(50))
    geometriaaproximada = Column(String(3))
    tipomassadagua = Column(String(18))
    salinidade = Column(String(16))
    regime = Column(String(31))
    

class QuedaDaguaL(Base):
    __tablename__ = 'hid_queda_dagua_l'
    __table_args__ = {'schema': 'bcim'}

    id_objeto = Column(Integer, primary_key=True)
    nome = Column(String(100))
    nomeabrev = Column(String(50))
    geometriaaproximada = Column(String(3))
    altura = Column(Float(53))
    tipoqueda = Column(String(15))
    


class RecifeA(Base):
    __tablename__ = 'hid_recife_a'
    __table_args__ = {'schema': 'bcim'}

    id_objeto = Column(Integer, primary_key=True)
    nome = Column(String(100))
    nomeabrev = Column(String(50))
    geometriaaproximada = Column(String(3))
    tiporecife = Column(String(16))
    situamare = Column(String(35))
    situacaocosta = Column(String(12))
    geom = Column(NullType)
    id_produtor = Column(Integer)
    id_elementoprodutor = Column(Integer)
    cd_insumo_orgao = Column(Integer)
    nr_insumo_mes = Column(SmallInteger)
    nr_insumo_ano = Column(SmallInteger)
    tx_insumo_documento = Column(String(60))


class RochaEmAguaA(Base):
    __tablename__ = 'hid_rocha_em_agua_a'
    __table_args__ = {'schema': 'bcim'}

    id_objeto = Column(Integer, primary_key=True)
    nome = Column(String(100))
    nomeabrev = Column(String(50))
    geometriaaproximada = Column(String(3))
    alturalamina = Column(Float(53))
    situacaoemagua = Column(String(17))
    

class SumidouroVertedouroP(Base):
    __tablename__ = 'hid_sumidouro_vertedouro_p'
    __table_args__ = {'schema': 'bcim'}

    id_objeto = Column(Integer, primary_key=True)
    nome = Column(String(100))
    nomeabrev = Column(String(50))
    geometriaaproximada = Column(String(3))
    causa = Column(String(25))
    tiposumvert = Column(String(12))
    

class TerrenoSujeitoInundacaoA(Base):
    __tablename__ = 'hid_terreno_sujeito_inundacao_a'
    __table_args__ = {'schema': 'bcim'}

    id_objeto = Column(Integer, primary_key=True)
    nome = Column(String(100))
    nomeabrev = Column(String(50))
    geometriaaproximada = Column(String(3))
    periodicidadeinunda = Column(String(20))
    

class TrechoDrenagemL(Base):
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
    

class TrechoMassaDaguaA(Base):
    __tablename__ = 'hid_trecho_massa_dagua_a'
    __table_args__ = {'schema': 'bcim'}

    id_objeto = Column(Integer, primary_key=True)
    nome = Column(String(100))
    nomeabrev = Column(String(50))
    geometriaaproximada = Column(String(3))
    tipotrechomassa = Column(String(13))
    salinidade = Column(String(16))
    regime = Column(String(31))
    

class MunicipioA(Base):
    __tablename__ = 'lim_municipio_a'
    __table_args__ = {'schema': 'bcim'}

    id_objeto = Column(Integer, primary_key=True)
    nome = Column(String(100))
    nomeabrev = Column(String(50))
    geometriaaproximada = Column(String(3))
    geocodigo = Column(String(15))
    anodereferencia = Column(Integer)


class OutrosLimitesOficiaisL(Base):
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


class PaisA(Base):
    __tablename__ = 'lim_pais_a'
    __table_args__ = {'schema': 'bcim'}

    id_objeto = Column(Integer, primary_key=True)
    nome = Column(String(100))
    nomeabrev = Column(String(50))
    geometriaaproximada = Column(String(3))
    sigla = Column(String(3))
    codiso3166 = Column(CHAR(3))


class TerraIndigenaA(Base):
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


class TerraIndigenaP(Base):
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


class UnidadeConservacaoNaoSnucA(Base):
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

class UnidadeFederacaoA(Base):
    __tablename__ = 'lim_unidade_federacao_a'
    __table_args__ = {'schema': 'bcim'}

    id_objeto = Column(Integer, primary_key=True)
    nome = Column(String(100))
    nomeabrev = Column(String(50))
    geometriaaproximada = Column(String(3))
    sigla = Column(String(3))
    geocodigo = Column(String(15))


class UnidadeProtecaoIntegralA(Base):
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

class UnidadeUsoSustentavelA(Base):
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

class AglomeradoRuralIsoladoP(Base):
    __tablename__ = 'loc_aglomerado_rural_isolado_p'
    __table_args__ = {'schema': 'bcim'}

    id_objeto = Column(Integer, primary_key=True)
    nome = Column(String(100))
    nomeabrev = Column(String(50))
    geometriaaproximada = Column(String(3))
    tipoaglomrurisol = Column(String(35))


class AldeiaIndigenaP(Base):
    __tablename__ = 'loc_aldeia_indigena_p'
    __table_args__ = {'schema': 'bcim'}

    id_objeto = Column(Integer, primary_key=True)
    nome = Column(String(100))
    nomeabrev = Column(String(50))
    geometriaaproximada = Column(String(3))
    codigofunai = Column(String(15))
    terraindigena = Column(String(100))
    etnia = Column(String(100))

class AreaEdificadaA(Base):
    __tablename__ = 'loc_area_edificada_a'
    __table_args__ = {'schema': 'bcim'}

    id_objeto = Column(Integer, primary_key=True)
    nome = Column(String(100))
    nomeabrev = Column(String(50))
    geometriaaproximada = Column(String(3))
    geocodigo = Column(String(15))


class CapitalP(Base):
    __tablename__ = 'loc_capital_p'
    __table_args__ = {'schema': 'bcim'}

    id_objeto = Column(Integer, primary_key=True)
    nome = Column(String(100))
    nomeabrev = Column(String(50))
    geometriaaproximada = Column(String(3))
    tipocapital = Column(String(20))


class CidadeP(Base):
    __tablename__ = 'loc_cidade_p'
    __table_args__ = {'schema': 'bcim'}

    id_objeto = Column(Integer, primary_key=True)
    nome = Column(String(100))
    nomeabrev = Column(String(50))
    geometriaaproximada = Column(String(3))


class VilaP(Base):
    __tablename__ = 'loc_vila_p'
    __table_args__ = {'schema': 'bcim'}

    id_objeto = Column(Integer, primary_key=True)
    nome = Column(String(100))
    nomeabrev = Column(String(50))
    geometriaaproximada = Column(String(3))


class CurvaBatimetricaL(Base):
    __tablename__ = 'rel_curva_batimetrica_l'
    __table_args__ = {'schema': 'bcim'}

    id_objeto = Column(Integer, primary_key=True)
    profundidade = Column(Integer)

class CurvaNivelL(Base):
    __tablename__ = 'rel_curva_nivel_l'
    __table_args__ = {'schema': 'bcim'}

    id_objeto = Column(Integer, primary_key=True)
    cota = Column(Integer)
    depressao = Column(String(3))
    geometriaaproximada = Column(String(3))
    indice = Column(String(16))

class DunaA(Base):
    __tablename__ = 'rel_duna_a'
    __table_args__ = {'schema': 'bcim'}

    id_objeto = Column(Integer, primary_key=True)
    nome = Column(String(100))
    nomeabrev = Column(String(50))
    geometriaaproximada = Column(String(3))
    fixa = Column(String(3))

class ElementoFisiograficoNaturalL(Base):
    __tablename__ = 'rel_elemento_fisiografico_natural_l'
    __table_args__ = {'schema': 'bcim'}

    id_objeto = Column(Integer, primary_key=True)
    nome = Column(String(100))
    nomeabrev = Column(String(50))
    geometriaaproximada = Column(String(3))
    tipoelemnat = Column(String(12))
    
class ElementoFisiograficoNaturalP(Base):
    __tablename__ = 'rel_elemento_fisiografico_natural_p'
    __table_args__ = {'schema': 'bcim'}

    id_objeto = Column(Integer, primary_key=True)
    nome = Column(String(100))
    nomeabrev = Column(String(50))
    geometriaaproximada = Column(String(3))
    tipoelemnat = Column(String(12))
    

class PicoP(Base):
    __tablename__ = 'rel_pico_p'
    __table_args__ = {'schema': 'bcim'}

    id_objeto = Column(Integer, primary_key=True)
    nome = Column(String(100))
    nomeabrev = Column(String(50))
    geometriaaproximada = Column(String(3))
    

class PontoCotadoAltimetricoP(Base):
    __tablename__ = 'rel_ponto_cotado_altimetrico_p'
    __table_args__ = {'schema': 'bcim'}

    id_objeto = Column(Integer, primary_key=True)
    geometriaaproximada = Column(String(3))
    cota = Column(Float(53))
    cotacomprovada = Column(String(3))
    

class PontoCotadoBatimetricoP(Base):
    __tablename__ = 'rel_ponto_cotado_batimetrico_p'
    __table_args__ = {'schema': 'bcim'}

    id_objeto = Column(Integer, primary_key=True)
    profundidade = Column(Float(53))
    

class EclusaL(Base):
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
    


class EdifConstAeroportuariaP(Base):
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


class EdifConstPortuariaP(Base):
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


class EdifMetroFerroviariaP(Base):
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


class PistaPontoPousoP(Base):
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


class PonteL(Base):
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

class SinalizacaoP(Base):
    __tablename__ = 'tra_sinalizacao_p'
    __table_args__ = {'schema': 'bcim'}

    id_objeto = Column(Integer, primary_key=True)
    nome = Column(String(100))
    nomeabrev = Column(String(50))
    geometriaaproximada = Column(String(3))
    operacional = Column(String(12))
    situacaofisica = Column(Text)
    tiposinal = Column(String(21))


class TravessiaL(Base):
    __tablename__ = 'tra_travessia_l'
    __table_args__ = {'schema': 'bcim'}

    id_objeto = Column(Integer, primary_key=True)
    nome = Column(String(100))
    geometriaaproximada = Column(String(3))
    nomeabrev = Column(String(50))
    tipotravessia = Column(String(18))


class TravessiaP(Base):
    __tablename__ = 'tra_travessia_p'
    __table_args__ = {'schema': 'bcim'}

    id_objeto = Column(Integer, primary_key=True)
    nome = Column(String(100))
    geometriaaproximada = Column(String(3))
    nomeabrev = Column(String(50))
    tipotravessia = Column(String(18))


class TrechoDutoL(Base):
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


class TrechoFerroviarioL(Base):
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


class TrechoHidroviarioL(Base):
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


class TrechoRodoviarioL(Base):
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

class TunelL(Base):
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


class BrejoPantanoA(Base):
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


class MangueA(Base):
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
    

class RestingaA(Base):
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
    