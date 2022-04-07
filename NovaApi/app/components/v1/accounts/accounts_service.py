from typing import Dict, List
from app.components.v1.common.base_sql_service import BaseSqlService
from .account import Account, WowCharacter


class AccountService(BaseSqlService):
    async def insert_account(self, account: Account):
        await self.execute("""
            INSERT INTO Accounts(account_id, account_name)
            VALUES ($1, $2);
        """, account.account_id, account.account_name)

    async def get_account_balance(self, account_id: int) -> int:
        return await self.fetchval("""
            SELECT SUM(amount) 
            FROM Transactions
            WHERE account_id = $1 and deleted = false;
        """, account_id)

    async def get_all_accounts(self) -> List[Account]:
        accounts = await self.fetch("""
            SELECT * FROM Accounts WHERE deleted = false;
        """)

        if not accounts:
            return []
        return [Account(**account) for account in accounts]

    async def get_all_accounts_with_balance(self) -> List[Account]:
        accounts = await self.fetch("""
            SELECT 
                a.account_id as account_id,
                a.account_name as account_name,
                SUM(t.amount) as balance 
             FROM Accounts a
             LEFT JOIN Transactions t ON t.account_id = a.account_id AND t.deleted = false
             WHERE a.deleted = false
             GROUP BY (a.account_id)
        """)

        if not accounts:
            return []
        return [Account(**account) for account in accounts]

    async def get_all_accounts_with_wowcharacters(self) -> List[Account]:
        accounts = await self.get_all_accounts()
        wow_chars = await self.get_all_wow_characters()

        for account in accounts:
            account.wow_characters = wow_chars.get(account.account_id, [])

        return accounts

    async def get_all_accounts_with_wowcharacters_and_balance(self) -> List[Account]:
        accounts = await self.get_all_accounts_with_balance()
        wow_chars = await self.get_all_wow_characters()

        for account in accounts:
            account.wow_characters = wow_chars.get(account.account_id, [])
        
        return accounts

    async def get_all_wow_characters(self) -> Dict[str, WowCharacter]:
        wowchars = await self.fetch("SELECT * FROM WowCharacters WHERE deleted = false")
        lookup = {}

        for char in wowchars:
            lookup.setdefault(char["account_id"], []).append(WowCharacter(**char))

        return lookup

service = AccountService()
