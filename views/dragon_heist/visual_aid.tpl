<body style="background-color: white;">
    <div id="page">
        <div id="picture" style="background-size: contain; width: 100%; height: 100%; background-repeat: no-repeat; background-position: center;"></div>
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
                Your browser does not support the audio element.
            </audio>
            <audio class="ambience" id="ambience-3" autoplay controls loop>
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
        </div>
    </div>
    <div id="error-message" hidden></div>
</body>
<script type="module">
    import {init} from "/js/dragon_heist/visual_aid.js";
    init();
</script>
