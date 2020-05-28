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
    let visual_aid_buttons = document.getElementsByClassName("visual-aid-button");
    visual_aid_buttons.forEach( function (button) {
        button.onclick = function () { set_visual_aid(button.name); };
    })
    let audio_buttons = document.getElementsByClassName("audio-button");
    audio_buttons.forEach( function (button) {
        button.onclick = function () { set_audio(button.name); };
    })
}

function set_visual_aid(name) {
    var xhr = new XMLHttpRequest();
    xhr.open("POST", yourUrl, true);
    xhr.setRequestHeader('Content-Type', 'application/json');
    xhr.send(JSON.stringify({
        value: value
    }));
}
