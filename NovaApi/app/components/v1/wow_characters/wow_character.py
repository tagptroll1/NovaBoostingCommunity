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

class WowCharacterRegisterBody(BaseModel):
    account_id: str
    region: str
    realm: str
    name: str

class WowCharacterUrlRegisterBody(BaseModel):
    account_id: str
    raiderio_url: str

class MythicPlussScore(BaseModel):
    score_all: float
    dps: float 
    healer: float
    tank: float
    spec_0: float
    spec_1: float
    spec_2: float
    spec_3: float

class MythicPlussScoreSeason(BaseModel):
    season: str
    scores: MythicPlussScore

class RaiderIOResponse(BaseModel):
    name: str
    race: str
    character_class: str
    active_spec_name: Optional[str]
    active_spec_role: Optional[str]
    gender: str
    faction: str
    achievement_points: int
    honorable_kills: int
    thumbnail_url: str
    region: str
    realm: str
    last_crawled_at: str
    profile_url: str
    profile_banner: str
    mythic_plus_scores_by_season: List[MythicPlussScoreSeason]

class ChangePaymentCharacterBody(BaseModel):
    account_id: str
    raiderio_url: Optional[str]
    name: Optional[str]
    realm: Optional[str]
    region: Optional[str]
    character_id: Optional[int]
