import {MyWebsocket} from "./mywebsocket.js";

let ws = null;
let visual_aid_version = null;

let all_audio = [];
let music_audio = [];
let music_counter = 0;
let ambience_audio = [];
let ambience_counter = 0;
let effect_audio = [];
let effect_counter = 0;

export function init(volume_settings) {
    music_audio = Array.from(document.getElementsByClassName("music"));
    ambience_audio = Array.from(document.getElementsByClassName("ambience"));
    effect_audio = Array.from(document.getElementsByClassName("effect"));
    all_audio = music_audio.concat(ambience_audio).concat(effect_audio);

    set_volumes(volume_settings);

    ws = new MyWebsocket("/visual_aid_websocket", handle_websocket);
    ws.load();

    window.addEventListener("beforeunload", event => {
        console.log("Closing websocket");
        ws.close();
    });

    document.getElementById("picture").ondblclick = toggle_audio_controls;

    // Check if autoplay is allowed by playing empty wav file
    window.onload = play_sound;
}

function toggle_audio_controls(e) {
    let audio_controls = document.getElementById("audio-controls");
    audio_controls.hidden = !audio_controls.hidden;
}

function handle_websocket(msg) {
    console.log(msg);
    let response = msg.data;
    console.log(response);
    let json = JSON.parse(response);
    // Check if we need to reload the page
    if (visual_aid_version === null) {
        visual_aid_version = json["version"];
        console.log(`Visual aid version ${visual_aid_version}`);
    } else if (visual_aid_version !== json["version"]) {
        console.log(`Current visual aid version (${visual_aid_version}) doesn't match value returned by server (${json["version"]}). Refreshing page...`);
        force_page_refresh();
        return;
    }
    // Handle remaining data
    if (json["action"] === "visual_aid") {
        handle_visual_aid(json["url"], json["title"]);
    } else if (json["action"] === "iframe") {
        handle_iframe(json["url"]);
    } else if (json["action"] === "volume") {
        set_volumes(json["settings"]);
    } else {
        handle_audio(json["action"], json["target"], json["url"]);
    }
}

function force_page_refresh() {
    location.reload(true);
}

function handle_visual_aid(url, title) {
    console.log("Setting img src: " + url);
    document.getElementById("iframe").hidden = true;
    let picture = document.getElementById("picture");
    let video = document.getElementById("video");
    if (url.endsWith(".mp4")) {
        picture.hidden = true;
        video.hidden = false;
        video.src = url;
        video.play();
    } else {
        video.hidden = true;
        video.pause();
        picture.style.backgroundImage = "url('" + url + "')";
        picture.hidden = false;
    }
    let picture_title = document.getElementById("picture-title");
    picture_title.innerHTML = decodeURIComponent(title);
    picture_title.hidden = false;
}

function handle_audio(action, target, url) {
    /*
        action: `load`, `play`, `pause`, `stop`, or `volume`
        target: `music`, `ambience`, `effect`, `youtube`, or `all`
        url: Audio URL (needed for `load`)
     */
    console.log(`Action: ${action}, target: ${target}, url: ${url}`);
    if (target === "youtube") {
        youtube_control(action, url);
        return;
    }
    if (action === "load") {
        load_audio(target, url);
    } else {
        let elements = [];
        if (target === "all") {
            elements = all_audio;
            youtube_control(action, url);
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
        for (let e of elements) {
            console.log(e);
            if (action === "play") {
                e.play();
            } else if (action === "pause") {
                e.pause();
            } else if (action === "stop") {
                e.pause();
                e.currentTime = 0;
                e.src = "";
            }
        }
    }
}

function handle_iframe(url) {
    console.log(`Loading ${url} in iframe`);
    document.getElementById("picture").hidden = true;
    let video = document.getElementById("video");
    video.hidden = true;
    video.pause();
    document.getElementById("picture-title").hidden = true;
    let iframe = document.getElementById("iframe");
    iframe.hidden = false;
    // Set onload so that once it's loaded, it goes to the right hash
    iframe.onload = () => {
        console.log(`My hash: ${iframe.contentWindow.location.hash}`);
    }
    iframe.src = url;
}

function load_audio(target, url) {
    console.log(`Loading URL ${url} into element ${target}...`);
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

function play_sound() {
    let silent_wav = "data:audio/wav;base64,UklGRiQAAABXQVZFZm10IBAAAAABAAEARKwAAIhYAQACABAAZGF0YQAAAAA=";
    let snd = new Audio(silent_wav);
    snd.play();
    setTimeout(() => { check_for_popup(snd); }, 500);
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

function youtube_control(action, url=null) {
    if (!youtube_player_loaded) {
        console.log("Youtube player is not initialized yet. Stopping early.");
        return;
    }
    if (action === "play") {
        youtube_player.playVideo();
    } else if (action === "pause") {
        youtube_player.pauseVideo();
    } else if (action === "stop") {
        youtube_player.stopVideo();
    } else if (action === "load") {
        let id = get_youtube_id(url);
        console.log(id);
        youtube_player.loadVideoById(id);
        youtube_player.seekTo(0);
    }
}

function get_youtube_id(url) {
    let m = url.match(/watch\?(.*)/);
    if (m && m.length > 1) {
        let params = m[1].split("&");
        for (let i in params) {
            console.log(params[i]);
            if (params[i].startsWith("v=")) {
                return params[i].substring(2);
            }
        }
    }
    m = url.match(/youtu.be\/(.*?)(\?.*)?$/);
    if (m && m.length > 1) {
        return m[1];
    }
    return url;
}


function set_volumes(volume_settings) {
    console.log(volume_settings);
    for (const [target, value] of Object.entries(volume_settings)) {
        if (target === 'music') {
            for (let e of music_audio) {
                e.volume = value;
            }
        } else if (target === 'ambience') {
            for (let e of ambience_audio) {
                e.volume = value;
            }
        } else if (target === 'effect') {
            for (let e of effect_audio) {
                e.volume = value;
            }
        } else {
            console.error(`Unknown key: ${target}`);
        }
    }
}
