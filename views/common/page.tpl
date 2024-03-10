% rebase("common/base.tpl", title=title)

% if get("toc"):
<div id="toc">
    <p id="toc-header"><span id="toc-collapse">[-]</span> <strong>Table of Contents</strong></p>
    <div id="toc-content">
    {{!toc}}
    </div>
</div>
% end

{{!text}}

<script type="module">
  import {init_links} from "/static/js/common/visual_aid_backend.js";
  init_links();
</script>
