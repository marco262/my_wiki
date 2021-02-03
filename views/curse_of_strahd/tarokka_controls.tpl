% rebase("common/base.tpl", title="Tarokka Controls")

<link rel="stylesheet" type="text/css" href="/static/css/tarokka_controls.css">

<p class="visual-aid-link" title="iframe|/curse_of_strahd/tarokka">Display Tarokka Table</p>

<table>
    <tr>
        <td></td>
        <td>
            <img class="card" id="top" src="/static/img/tarokka/__Back.png">
            <div class="button-div">
                <input type="checkbox" class="inverted-checkbox" id="inverted-top">Inverted
                <input type="checkbox" class="off-grid-checkbox" id="off-grid-top">Off Grid
                <input type="checkbox" class="flipped-checkbox" id="flipped-top">Flipped
            </div>
        </td>
        <td></td>
    </tr>
    <tr>
        <td>
            <img class="card" id="left" src="/static/img/tarokka/__Back.png">
            <div class="button-div">
                <input type="checkbox" class="inverted-checkbox" id="inverted-left">Inverted
                <input type="checkbox" class="off-grid-checkbox" id="off-grid-left">Off Grid
                <input type="checkbox" class="flipped-checkbox" id="flipped-left">Flipped
            </div>
        </td>
        <td>
            <img class="card" id="middle" src="/static/img/tarokka/__Back.png">
            <div class="button-div">
                <input type="checkbox" class="inverted-checkbox" id="inverted-middle">Inverted
                <input type="checkbox" class="off-grid-checkbox" id="off-grid-middle">Off Grid
                <input type="checkbox" class="flipped-checkbox" id="flipped-middle">Flipped
            </div>
        </td>
        <td>
            <img class="card" id="right" src="/static/img/tarokka/__Back.png">
            <div class="button-div">
                <input type="checkbox" class="inverted-checkbox" id="inverted-right">Inverted
                <input type="checkbox" class="off-grid-checkbox" id="off-grid-right">Off Grid
                <input type="checkbox" class="flipped-checkbox" id="flipped-right">Flipped
            </div>
        </td>
    </tr>
    <tr>
        <td></td>
        <td>
            <img class="card" id="bottom" src="/static/img/tarokka/__Back.png">
            <div class="button-div">
                <input type="checkbox" class="inverted-checkbox" id="inverted-bottom">Inverted
                <input type="checkbox" class="off-grid-checkbox" id="off-grid-bottom">Off Grid
                <input type="checkbox" class="flipped-checkbox" id="flipped-bottom">Flipped
            </div>
        </td>
        <td></td>
    </tr>
</table>

<p>
    <button id="deal-button">Deal</button>
    <button id="flip-all-button">Flip All</button>
    <button id="reset-button">Reset</button>
</p>

<p>
    <select name="reading" id="reading-name">
      <option value="Ezmerelda Reading">Ezmerelda Reading</option>
      <option value="Ireena Reading">Ireena Reading</option>
      <option value="Prophecy">Prophecy</option>
    </select>
    <button id="set-reading-button">Set Reading</button>
</p>

<p>
    <button id="set-random-reading-button">Set Random Reading</button>
</p>

<script type="module">
    import {init} from "/js/curse_of_strahd/tarokka_controls.js";
    import {init_links} from "/js/common/visual_aid_backend.js";
    init();
    init_links();
</script>
