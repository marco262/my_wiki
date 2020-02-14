% include("header.tpl", title=title)
<h1>{{title}}</h1>

% if defined("toc"):
% include("toc.tpl")
% end

{{!text}}
% include("footer.tpl")