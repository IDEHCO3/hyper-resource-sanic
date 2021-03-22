from sqlalchemy import create_engine
from sqlalchemy.sql.expression import select
from sqlalchemy.orm import Session
from src.models.lim_unidade_federacao_a import LimUnidadeFederacaoA
URLDB="postgresql://postgres:desenv@127.0.0.1:5432/postgres"
engine = create_engine(URLDB, echo=True, future=True)
session = Session(engine)
from osgeo import ogr
uf = session.execute(select(LimUnidadeFederacaoA).filter_by(sigla="RJ")).scalar_one()