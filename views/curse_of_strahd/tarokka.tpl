<!DOCTYPE html>
<head>
    <title>Tarokka Reading</title>
    <meta name="viewport" content="width=device-width">
    <link rel="preload" href="/static/css/tarokka.css" as="style">
    <link rel="stylesheet" type="text/css" href="/static/css/tarokka.css">
    <link rel="prefetch" href="/media/img/tarokka/__Back.png" as="image">
    <link rel="preload" href="/media/img/tileable-wood-texture.jpg" as="image">
    <link rel="preload" href="/media/audio/536784__egomassive__deal.ogg" as="audio">
    <link rel="preload" href="/media/audio/240776__f4ngy__card-flip.wav" as="audio">
</head>
<body style="background-image: url(/media/img/tileable-wood-texture.jpg)">

<div id="container">
    <div id="grid">
        <article class="flip-card" id="top">
            <div class="flip-card-inner off-grid" id="flip-card-inner-top">
                <div class="flip-card-back">
                    4
                </div>
                <div class="flip-card-front">
                    <img id="card-img-top" class="card card-front" src="/media/img/tarokka/High Deck - Mists.png" alt="Front">
                </div>
            </div>
        </article>
        <article class="flip-card" id="left">
            <div class="flip-card-inner off-grid" id="flip-card-inner-left">
                <div class="flip-card-back">
                    3
                </div>
                <div class="flip-card-front">
                    <img id="card-img-left" class="card card-front" src="/media/img/tarokka/High Deck - Mists.png" alt="Front">
                </div>
            </div>
        </article>
        <article class="flip-card" id="middle">
            <div class="flip-card-inner off-grid" id="flip-card-inner-middle">
                <div class="flip-card-back">
                    1
                </div>
                <div class="flip-card-front">
                    <img id="card-img-middle" class="card card-front" src="/media/img/tarokka/High Deck - Mists.png" alt="Front">
                </div>
            </div>
        </article>
        <article class="flip-card" id="right">
            <div class="flip-card-inner off-grid" id="flip-card-inner-right">
                <div class="flip-card-back">
                    5
                </div>
                <div class="flip-card-front">
                    <img id="card-img-right" class="card card-front" src="/media/img/tarokka/High Deck - Mists.png" alt="Front">
                </div>
            </div>
        </article>
        <article class="flip-card" id="bottom">
            <div class="flip-card-inner off-grid" id="flip-card-inner-bottom">
                <div class="flip-card-back">
                    2
                </div>
                <div class="flip-card-front">
                    <img id="card-img-bottom" class="card card-front" src="/media/img/tarokka/High Deck - Mists.png" alt="Front">
                </div>
            </div>
        </article>
    </div>
    <div id="info-box">
        <div id="card-info">
            <p><strong>Prophecy:</strong> <span id="prophecy_summary"></span></p>
            <p><strong>Vibe Check:</strong> <span id="vibe_check_summary"></span></p>
            <hr>
            <h1 id="card-name"></h1>
            <p id="card-description"></p>
            <p id="suit-description"></p>
        </div>
        <p><a href="tarokka_card_list">Tarokka Card List</a></p>
        <p><a href="Tarokka Reading Rules">Tarokka Reading Rules</a></p>
    </div>
</div>

<div id="audio-controls" hidden>
    <audio id="card-deal-effect" controls src="/media/audio/536784__egomassive__deal.ogg">
        Your browser does not support the audio element.
    </audio>
    <audio id="card-flip-effect" controls src="/media/audio/240776__f4ngy__card-flip.wav">
        Your browser does not support the audio element.
    </audio>
</div>

<div id="error-message" hidden></div>


<script type="module">
    import { init } from "/static/js/curse_of_strahd/tarokka.js";
    window.onload = init;
</script>
</body>
