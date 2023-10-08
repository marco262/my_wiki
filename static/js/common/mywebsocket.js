export class MyWebsocket {
    constructor(websocket_uri, handle_websocket, max_websocket_errors=3) {
        this.websocket_uri = websocket_uri;
        this.handle_websocket = handle_websocket;
        this.ws = null;
        this.websocket_errors = 0;
        this.max_websocket_errors = max_websocket_errors;
    }

    load() {
        this.load_websocket(this);
    }

    load_websocket(obj) {
        let loc = window.location;
        let ws_uri = (loc.protocol === "https:") ? "wss:" : "ws:";
        ws_uri += `//${loc.host}${obj.websocket_uri}`;
        obj.ws = new WebSocket(ws_uri);
        obj.set_hooks(obj);
        console.log(`Loaded websocket: ${ws_uri}`);
    }

    set_hooks(obj) {
        obj.ws.onopen = () => {
            // Set onclose hook only after the websocket has successfully been opened
            obj.ws.onclose = () => obj.on_websocket_close(obj);
            obj.websocket_errors = 0;
        }
        obj.ws.onmessage = (msg) => {
            let error_msg = document.getElementById("error-message");
            if (error_msg !== null)
                error_msg.hidden = true;
            obj.websocket_errors = 0;
            obj.handle_websocket(msg);
        };
        obj.ws.onerror = (error) => obj.on_websocket_error(obj, error);
    }

    on_websocket_error(obj, error) {
        console.error("WebSocket error:");
        console.error(error);
        obj.quiet_close(obj.ws);
        obj.websocket_errors += 1;
        if (obj.websocket_errors > obj.max_websocket_errors) {
            let error_msg = document.getElementById("error-message");
            if (error_msg !== null) {
                error_msg.innerText = `Failed to reconnect to WebSocket after ${obj.max_websocket_errors} attempts. ` +
                    `Please reload page to try again.`;
                error_msg.hidden = false;
            }
            return;
        }
        let reconnect_timer = obj.websocket_errors < 2 ? 0 : 5000;
        console.log(`Reconnecting in ${reconnect_timer} ms...`);
        // Try to reconnect immediately if it's
        setTimeout(obj.load_websocket, reconnect_timer, obj);
    }

    on_websocket_close(obj) {
        obj.on_websocket_error(obj, "Websocket closed");
    }

    quiet_close(ws) {
        // If the websocket errored out but is still open, close it first before continuing
        if (ws !== null && ws.readyState < ws.CLOSING) {
            ws.onclose = null;
            ws.close();
        }
    }

    close() {
        this.ws.onclose = null;
        this.ws.close();
    }
}