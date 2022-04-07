from app.db.init_db import get_pool


class BaseSqlService:
    async def execute(self, sql, *args):
        pool = await get_pool()

        async with pool.acquire() as connection:
            async with connection.transaction():
                await connection.execute(sql, *args)

    async def fetchval(self, sql, *args):
        pool = await get_pool()

        async with pool.acquire() as connection:
            async with connection.transaction():
                return await connection.fetchval(sql, *args)

    async def fetch(self, sql, *args):
        pool = await get_pool()

        async with pool.acquire() as connection:
            async with connection.transaction():
                return await connection.fetch(sql, *args)
