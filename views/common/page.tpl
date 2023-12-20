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
