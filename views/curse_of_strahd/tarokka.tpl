<link rel="stylesheet" type="text/css" href="/static/css/tarokka.css">
<link rel="preload" href="/static/img/tarokka/__Back.png" as="image">

<%
tome = "Master of Glyphs - Priest"
symbol = "8 of Coins - Tax Collector"
sword = "3 of Glyphs - Healer"
ally = "High Deck - Mists"
devil = "High Deck - Broken One"
%>

<table>
    <tr>
        <td></td>
        <td>
            <div class="flip-card">
                <div class="flip-card-inner">
                    <div class="flip-card-back">
                        <img class="card" src="/static/img/tarokka/__Back.png" alt="Back">
                    </div>
                    <div class="flip-card-front">
                        <img class="card" src="/static/img/tarokka/{{ symbol }}.png" alt="Front">
                    </div>
                </div>
            </div>
        </td>
        <td></td>
    </tr>
    <tr>
        <td>
            <div class="flip-card">
                <div class="flip-card-inner">
                    <div class="flip-card-back">
                        <img class="card" src="/static/img/tarokka/__Back.png" alt="Back">
                    </div>
                    <div class="flip-card-front">
                        <img class="card" src="/static/img/tarokka/{{ tome }}.png" alt="Front">
                    </div>
                </div>
            </div>
        </td>
        <td>
            <div class="flip-card">
                <div class="flip-card-inner">
                    <div class="flip-card-back">
                        <img class="card" src="/static/img/tarokka/__Back.png" alt="Back">
                    </div>
                    <div class="flip-card-front">
                        <img class="card" src="/static/img/tarokka/{{ devil }}.png" alt="Front">
                    </div>
                </div>
            </div>
        </td>
        <td>
            <div class="flip-card">
                <div class="flip-card-inner">
                    <div class="flip-card-back">
                        <img class="card" src="/static/img/tarokka/__Back.png" alt="Back">
                    </div>
                    <div class="flip-card-front">
                        <img class="card" src="/static/img/tarokka/{{ sword }}.png" alt="Front">
                    </div>
                </div>
            </div>
        </td>
    </tr>
    <tr>
        <td></td>
        <td>
            <div class="flip-card">
                <div class="flip-card-inner">
                    <div class="flip-card-back">
                        <img class="card" src="/static/img/tarokka/__Back.png" alt="Back">
                    </div>
                    <div class="flip-card-front">
                        <img class="card" src="/static/img/tarokka/{{ ally }}.png" alt="Front">
                    </div>
                </div>
            </div>
        </td>
        <td></td>
    </tr>
</table>


<script type="module">
    import { init } from "/js/curse_of_strahd/tarokka.js";
    init();
</script>