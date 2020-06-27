let tag = document.createElement('script');
tag.id = 'iframe-demo';
tag.src = 'https://www.youtube.com/iframe_api';
let firstScriptTag = document.getElementsByTagName('script')[0];
firstScriptTag.parentNode.insertBefore(tag, firstScriptTag);

let youtube_player;
let youtube_player_loaded = false;

function onYouTubeIframeAPIReady() {
    youtube_player = new YT.Player('youtube-player', {
        events: {
            'onReady': onPlayerReady,
            'onStateChange': onPlayerStateChange
        }
    });
}

function onPlayerReady(event) {
    document.getElementById('youtube-player').style.borderColor = '#FF6D00';
    youtube_player_loaded = true;
}

function changeBorderColor(playerStatus) {
    let color;
    if (playerStatus === -1) {
        color = "#37474F"; // unstarted = gray
    } else if (playerStatus === 0) {
        color = "#FFFF00"; // ended = yellow
    } else if (playerStatus === 1) {
        color = "#33691E"; // playing = green
    } else if (playerStatus === 2) {
        color = "#DD2C00"; // paused = red
    } else if (playerStatus === 3) {
        color = "#AA00FF"; // buffering = purple
    } else if (playerStatus === 5) {
        color = "#FF6DOO"; // video cued = orange
    }
    if (color) {
        document.getElementById('youtube-player').style.borderColor = color;
    }
}

function onPlayerStateChange(event) {
    changeBorderColor(event.data);
}