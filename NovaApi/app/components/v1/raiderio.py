# from fastapi import APIRouter, Depends
# from api import deps

# router = APIRouter()


# @router.get("/{region}/{realm}/{character}") #, response_model=schemas.RaiderIOProfile)
# async def get_raiderio_profile(
#     region: str,
#     realm: str,
#     character: str,
#     db = Depends(deps.get_db)):
#     return ""