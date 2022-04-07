import type { Locals } from "$lib/types";
import type { RequestHandler } from "@sveltejs/kit";
import Redis from "ioredis";
import env from "../../../env";

export const get: RequestHandler<Locals> = async (request) => {
    const revokeuri = env.discord_revoke_uri;
    const client_id = env.discord_client_id;
    const client_secret = env.discord_client_secret;

    const redis = new Redis(env.redis_uri); 
    const token = redis.get(request.locals.userid);

    if (!token) {
        return {
            status: 303,
            headers: {
                location: "/"
            }
        }
    }

    try {
        await fetch(revokeuri, {
            headers: {
                Authorization: `Bearer ${token}`,
                Accept: "application/json",
                client_id,
                client_secret
            }
        })

        await redis.del(request.locals.userid);
    }
    catch (error) {
        console.log(error);
    }

    return {
        status: 303,
        headers: {
            location: `/`
        }
    }
}