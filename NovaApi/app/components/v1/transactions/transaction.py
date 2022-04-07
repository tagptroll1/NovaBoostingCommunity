from app.components.v1.wow_characters.wow_character import WowCharacter
from typing import Optional
from pydantic import BaseModel
from datetime import datetime


# make type an enum
class Transaction(BaseModel):
    transaction_id: Optional[int]
    account_id: str
    amount: int
    comment: Optional[str]
    transaction_type: str
    created_by: Optional[str]
    updated_by: Optional[str]
    created_at: Optional[datetime]
    updated_at: Optional[datetime]
    deleted: bool = False

class TransactionExpand(BaseModel):
    transaction_id: Optional[int]
    wow_character: WowCharacter
    amount: int
    comment: Optional[str]
    transaction_type: str
    created_by: Optional[str]
    updated_by: Optional[str]
    created_at: Optional[datetime]
    updated_at: Optional[datetime]