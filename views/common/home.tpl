* [5e D&D Wiki](/dnd/)
* [One D&D Wiki](/onednd/)
* [Numenera Resources](/numenera/)

## Campaigns

### Active

* [Class 1A](/class_1a/)
* [A Realm Reborn](/arr/)

### Past

* [The Heroes of Sandpoint](/sandpoint/)
* [Here There Be Pirates!](/pirates/)
* [Curse of Strahd](/curse_of_strahd/)
* [Waterdeep Adventures](/waterdeep/)
* [Dragon Heist](/dragon_heist/)

<div id="last-commit-text">
    <strong>Last commit:</strong> {{ commit_history }}<br>
    <strong>Last restart:</strong> {{ last_restart }}
</div>
<span id="status-text" hidden><em>Already up to date!</em></span>

<script type="module">
    import { ajax_call } from "/static/js/common/utils.js";

    function load_changes() {
        ajax_call("/load_changes", handle_load)
    }

    function handle_load(xhttp) {
        let status_text = document.getElementById("status-text");
        if (xhttp.responseText === "Restarting") {
            status_text.innerHTML = "<em>Updates found. Web server is restarting. This page will automatically reload in 5 seconds...</em>";
            status_text.hidden = false;
            setTimeout(reload_page, 5000);
        } else {
            status_text.hidden = false;
        }
    }

    function reload_page() {
        location.reload();
    }

    document.getElementById("last-commit-text").ondblclick = load_changes;
</script>
