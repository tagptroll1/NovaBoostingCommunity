from typing import List
from fastapi import APIRouter

from .account import Account
from .accounts_service import service

router = APIRouter()

# Route: /accounts
@router.post("", response_model=Account)
async def get_raiderio_profile(account: Account):
    await service.insert_account(account)
    return account

@router.get("", response_model=List[Account])
async def get_all_accounts(include_balance: bool = False, include_wowcharacters: bool = False):
    if include_balance and include_wowcharacters:
        return await service.get_all_accounts_with_wowcharacters_and_balance()
    elif include_balance:
        return await service.get_all_accounts_with_balance()
    elif include_wowcharacters:
        return await service.get_all_accounts_with_wowcharacters()
    return await service.get_all_accounts()

@router.get("/{account_id}/balance")
async def get_account_balance(account_id: str):
    balance = await service.get_account_balance(account_id)
    return { "amount": balance or 0 }
