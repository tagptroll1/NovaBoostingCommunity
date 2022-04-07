from app.components.v1.wow_characters import wow_character
from app.components.v1.wow_characters.wow_character import WowCharacter
from typing import List
from fastapi import APIRouter

from .transaction import Transaction, TransactionExpand
from .transactions_service import service

router = APIRouter()

# Route: /transactions
@router.post("", response_model=Transaction)
async def post_transaction(transaction: Transaction):
    transaction_id = await service.insert_transaction(transaction)
    transaction.transaction_id = transaction_id
    return transaction

@router.delete("/{transaction_id}")
async def delete_wow_character(transaction_id: int):
    await service.delete_transaction(transaction_id)

@router.get("", response_model=List[TransactionExpand])
async def get_all_transactions(account_id = None):
    # todo, implement filters
    rows = await service.get_all_transactions(account_id)
    returns = []

    for row in rows:
        character = WowCharacter(
            character_id=row["character_id"],
            name=row["name"],
            realm=row["realm"],
            faction=row["faction"],
            server=row["server"],
            character_class=row["character_class"],
            account_id=row["account_id"],
            paymentcharacter=row["paymentcharacter"]
        )
        returns.append(
            TransactionExpand(
                transaction_id=row["transaction_id"],
                wow_character=character,
                amount=row["amount"],
                comment=row["comment"],
                transaction_type=row["transaction_type"],
                created_at=row["created_at"],
                created_by=row["created_by"],
                updated_at=row["updated_at"],
                updated_by=row["updated_by"],
            )
        )

    return returns
        
    

