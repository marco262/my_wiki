<span class="visual-aid-link" title="iframe|curse_of_strahd/tarokka">Display Tarokka Table</span>

|| ||<button id="flip-top-button">Flip Top</button>|| || 
||<button id="flip-left-button">Flip Left</button>||<button id="flip-middle-button">Flip Middle</button>||<button id="flip-right-button">Flip Right</button>||
|| ||<button id="flip-bottom-button">Flip Bottom</button>|| ||

<button id="deal-button">Deal</button> <button id="flip-all-button">Flip All</button> <button id="reset-button">Reset</button>

<select name="reading" id="reading-name">
  <option value="Ezmerelda Reading">Ezmerelda Reading</option>
  <option value="Ireena Reading">Ireena Reading</option>
  <option value="Prophecy">Prophecy</option>
</select>
<button id="set-reading-button">Set Reading</button>

<button id="set-random-reading-button">Set Random Reading</button>

<script type="module">
    import {init} from "/js/curse_of_strahd/tarokka_controls.js";
    import {init_links} from "/js/common/visual_aid_backend.js";
    init();
    init_links();
</script>
