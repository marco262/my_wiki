% rebase("common/base.tpl", title="Tarokka Controls")

<link rel="stylesheet" type="text/css" href="/static/css/tarokka_controls.css">

<p class="visual-aid-link" title="iframe|/curse_of_strahd/tarokka">Display Tarokka Table</p>

<table>
    <tr>
        <td></td>
        <td>
            <img class="card" id="top" src="/media/img/tarokka/__Back.png">
            <div class="button-div">
                <input type="checkbox" class="inverted-checkbox" id="inverted-top" value="top">Inverted
                <input type="checkbox" class="off-grid-checkbox" id="off-grid-top" value="top">Off Grid
                <input type="checkbox" class="flipped-checkbox" id="flipped-top" value="top">Flipped
            </div>
            <div class="dropdown-div">
                <select class="force-card-set" id="force-card-set-top">
                    <option value="">&lt;random&gt;</option>
                </select>
            </div>
        </td>
        <td></td>
    </tr>
    <tr>
        <td>
            <img class="card" id="left" src="/media/img/tarokka/__Back.png">
            <div class="button-div">
                <input type="checkbox" class="inverted-checkbox" id="inverted-left" value="left">Inverted
                <input type="checkbox" class="off-grid-checkbox" id="off-grid-left" value="left">Off Grid
                <input type="checkbox" class="flipped-checkbox" id="flipped-left" value="left">Flipped
            </div>
            <div class="dropdown-div">
                <select class="force-card-set" id="force-card-set-left">
                    <option value="">&lt;random&gt;</option>
                </select>
            </div>
        </td>
        <td>
            <img class="card" id="middle" src="/media/img/tarokka/__Back.png">
            <div class="button-div">
                <input type="checkbox" class="inverted-checkbox" id="inverted-middle" value="middle">Inverted
                <input type="checkbox" class="off-grid-checkbox" id="off-grid-middle" value="middle">Off Grid
                <input type="checkbox" class="flipped-checkbox" id="flipped-middle" value="middle">Flipped
            </div>
            <div class="dropdown-div">
                <select class="force-card-set" id="force-card-set-middle">
                    <option value="">&lt;random&gt;</option>
                </select>
            </div>
        </td>
        <td>
            <img class="card" id="right" src="/media/img/tarokka/__Back.png">
            <div class="button-div">
                <input type="checkbox" class="inverted-checkbox" id="inverted-right" value="right">Inverted
                <input type="checkbox" class="off-grid-checkbox" id="off-grid-right" value="right">Off Grid
                <input type="checkbox" class="flipped-checkbox" id="flipped-right" value="right">Flipped
            </div>
            <div class="dropdown-div">
                <select class="force-card-set" id="force-card-set-right">
                    <option value="">&lt;random&gt;</option>
                </select>
            </div>
        </td>
    </tr>
    <tr>
        <td></td>
        <td>
            <img class="card" id="bottom" src="/media/img/tarokka/__Back.png">
            <div class="button-div">
                <input type="checkbox" class="inverted-checkbox" id="inverted-bottom" value="bottom">Inverted
                <input type="checkbox" class="off-grid-checkbox" id="off-grid-bottom" value="bottom">Off Grid
                <input type="checkbox" class="flipped-checkbox" id="flipped-bottom" value="bottom">Flipped
            </div>
            <div class="dropdown-div">
                <select class="force-card-set" id="force-card-set-bottom">
                    <option value="">&lt;random&gt;</option>
                </select>
            </div>
        </td>
        <td></td>
    </tr>
</table>

<p>
    <button id="deal-button">Deal</button>
    <button id="show-all-button">Show All</button>
    <button id="hide-all-button">Hide All</button>
    <button id="reset-button">Reset</button>
</p>

<p>
    <select name="reading" id="reading-name">
      <option value="Ezmerelda Reading">Ezmerelda Reading</option>
      <option value="Ireena Reading">Ireena Reading</option>
      <option value="Prophecy">Prophecy</option>
      <option value="Strahd Reading">Strahd Reading</option>
      <option value="barry reading">Barry Reading</option>
    </select>
    <button id="set-reading-button">Set Reading</button>
</p>

<p>
    <button id="set-random-reading-button">Set Random Reading</button>
    <button id="set-random-reading-w-force-button">Set Random Reading (w/ force)</button>
    <button id="force-cards-button">Force Cards</button>
    <button id="clear-forced-cards">Clear Forced Cards</button>
</p>

<p>
    <button id="sync-button">Sync With Server</button>
</p>

<script type="module">
    import {init} from "/static/js/curse_of_strahd/tarokka_controls.js";
    import {init_links} from "/static/js/common/visual_aid_backend.js";
    init();
    init_links();
</script>
