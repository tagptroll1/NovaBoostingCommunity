import aiohttp
import re
from asyncpg.exceptions import ForeignKeyViolationError
from fastapi import HTTPException

from app.db.init_db import get_pool
from app.components.v1.common.base_sql_service import BaseSqlService
from .wow_character import ChangePaymentCharacterBody, RaiderIOResponse, WowCharacter, WowCharacterUrlRegisterBody

RAIDERIO_LINK = r"https:\/\/raider\.io\/characters\/(.+)\/(.+)\/([^?.]+)"
raiderio_regex = re.compile(RAIDERIO_LINK)

class WowCharacterService(BaseSqlService):
    async def set_paymentcharacter(self, body: ChangePaymentCharacterBody):
        pool = await get_pool()

        if body.character_id:
            async with pool.acquire() as connection:
                async with connection.transaction():
                    await connection.execute("""
                        UPDATE WowCharacters
                        SET paymentcharacter = CASE
                            WHEN character_id = $1 
                            THEN true
                            ELSE false
                            END
                        WHERE account_id = $2 and deleted = false
                    """, body.character_id, body.account_id)
                    return

        elif body.raiderio_url:
            match = raiderio_regex.findall(body.raiderio_url)

            if not match:
                raise HTTPException(
                    status_code=404,
                    detail=f"Not a valid raiderio url")

            server = match[0][0]
            realm = match[0][1]
            char = match[0][2]

        elif body.name and body.realm and body.region:
            server = body.region
            realm = body.realm
            char = body.name

        else:
            raise HTTPException(
                status_code=400,
                detail=f"Invalid body")

        async with pool.acquire() as connection:
                async with connection.transaction():
                    await connection.execute("""
                        UPDATE WowCharacters
                        SET paymentcharacter = CASE
                            WHEN INITCAP(name) = INITCAP($1)
                                AND LOWER(realm) = LOWER($2)
                                AND LOWER(server) = LOWER($3)
                            THEN true
                            ELSE false
                            END
                        WHERE account_id = $4 and deleted = false
                    """, char, realm, server, body.account_id)
        
    async def register_wow_character(self, register_body: WowCharacterUrlRegisterBody) -> WowCharacter:
        match = raiderio_regex.findall(register_body.raiderio_url)

        if not match:
            raise HTTPException(
                status_code=404,
                detail=f"Not a valid raiderio url")

        server = match[0][0]
        realm = match[0][1]
        char = match[0][2]

        character = await self.get_character(server, realm, char)
        
        charobj = RaiderIOResponse(**character)
        pool = await get_pool()

        try:
            async with pool.acquire() as connection:
                async with connection.transaction():
                    character_id, paymentcharacter = await connection.fetchval("""
                        WITH ensure_account AS (
                            INSERT INTO Accounts(account_id, account_name)
                            VALUES ($1, 'Nova balance account')
                            ON CONFLICT DO NOTHING
                        )
                        INSERT INTO WowCharacters(name, realm, faction, server, character_class, account_id, paymentcharacter)
                        VALUES ($2, $3, $4, $5, $6, $1,
                            CASE 
                                WHEN EXISTS (SELECT account_id FROM WowCharacters WHERE account_id = $1 and deleted = false) 
                                    THEN false
                                    ELSE true
                            END
                            )
                        ON CONFLICT DO NOTHING
                        RETURNING (character_id, paymentcharacter)
                    """, register_body.account_id, charobj.name, charobj.realm, charobj.faction, charobj.region, charobj.character_class)
                    return WowCharacter(
                        character_id=character_id,
                        name=charobj.name,
                        realm=charobj.realm,
                        faction=charobj.faction,
                        server=charobj.region,
                        character_class=charobj.character_class,
                        account_id=register_body.account_id,
                        paymentcharacter=paymentcharacter
                    )
        except ForeignKeyViolationError:
            raise HTTPException(status_code=404, detail=f"Account with ID {register_body.account_id} was not found")

    async def get_character(self, region: str, realm: str, name: str):
        """Retrieve a raider.io profile through their API"""
        url = (f"https://raider.io/api/v1/characters/profile"
            f"?region={region}"
            f"&realm={realm}"
            f"&name={name}"
            "&fields=mythic_plus_scores_by_season:current")

        async with aiohttp.ClientSession() as session:
            async with session.get(url) as response:
                character = await response.json()

        if character: 
            character["character_class"] = character.pop("class")

            if (scores := character.get("mythic_plus_scores_by_season")):
                for score in scores:
                    if (scores :=score.get("scores")):
                        scores["score_all"] = scores.pop("all")
        
        return character

    async def get_all_wow_characters(self):
        return await self.fetch("SELECT * FROM WowCharacters WHERE deleted = false")

    async def delete_wow_character(self, character_id: int):
        return await self.execute("UPDATE WowCharacters SET deleted=true WHERE character_id = $1", character_id)


    @staticmethod
    def get_character_score(character, tag="all") -> int:
        if character.get("mythic_plus_scores_by_season"):
            season1 = character["mythic_plus_scores_by_season"][0]
            # only 1 season atm, find correct season here.

            scores = season1["scores"]

            # Return given tag
            return scores.get(tag)

service = WowCharacterService()
