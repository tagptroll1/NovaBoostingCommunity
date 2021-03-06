import cookie from 'cookie';
import { v4 as uuid } from '@lukeed/uuid';
import type { Handle } from '@sveltejs/kit';
import Redis from "ioredis";
import env from "../env";

const redis = new Redis(env.redis_uri); 

export const handle: Handle = async ({ request, render }) => {
	const cookies = cookie.parse(request.headers.cookie || '');
	request.locals.userid = cookies.userid || uuid();

	// TODO https://github.com/sveltejs/kit/issues/1046
	if (request.query.has('_method')) {
		request.method = request.query.get('_method').toUpperCase();
	}
	
	const response = await render(request);
	
	if (!cookies.userid) {
		// if this is the first time the user has visited this app,
		// set a cookie so that we recognise them when they return
		response.headers['set-cookie'] = `userid=${request.locals.userid}; Path=/; HttpOnly`;
	}

	return response;
};

/** @type {import('@sveltejs/kit').GetSession} */
export async function getSession(request) {
	const loggedIn = !!await redis.get(request.locals?.userid);
	return {
		loggedIn
	};
}
