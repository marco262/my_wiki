<!DOCTYPE html>
<head>
    <title>Tarokka Reading</title>
    <meta name="viewport" content="width=device-width">
    <link rel="stylesheet" type="text/css" href="/static/css/tarokka.css">
    <link rel="preload" href="/static/img/wooden_table_background.jpeg" as="image">
    <link rel="preload" href="/static/img/tarokka/__Back.png" as="image">
</head>
<body>
<%
left = "Master of Glyphs - Priest"
top = "8 of Coins - Tax Collector"
right = "3 of Glyphs - Healer"
bottom = "High Deck - Mists"
middle = "High Deck - Broken One"
%>

<div id="slide-off-button">Deal/Undeal Cards</div>

<div id='grid'>
    <article id='top'>
        <div class="flip-card">
            <div class="flip-card-inner">
                <div class="flip-card-back">
                    <img class="card" src="/static/img/tarokka/__Back.png" alt="Back">
                </div>
                <div class="flip-card-front">
                    <img class="card" src="/static/img/tarokka/{{ top }}.png" alt="Front">
                </div>
            </div>
      </div>
    </article>
    <article id='left'>
        <div class="flip-card">
            <div class="flip-card-inner">
                <div class="flip-card-back">
                    <img class="card" src="/static/img/tarokka/__Back.png" alt="Back">
                </div>
                <div class="flip-card-front">
                    <img class="card" src="/static/img/tarokka/{{ left }}.png" alt="Front">
                </div>
            </div>
        </div>
    </article>
    <article id='middle'>
        <div class="flip-card">
            <div class="flip-card-inner">
                <div class="flip-card-back">
                    <img class="card" src="/static/img/tarokka/__Back.png" alt="Back">
                </div>
                <div class="flip-card-front">
                    <img class="card" src="/static/img/tarokka/{{ middle }}.png" alt="Front">
                </div>
            </div>
        </div>
    </article>
    <article id='right'>
        <div class="flip-card">
            <div class="flip-card-inner">
                <div class="flip-card-back">
                    <img class="card" src="/static/img/tarokka/__Back.png" alt="Back">
                </div>
                <div class="flip-card-front">
                    <img class="card" src="/static/img/tarokka/{{ right }}.png" alt="Front">
                </div>
            </div>
        </div>
    </article>
    <article id='bottom'>
        <div class="flip-card">
            <div class="flip-card-inner">
                <div class="flip-card-back">
                    <img class="card" src="/static/img/tarokka/__Back.png" alt="Back">
                </div>
                <div class="flip-card-front">
                    <img class="card" src="/static/img/tarokka/{{ bottom }}.png" alt="Front">
                </div>
            </div>
        </div>
    </article>
</div>




<script type="module">
    import { init } from "/js/curse_of_strahd/tarokka.js";
    init();
</script>
</body>