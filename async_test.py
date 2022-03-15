import asyncio

from src.models.lim_unidade_federacao_a import LimUnidadeFederacaoA
from src.orm.database_postgis import DialectDbPostgis
from src.url_interpreter.interpreter_new import InterpreterNew
db = DialectDbPostgis(None, LimUnidadeFederacaoA.__table__, LimUnidadeFederacaoA)
url = "/projection/sigla,geom/offset-limit/5&2/collect/sigla&geom/buffer/0.8"
interp = InterpreterNew(url,LimUnidadeFederacaoA, db)
url = "/projection/sigla,geom/offset-limit/5&2/collect/sigla&geom/buffer/0.8"
#???
url = "/sigla,geom/filter/sigla/eq/RJ/and/geom/collect/gt/10/offset-limit/5&2/collect/sigla&geom/buffer/0.8"
async def test_code():
    res = interp.words()
    print(res)
    res = await interp.get_tokens()
    print(res)

asyncio.run(test_code())

