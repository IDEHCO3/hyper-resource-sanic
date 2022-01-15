from sqlalchemy import create_engine, text
URLDB="postgresql://postgres:desenv@127.0.0.1:5432/postgres"

engine = create_engine(URLDB)
conn = engine.connect()
sql = 'select * from bc250_2019.lml_unidade_federacao_a'
result = conn.execute(text(sql))
print(result)
print(type(result))
conn.close()