let websocket_errors = 0;
let max_websocket_errors = 3;
let ws = null;

let all_audio = [];
let music_audio = [];
let music_counter = 0;
let ambience_audio = [];
let ambience_counter = 0;
let effect_audio = [];
let effect_counter = 0;

export function init() {
    music_audio = document.getElementsByClassName("music");
    ambience_audio = document.getElementsByClassName("ambience");
    effect_audio = document.getElementsByClassName("effect");
    all_audio = music_audio + ambience_audio + effect_audio;

    load_websocket();

    window.addEventListener("beforeunload", event => {
        console.log("Closing websocket");
        ws.close();
    });

    document.getElementById("picture").ondblclick = toggle_audio_controls;

    // Check if autoplay is allowed by playing empty wav file
    let silent_wav = "data:audio/wav;base64,UklGRiQAAABXQVZFZm10IBAAAAABAAEARKwAAIhYAQACABAAZGF0YQAAAAA=";
    var snd = new Audio(silent_wav);
    snd.play();
    check_for_popup(snd);
}

function load_websocket() {
    let loc = window.location;
    let ws_uri = (loc.protocol === "https:") ? "wss:" : "ws:";
    ws_uri += `//${loc.host}/dragon_heist/visual_aid_websocket`;
    ws = new WebSocket(ws_uri);
    ws.onmessage = handle_websocket;
    ws.onerror = on_websocket_error;
    console.log(`Loaded websocket`)
}

function on_websocket_error(error) {
    console.log("WebSocket error:");
    console.log(error);
    websocket_errors += 1;
    if (websocket_errors >= max_websocket_errors) {
        document.getElementById("page").hidden = true;
        let error_msg = document.getElementById("error-message");
        error_msg.innerText = `Failed to connect to WebSocket after ${websocket_errors} attempts. ` +
            `Please reload page to try again.`;
        error_msg.hidden = false;
        return;
    }
    console.log("Reconnecting in 5 seconds...");
    setTimeout(load_websocket, 5000);
}

function toggle_audio_controls(e) {
    let audio_controls = document.getElementById("audio-controls");
    audio_controls.hidden = !audio_controls.hidden;
}

function handle_websocket(msg) {
    websocket_errors = 0;
    console.log(msg);
    let response = msg.data;
    console.log(response);
    let json = JSON.parse(response);
    if (json["target"] === "visual_aid") {
        handle_visual_aid(json["url"]);
    } else {
        handle_audio(json["action"], json["target"], json["url"]);
    }
}

function handle_visual_aid(url) {
    console.log("Setting img src: " + url);
    document.getElementById("picture").style.backgroundImage = "url('" + url + "')";
}

function handle_audio(action, target, url) {
    /*
        action: load, play, pause, stop
        target: music, ambience, effect, all
        url: <music URL, only needed for load>
     */
    console.log(`Action: ${action}, target: ${target}, url: ${url}`);
    if (action === "load") {
        load_audio(target, url);
    } else {
        let elements = [];
        if (target === "all") {
            elements = all_audio;
        } else if (target === "music") {
            elements = music_audio;
        } else if (target === "ambience") {
            elements = ambience_audio;
        } else if (target === "effect") {
            elements = effect_audio;
        } else {
            console.error(`No audio class "${target}"`);
            return;
        }
        console.log(elements);
        elements.forEach(e => {
            if (action === "play") {
                e.play();
            } else if (action === "pause") {
                e.pause();
            } else if (action === "stop") {
                e.pause();
                e.current_time = 0;
            }
        })
    }
}

function load_audio(target, url) {
    console.log(`Load URL ${url} into element ${target}`);
    let element;
    if (target === "music") {
        element = music_audio[music_counter];
        music_counter = (music_counter + 1) % music_audio.length;
    } else if (target === "ambience") {
        element = ambience_audio[ambience_counter];
        ambience_counter = (ambience_counter + 1) % ambience_audio.length;
    } else if (target === "effect") {
        element = effect_audio[effect_counter];
        effect_counter = (effect_counter + 1) % effect_audio.length;
    } else {
        console.error(`No audio class "${target}" for "load" action`);
        return;
    }
    element.src = url;
    element.load();
    element.play();
    check_for_popup(element);
}

function check_for_popup(snd) {
    let failed_to_play = snd.paused;
    console.log(`Failed to play: ${failed_to_play}`);
    if (failed_to_play) {
        if (navigator.userAgent.indexOf("Firefox") !== -1) {
            document.getElementById("browser-specific-instructions").innerText =
                `please set the Autoplay permission for this page to "Allow Audio and Video".`;
        }
        let popup = document.getElementById("notification-popup");
        popup.onclick = function () { popup.style.top = null; }
        popup.style.top = "0px";
        console.log("User-agent header sent: " + navigator.userAgent);
    }
}