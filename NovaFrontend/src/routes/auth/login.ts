import type { Locals } from "$lib/types"
import type { RequestHandler } from "@sveltejs/kit"
import env from "../../../env";

export const get: RequestHandler<Locals> = async (request) => {
    const authorizeBase = env.discord_authorize_uri;
    const clientid = env.discord_client_id;
    return {
        status: 303,
        headers: {
            location: `${authorizeBase}?client_id=${clientid}&redirect_uri=${env.discord_redirect_uri}&response_type=code&scope=guilds%20identify`
        }
    }
}