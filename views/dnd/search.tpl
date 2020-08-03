% rebase("common/base.tpl", title="Search")

<p>
Search Key:
<input type="text" style="width: 200px;" id="search_key" />
<input type="button" value="Search" id="search_button" />
</p>

<div id="search_results">
    % if not defined("search_results"):
    <em>Search results will appear here</em>
    % else:
    %   for title, filepath, html_link, context in search_results:
    <div class="search-result">
        <h2 class="search-result-title"><a href="{{ html_link }}">{{ title }}</a></h2>
        <div class="search-result-path">Path: {{ filepath }}</div>
        % if context:
        <blockquote class="search-result-context">{{! context }}</blockquote>
        % end
    </div>
    %   end
    <hr>
    <div id="query-time">
        Your results were returned in {{ query_time }} seconds.
    </div>
    % end
</div>

<script type="module">
    import {search, on_key_press} from "/js/dnd/search.js";
    let search_key_box = document.getElementById("search_key");
    search_key_box.focus();
    search_key_box.onkeypress = on_key_press;
    % if defined("search_key"):
    search_key_box.value = "{{ search_key }}";
    % end
    document.getElementById("search_button").onclick = search;
</script>
