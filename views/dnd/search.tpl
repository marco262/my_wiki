% rebase("common/base.tpl", title="Search")

<p>
Search Key:
<input type="text" style="width: 200px;" id="search_key" />
<input type="button" value="Search" id="search_button" />
</p>

<div id="search_results">
    % if not defined("search_results"):
    <i>Search results will appear here</i>
    % else:
    %   for title, filepath, html_link, context in search_results:
    <div class="search-result">
        <h2 class="search-result-title"><a href="{{ html_link }}">{{ title }}</a></h2>
        <div class="search-result-path">Path: {{ filepath }}</div>
        <blockquote class="search-result-context">{{! context }}</blockquote>
    </div>
    %   end
    % end
</div>

<script type="module">
    import {search} from "/js/dnd/search.js";
    let search_key_box = document.getElementById("search_key");
    search_key_box.focus();
    % if defined("search_key"):
    search_key_box.value = "{{ search_key }}";
    % end
    document.getElementById("search_button").onclick = search;
</script>
