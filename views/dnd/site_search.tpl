% rebase("common/base.tpl", title=title)

% if include_search_box:
<p>
    Search Key:
    <input type="text" style="width: 200px;" id="search_key" />
    <input type="button" value="Search" id="search_button" />
    <span id="request-sent" hidden><i>Search request sent. Waiting for response...</i></span>
</p>
% end

<div id="search_results">
    % if not defined("search_results"):
    <i>Search results will appear here</i>
    % elif not search_results:
    <i>No results</i>
    % else:
    %   for title, filepath, html_link, contexts in search_results:
    <div class="search-result">
        <h2 class="search-result-title"><a href="{{ html_link }}">{{ title }}</a></h2>
        <div class="search-result-path">Path: {{ filepath }}</div>
        % if contexts is not None:
            % for context in contexts:
        <blockquote class="search-result-context">{{! context }}</blockquote>
            % end
        % end
    </div>
    %   end
    % end
</div>

% if defined("total_pages") and total_pages > 1:
<div id="search_navigation">
    % if page == 1:
    &lt;&nbsp;
    % else:
    <a href="{{ search_key }}?page={{ page - 1 }}">&lt;</a>&nbsp;
    % end
    % for i in range(1, total_pages + 1):
        % if i == page:
        {{ i }}&nbsp;
        % else:
        <a href="{{ search_key }}?page={{ i }}">{{ i }}</a>&nbsp;
        % end
    % end
    % if page < total_pages:
    <a href="{{ search_key }}?page={{ page + 1 }}">&gt;</a>
    % else:
    &gt;
    % end
</div>
% end

% if defined("processing_time"):
<hr>
<div class="search-processing-time">Results returned in: {{ round(processing_time, 3) }} seconds</div>
% end

<script type="module">
    import {search, on_key_press} from "/js/dnd/search.js";
    let search_key_box = document.getElementById("search_key");
    search_key_box.focus();
    search_key_box.onkeypress = on_key_press;
    % if defined("search_key"):
    search_key_box.value = "{{! search_key }}";
    % end
    document.getElementById("search_button").onclick = search;
</script>
