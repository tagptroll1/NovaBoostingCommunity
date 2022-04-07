// Exposing node features to renderer goes here.
import { contextBridge, ipcRenderer } from "electron";

const validSendChannels = [
    "window::minimize",
    "window::close"
];

const validReceiveChannels = [];

contextBridge.exposeInMainWorld(
    "api", {
        send: (channel, data?) => {
            if (validSendChannels.includes(channel)) {
                ipcRenderer.send(channel, data);
            }
        },
        receive: (channel, func) => {
            if (validReceiveChannels.includes(channel)) {
                ipcRenderer.on(channel, (event, ...args) => func(...args));
            }
        },
        apiToken: process.env.apiToken,
    }
);
