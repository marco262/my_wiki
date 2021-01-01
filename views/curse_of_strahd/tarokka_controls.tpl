<!DOCTYPE html>
<head>
    <title>Tarokka Reading</title>
    <meta name="viewport" content="width=device-width">
    <link rel="stylesheet" type="text/css" href="/static/css/tarokka.css">
    <link rel="stylesheet" type="text/css" href="/static/css/tarokka_controls.css">
    <link rel="preload" href="/static/img/tileable-wood-texture.jpg" as="image">
    <link rel="preload" href="/static/img/tarokka/__Back.png" as="image">
</head>
<body style="background-image: url(/static/img/tileable-wood-texture.jpg)">

<div id='grid'>
    <article class="flip-card" id='top'>
        <div class="flip-card-inner off-grid" id="flip-card-inner-top">
            <div class="flip-card-back">
                <img class="card" src="/static/img/tarokka/__Back.png" alt="Back">
            </div>
            <div class="flip-card-front">
                <img class="card" src="/static/img/tarokka/{{ top }}.png" alt="Front">
            </div>
        </div>
    </article>
    <article class="flip-card" id='left'>
        <div class="flip-card-inner off-grid" id="flip-card-inner-left">
            <div class="flip-card-back">
                <img class="card" src="/static/img/tarokka/__Back.png" alt="Back">
            </div>
            <div class="flip-card-front">
                <img class="card" src="/static/img/tarokka/{{ left }}.png" alt="Front">
            </div>
        </div>
    </article>
    <article class="flip-card" id='middle'>
        <div class="flip-card-inner off-grid" id="flip-card-inner-middle">
            <div class="flip-card-back">
                <img class="card" src="/static/img/tarokka/__Back.png" alt="Back">
            </div>
            <div class="flip-card-front">
                <img class="card" src="/static/img/tarokka/{{ middle }}.png" alt="Front">
            </div>
        </div>
    </article>
    <article class="flip-card" id='right'>
        <div class="flip-card-inner off-grid" id="flip-card-inner-right">
            <div class="flip-card-back">
                <img class="card" src="/static/img/tarokka/__Back.png" alt="Back">
            </div>
            <div class="flip-card-front">
                <img class="card" src="/static/img/tarokka/{{ right }}.png" alt="Front">
            </div>
        </div>
    </article>
    <article class="flip-card" id='bottom'>
        <div class="flip-card-inner off-grid" id="flip-card-inner-bottom">
            <div class="flip-card-back">
                <img class="card" src="/static/img/tarokka/__Back.png" alt="Back">
            </div>
            <div class="flip-card-front">
                <img class="card" src="/static/img/tarokka/{{ bottom }}.png" alt="Front">
            </div>
        </div>
    </article>
</div>

<script type="module">
    import { init } from "/js/curse_of_strahd/tarokka_controls.js";
    init();
</script>
</body>
