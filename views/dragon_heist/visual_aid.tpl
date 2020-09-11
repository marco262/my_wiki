<head>
    <title>Visual Aid</title>
    <link rel="stylesheet" type="text/css" href="/static/css/visual_aid.css">
</head>
<body style="background-color: white;">
    <div id="notification-popup">
        <div id="arrow"></div>
        <div id="box">
            <p><strong>Sounds may not play properly on this page.</strong></p>
            <p>To allow sounds to play, <span id="browser-specific-instructions">please go into the settings for this page and allow Sound/Audio.</span></p>
            <p><em>Click to close</em></p>
        </div>
    </div>
    <div id="page">
        <div id="picture" style="background-size: contain; width: 100%; height: 100%; background-repeat: no-repeat; background-position: center;"></div>
        <iframe id="iframe" src="" height="100%" width="100%" hidden></iframe>
        <div id="audio-controls" hidden>
            <p><em>Double-click picture to hide controls</em></p>
            <p>Music</p>
            <audio class="music" id="music" autoplay controls loop>
                Your browser does not support the audio element.
            </audio>
            <p>Ambience</p>
            <audio class="ambience" id="ambience-1" autoplay controls loop>
                Your browser does not support the audio element.
            </audio>
            <audio class="ambience" id="ambience-2" autoplay controls loop>
                Your browser does not support the audio element.o
            </audio>
            <audio class="ambience" id="ambience-3" autoplay controls loop>
                Your browser does not support the audio element.
            </audio>
            <audio class="ambience" id="ambience-4" autoplay controls loop>
                Your browser does not support the audio element.
            </audio>
            <audio class="ambience" id="ambience-5" autoplay controls loop>
                Your browser does not support the audio element.
            </audio>
            <p>Effects</p>
            <audio class="effect" id="effect-1" autoplay controls>
                Your browser does not support the audio element.
            </audio>
            <audio class="effect" id="effect-2" autoplay controls>
                Your browser does not support the audio element.
            </audio>
            <audio class="effect" id="effect-3" autoplay controls>
                Your browser does not support the audio element.
            </audio>
            <p>Youtube Player</p>
            <p><iframe id="youtube-player"
                    width="640" height="360"
                    src="https://www.youtube.com/embed/M7lc1UVf-VE?enablejsapi=1"
                    frameborder="0"
                    style="border: solid 4px #37474F"
            ></iframe></p>
        </div>
    </div>
    <div id="error-message" hidden></div>
</body>

<script id="youtube-script" src="/js/dragon_heist/youtube.js"></script>
<script type="module">
    import { init } from "/js/dragon_heist/visual_aid.js";
    init();
</script>
