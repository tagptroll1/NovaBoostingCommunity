
from app.components.v1.auth.auth_middleware import includes_api_key
from fastapi import FastAPI
from fastapi.responses import Response
from starlette.requests import Request

from .config import settings
from .db.init_db import get_pool
from .events import setup_events
from .components.v1.api import api_router

app = FastAPI()

# from fastapi.middleware.httpsredirect import HTTPSRedirectMiddleware
# app.add_middleware(HTTPSRedirectMiddleware)

setup_events(app)
app.include_router(api_router, prefix="/api")


@app.middleware("http")
async def callMiddleware(request: Request, call_next):
    return await includes_api_key(request, call_next, settings.BOT_TOKEN, settings.SERVER_ID)


@app.get("/api")
async def read_root():
    is_alive = False
    # try:
    pool = await get_pool()

    async with pool.acquire() as connection:
        async with connection.transaction():
            result = await connection.fetchval("select 1")
        is_alive = result == 1
    # except Exception as exception:
        # print("failed to use database", exception)

    return Response(f"I'm alive\n Database: {'ok' if is_alive else ''}")


# @app.get("/items/{item_id}")
# def read_item(item_id: int, q: Optional[str] = None):
#     return {"item_id": item_id, "q": q}