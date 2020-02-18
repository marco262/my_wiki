% include("common/header.tpl", title=title)
<h1>{{ title }}</h1>
% if characters is None:
<p><i>No characters created yet</i>
% else:
<ul>
    % for name in characters:
        <li><a href="/dnd/character/{{ name }}">{{ name }}</a></li>
    % end
</ul>
% end

% include("common/footer.tpl")
