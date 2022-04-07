from fastapi import APIRouter

from .transactions import transactions_api
from .accounts import accounts_api
from .wow_characters import wow_characters_api

api_router = APIRouter(prefix="/v1")
api_router.include_router(transactions_api.router, prefix="/transactions", tags=["transactions"])
api_router.include_router(accounts_api.router, prefix="/accounts", tags=["accounts"])
api_router.include_router(wow_characters_api.router, prefix="/wowcharacter", tags=["wowcharacter"])

__slots__ = (api_router,)