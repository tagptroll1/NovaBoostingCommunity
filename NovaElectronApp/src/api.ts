
declare global {
    interface Window {
        api: {
            send: (string, any?) => void,
            receive: (string, any?) => void,
            apiToken: string,
        }
    }
}

export const api = window.api;

export class NovaApi {
    private baseUrl: string;

    constructor(baseUrl?: string) {
        this.baseUrl = baseUrl ?? "http://127.0.0.1:8000/api/v1/";
        if (!this.baseUrl.endsWith("/")) {
            this.baseUrl += "/";
        }
    }

    public async get(endpoint: string, headers?: HeadersInit) {
        if (endpoint.startsWith("/")) {
            endpoint = endpoint.slice(1);
        }
        const url = this.baseUrl + endpoint;

        if (!headers) {
            headers = {};
        }
        if (!headers["Authorization"]) {
            headers["Authorization"] = `Bearer ${api.apiToken}`
        }
        const resp = await fetch(url, {
            headers,
            method: "GET",
        });

        return await resp.json();
    }
}