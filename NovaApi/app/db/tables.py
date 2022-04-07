from app.db.init_db import get_pool

async def ensure_tables():
    pool = await get_pool()

    async with pool.acquire() as connection:
        async with connection.transaction():
            await connection.execute("""
                CREATE TABLE IF NOT EXISTS Accounts(
                    account_id TEXT PRIMARY KEY,
                    account_name TEXT NOT NULL,
                    created_by TEXT,
                    updated_by TEXT,
                    created_at TIMESTAMP NOT NULL DEFAULT CURRENT_TIMESTAMP,
                    updated_at TIMESTAMP,
                    deleted boolean NOT NULL DEFAULT false
                )
            """)

            await connection.execute("""
                CREATE TABLE IF NOT EXISTS Transactions(
                    transaction_id serial PRIMARY KEY,
                    account_id TEXT NOT NULL,
                    amount BIGINT NOT NULL,
                    transaction_type TEXT NOT NULL,
                    comment TEXT,
                    created_by TEXT,
                    updated_by TEXT,
                    created_at TIMESTAMP NOT NULL DEFAULT CURRENT_TIMESTAMP,
                    updated_at TIMESTAMP,
                    deleted boolean NOT NULL DEFAULT false,
                    FOREIGN KEY (account_id)
                        REFERENCES Accounts (account_id)
                )
            """)

            await connection.execute("""
                CREATE TABLE IF NOT EXISTS WowCharacters(
                    character_id serial PRIMARY KEY,
                    name TEXT NOT NULL,
                    realm TEXT NOT NULL,
                    faction TEXT NOT NULL,
                    server TEXT NOT NULL,
                    character_class TEXT NOT NULL,
                    account_id TEXT NOT NULL,
                    paymentcharacter BOOL NOT NULL DEFAULT false,
                    created_by TEXT,
                    updated_by TEXT,
                    created_at TIMESTAMP NOT NULL DEFAULT CURRENT_TIMESTAMP,
                    updated_at TIMESTAMP,
                    deleted boolean NOT NULL DEFAULT false,
                    FOREIGN KEY (account_id)
                        REFERENCES Accounts (account_id),
                    UNIQUE(name, realm, faction, server, character_class, account_id)
                )
            """)