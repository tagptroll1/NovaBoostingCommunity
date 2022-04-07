
import type { RequestHandler } from '@sveltejs/kit';
import type { Locals } from '$lib/types';
import env from "../../../env";
import Redis from "ioredis";


export const get: RequestHandler<Locals> = async (request) => {
    const code = request.query.get("code");
	const exchangeOptions = new URLSearchParams();
	exchangeOptions.append("grant_type", "authorization_code");
	exchangeOptions.append("client_id", env.discord_client_id);
	exchangeOptions.append("client_secret", env.discord_client_secret);
	exchangeOptions.append("code", code);
	exchangeOptions.append("redirect_uri", env.discord_redirect_uri);

	const options = {
	  method: "POST",
	  body: exchangeOptions,
	  headers: {
		"content-type": "application/x-www-form-urlencoded",
	  },
	};
  
	try {
	  const response = await fetch(env.discord_auth_token_uri, options);
	  const json = await response.json();
	  console.log(json)
	  const accessToken = json.access_token;
	  const refreshToken = json.refresh_token;
	  const redis = new Redis(env.redis_uri); 
	  await redis.set(request.locals.userid, accessToken);
	}
	catch (err) {
		console.error("bigerr" + err.toString());
		return {
			status: 401,
			body: err
		}
	}

	return {
		status: 303,
		headers: {
			location: "/"
		}
	};
};