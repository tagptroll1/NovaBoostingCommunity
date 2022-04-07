from typing import List
from fastapi import APIRouter

from .wow_character import (
    ChangePaymentCharacterBody, WowCharacter,
    WowCharacterRegisterBody, WowCharacterUrlRegisterBody)
from .wow_characters_service import service

router = APIRouter()

# Route: /wowcharacter
@router.post("/register", response_model=WowCharacter)
async def register_wow_character(register_body: WowCharacterRegisterBody):
    urlBody = WowCharacterUrlRegisterBody(
        account_id=register_body.account_id,
        raiderio_url=(
            "https://raider.io/characters"
            f"/{register_body.region}"
            f"/{register_body.realm}"
            f"/{register_body.name}"
        )
    )
    return await service.register_wow_character(urlBody)

@router.get("", response_model=List[WowCharacter])
async def get_all_wow_characters():
    return await service.get_all_wow_characters()

@router.delete("/{character_id}")
async def delete_wow_character(character_id: int):
    await service.delete_wow_character(character_id)

@router.put("/paymentcharacter")
async def change_paymentcharacter(body: ChangePaymentCharacterBody):
    return await service.set_paymentcharacter(body)


@router.post("/registerurl", response_model=WowCharacter)
async def register_wow_character_by_url(register_body: WowCharacterUrlRegisterBody):
    return await service.register_wow_character(register_body)
