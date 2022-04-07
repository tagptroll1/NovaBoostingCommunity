from datetime import datetime
from typing import List, Optional
from pydantic import BaseModel


class WowCharacter(BaseModel):
    character_id: Optional[int]
    name: str
    realm: str
    faction: str
    server: str
    character_class: str
    account_id: str
    paymentcharacter: bool
    created_by: Optional[str]
    updated_by: Optional[str]
    created_at: Optional[datetime]
    updated_at: Optional[datetime]
    deleted: bool = False


class Account(BaseModel):
    account_id: str
    account_name: str
    balance: Optional[str]
    wow_characters: Optional[List[WowCharacter]]
    created_by: Optional[str]
    updated_by: Optional[str]
    created_at: Optional[datetime]
    updated_at: Optional[datetime]
    deleted: bool = False
