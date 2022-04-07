from app.components.v1.common.base_sql_service import BaseSqlService
from asyncpg.exceptions import ForeignKeyViolationError
from fastapi import HTTPException

from app.db.init_db import get_pool
from .transaction import Transaction


class TransactionService(BaseSqlService):
    async def delete_transaction(self, transaction_id: int):
        return await self.execute("UPDATE Transactions SET deleted=true WHERE transaction_id = $1", transaction_id)

    async def insert_transaction(self, transaction: Transaction) -> int:
        pool = await get_pool()

        try:
            async with pool.acquire() as connection:
                async with connection.transaction():
                    return await connection.fetchval("""
                        WITH ensure_account AS (
                            INSERT INTO Accounts(account_id, account_name)
                            VALUES ($1, 'Nova balance account')
                            ON CONFLICT DO NOTHING
                        )
                        INSERT INTO Transactions(account_id, amount, transaction_type, comment)
                        VALUES ($1, $2, $3, $4)
                        RETURNING transaction_id
                    """, transaction.account_id, transaction.amount, transaction.transaction_type, transaction.comment)
        except ForeignKeyViolationError:
            raise HTTPException(status_code=404, detail=f"Account with ID {transaction.account_id} was not found")

    async def get_all_transactions(self, account_id = None):
        pool = await get_pool()

        async with pool.acquire() as connection:
            async with connection.transaction():
                if account_id:
                    return await connection.fetch("""
                        SELECT 
                            t.transaction_id as transaction_id,
                            t.amount as amount,
                            t.transaction_type as transaction_type,
                            t.comment as comment,
                            t.created_at as created_at,
                            t.created_by as created_by,
                            t.updated_at as updated_at,
                            t.updated_by as updated_by,
                            w.character_id as character_id,
                            w.name as name,
                            w.realm as realm,
                            w.faction as faction,
                            w.server as server,
                            w.character_class as character_class,
                            w.account_id as account_id,
                            w.paymentcharacter as paymentcharacter
                        FROM Transactions t
                        JOIN WowCharacters w ON w.account_id = t.account_id
                        WHERE w.paymentcharacter = true and t.account_id = $1
                            AND w.deleted = false AND t.deleted = false
                    """, account_id)
                else:
                    return await connection.fetch("""
                        SELECT 
                            t.transaction_id as transaction_id,
                            t.amount as amount,
                            t.transaction_type as transaction_type,
                            t.comment as comment,
                            t.created_at as created_at,
                            t.created_by as created_by,
                            t.updated_at as updated_at,
                            t.updated_by as updated_by,
                            w.character_id as character_id,
                            w.name as name,
                            w.realm as realm,
                            w.faction as faction,
                            w.server as server,
                            w.character_class as character_class,
                            w.account_id as account_id,
                            w.paymentcharacter as paymentcharacter
                        FROM Transactions t
                        JOIN WowCharacters w ON w.account_id = t.account_id
                        WHERE w.paymentcharacter = true and t.deleted = false and w.deleted = false
                    """)


service = TransactionService()
