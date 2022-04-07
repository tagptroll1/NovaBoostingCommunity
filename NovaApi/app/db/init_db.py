import asyncpg

from app.config import settings

pool = None

async def get_pool() -> asyncpg.Pool:
    global pool

    if not pool:
        print(settings.DATABASE_URI)
        try:
            pool = await asyncpg.create_pool(settings.DATABASE_URI)
        except asyncpg.InvalidCatalogNameError:
            # Database does not exist, create it.
            sys_conn = await asyncpg.connect(
                database='template1',
                user=settings.POSTGRES_USER,
                password=settings.POSTGRES_PASSWORD
            )
            await sys_conn.execute(
                f'CREATE DATABASE "{settings.POSTGRES_DB}" OWNER "{settings.POSTGRES_USER}"'
            )
            await sys_conn.close()

            # Connect to the newly created database.
            pool = await asyncpg.create_pool(settings.DATABASE_URI)
    return pool