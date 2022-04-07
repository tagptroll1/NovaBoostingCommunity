

import aiohttp
import json
from starlette.requests import Request
from starlette.responses import Response

ADMIN_PERM = 0x0000000008
MANAGE_ROLE_PERM = 0x0010000000

roles = None
no_perms = json.dumps({"message": "No permissions"})

async def includes_api_key(request: Request, call_next, bot_token: str, server_id: int):
    if not request.url.path.startswith("/api"):
        return await call_next(request)

    auth = request.headers.get("Authorization")

    if not auth or not auth.startswith("Bearer"):
        return Response(no_perms, 401)

    split = auth.split()

    if len(split) != 2:
        return Response(no_perms, 401)

    meurl = "https://discord.com/api/v9/users/@me"

    headers = { "Authorization": auth }
    bot_headers = { "Authorization": f"Bot {bot_token}" }

    global roles

    async with aiohttp.ClientSession() as session:
        async with session.get(meurl, headers=headers) as response:
            me = await response.json()
            if "id" not in me:
                return Response(no_perms, 401)
            request.member = me

        memberurl = f"https://discord.com/api/v9/guilds/{server_id}/members/{me['id']}"
        async with session.get(memberurl, headers=bot_headers) as response:
            member = await response.json()
        
        if not roles:
            role_url = f"https://discord.com/api/v9/guilds/{server_id}/roles"
            async with session.get(role_url, headers=bot_headers) as response:
                roles = await response.json()

                for role in roles:
                    perm = int(role["permissions"])
                    role["manage_roles"] = (perm & MANAGE_ROLE_PERM) != 0
                    role["administrator"] = (perm & ADMIN_PERM) != 0

    request.roles = [role for role in roles if role["id"] in member["roles"]]

    if not any(role["administrator"] or role["manage_roles"] for role in request.roles):
        return Response(no_perms, 401)

    if call_next:
        return await call_next(request)