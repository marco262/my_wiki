% include("common/header.tpl", title=title)
<h1>{{title}}</h1>

% if defined("toc"):
% include("common/toc.tpl")
% end

{{!text}}

% if accordion_text:
<script type="module">
    import { init_accordions } from "/js/common/utils.js";
    init_accordions();
</script>
% end
% include("common/footer.tpl")