import Redis from "ioredis";
import { NovaApi } from "$lib/api";
import type { Locals } from "$lib/types";
import type { RequestHandler } from "@sveltejs/kit";
import env from "../../../env";
import {v4 as uuid} from "@lukeed/uuid";

const api = new NovaApi();
const redis = new Redis(env.redis_uri);

export const get: RequestHandler<Locals> = async (request) => {
    request.locals.userid = request.locals?.userid || uuid();

    const token = await redis.get(request.locals?.userid);
    console.log({token});    
    if (!token) {
        return {
            status: 401,
            body: "Not logged in"
        }
    }

    const accounts = await api.get("accounts?include_balance=true&include_wowcharacters=true", token);
    return {
        body: accounts
    }
}
