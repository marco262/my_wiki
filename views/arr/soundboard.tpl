% rebase("common/base.tpl", title="Soundboard")

<ul>
% for path in glob_file_list:
<li><span class="visual-aid-link" title="load|music|arr/{{ path }}">{{ path }}</span></li>
% end
</ul>

<script type="module">
    import { init_links, init_soundboard } from "/static/js/common/visual_aid_backend.js";
    init_links();
    init_soundboard();
</script>