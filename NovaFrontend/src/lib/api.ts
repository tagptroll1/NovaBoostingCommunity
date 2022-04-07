import env from "../../env";

class NovaApi {
    private baseUri: string;

    constructor(baseUri?: string) {
        if (!baseUri) {
            this.baseUri = env.nova_baseuri;
        } else {
            this.baseUri = baseUri;
        }
    }

    public async send(method: string, route: string, token?: string, body?: BodyInit) {
        const uri = this.baseUri + route
        try {
            const requestInit: RequestInit = {
				method,
				headers: {
					accept: 'application/json',
				}
			};

            if (body) {
                requestInit.body = body;
                requestInit.headers["Content-Type"] = "application/json";
            }

            if (token) 
            {
                requestInit.headers["Authorization"] = `Bearer ${token}`; 
            }

			const res = await fetch(uri, requestInit);

			if (res.ok) {
				return await res.json();
			} else {
				console.error(await res.text());
			}
		} catch (e) {
            console.error(e);
            throw e;
		}
    }

    public async get(route: string, token?: string) {
        return await this.send("GET", route, token);
    }

    public async post(route: string, body: BodyInit, token?: string) {
        return await this.send("POST", route, token, body);
    }

    public async put(route: string, body: BodyInit, token?: string) {
        return await this.send("PUT", route, token, body);
    }

    public async del(route: string, token?: string) {
        return await this.send("DELETE", route, token);
    }
}


export { NovaApi }