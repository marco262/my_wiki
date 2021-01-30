<!DOCTYPE html>
<head>
    <title>Tarokka Reading</title>
    <meta name="viewport" content="width=device-width">
    <link rel="stylesheet" type="text/css" href="/static/css/tarokka.css">
    <link rel="preload" href="/static/img/tileable-wood-texture.jpg" as="image">
    <link rel="preload" href="/static/img/tarokka/__Back.png" as="image">
    <link rel="preload" href="/static/audio/536784__egomassive__deal.ogg" as="audio">
    <link rel="preload" href="/static/audio/240776__f4ngy__card-flip.wav" as="audio">
</head>
<body style="background-image: url(/static/img/tileable-wood-texture.jpg)">
<%
# left = "Master of Glyphs - Priest"
# top = "8 of Coins - Tax Collector"
# right = "2 of Glyphs - Missionary"
# bottom = "High Deck - Mists"
# middle = "High Deck - Broken One"

middle = "7 of Glyphs - Charlatan"
middle_class = ""
bottom = "9 of Swords - Torturer"
bottom_class = ""
left = "High Deck - Mists"
left_class = ""
top = "9 of Glyphs - Traitor"
top_class = "inverted"
right = "4 of Glyphs - Shepherd"
right_class = "inverted"
%>

<div id='grid'>
    <article class="flip-card" id='top'>
        <div class="flip-card-inner off-grid" id="flip-card-inner-top">
            <div class="flip-card-back">
                <img class="card" src="/static/img/tarokka/__Back.png" alt="Back">
            </div>
            <div class="flip-card-front">
                <img id="card-img-top" class="card {{ top_class }}" src="/static/img/tarokka/{{ top }}.png" alt="Front">
            </div>
        </div>
    </article>
    <article class="flip-card" id='left'>
        <div class="flip-card-inner off-grid" id="flip-card-inner-left">
            <div class="flip-card-back">
                <img class="card" src="/static/img/tarokka/__Back.png" alt="Back">
            </div>
            <div class="flip-card-front">
                <img id="card-img-left" class="card {{ left_class }}" src="/static/img/tarokka/{{ left }}.png" alt="Front">
            </div>
        </div>
    </article>
    <article class="flip-card" id='middle'>
        <div class="flip-card-inner off-grid" id="flip-card-inner-middle">
            <div class="flip-card-back">
                <img class="card" src="/static/img/tarokka/__Back.png" alt="Back">
            </div>
            <div class="flip-card-front">
                <img id="card-img-middle" class="card {{ middle_class }}" src="/static/img/tarokka/{{ middle }}.png" alt="Front">
            </div>
        </div>
    </article>
    <article class="flip-card" id='right'>
        <div class="flip-card-inner off-grid" id="flip-card-inner-right">
            <div class="flip-card-back">
                <img class="card" src="/static/img/tarokka/__Back.png" alt="Back">
            </div>
            <div class="flip-card-front">
                <img id="card-img-right" class="card {{ right_class }}" src="/static/img/tarokka/{{ right }}.png" alt="Front">
            </div>
        </div>
    </article>
    <article class="flip-card" id='bottom'>
        <div class="flip-card-inner off-grid" id="flip-card-inner-bottom">
            <div class="flip-card-back">
                <img class="card" src="/static/img/tarokka/__Back.png" alt="Back">
            </div>
            <div class="flip-card-front">
                <img id="card-img-bottom" class="card {{ bottom_class }}" src="/static/img/tarokka/{{ bottom }}.png" alt="Front">
            </div>
        </div>
    </article>
</div>

<div id="audio-controls" hidden>
    <audio id="card-deal-effect" controls src="/static/audio/536784__egomassive__deal.ogg">
        Your browser does not support the audio element.
    </audio>
    <audio id="card-flip-effect" controls src="/static/audio/240776__f4ngy__card-flip.wav">
        Your browser does not support the audio element.
    </audio>
</div>

<div id="error-message" hidden></div>


<script type="module">
    import { init } from "/js/curse_of_strahd/tarokka.js";
    init();
</script>
</body>
