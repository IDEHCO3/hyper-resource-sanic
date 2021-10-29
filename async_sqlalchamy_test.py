import asyncio

from sqlalchemy.ext.asyncio import create_async_engine
from sqlalchemy import text
from sqlalchemy.future import select


async def async_main():
    URLDB = "postgresql+asyncpg://postgres:desenv@127.0.0.1:5432/postgres"
    engine = create_async_engine(URLDB, echo=True,)
    async with engine.connect() as conn:

        # select a Result, which will be delivered with buffered
        # results
        t = text("SELECT * FROM bc250_2019.lml_unidade_federacao_a")
        print("----------------------------------------------------")
        print(t)
        print("----------------------------------------------------")
        result = await conn.execute(t)
        #print(result.fetchall())
        #async_result = await conn.stream()
        sub_query = "SELECT * FROM bc250_2019.lml_unidade_federacao_a"
        query = f"SELECT  ST_AsGeobuf(q, 'geom') FROM ({sub_query}) AS q"
        t = text(query)
        print("----------------------------------------------------")
        print(t)
        print("----------------------------------------------------")
        result = await conn.execute(t)
        fetch_all = result.fetchall()
        print(fetch_all[0][0])
    # for AsyncEngine created in function scope, close and
    # clean-up pooled connections
    await engine.dispose()

asyncio.run(async_main())