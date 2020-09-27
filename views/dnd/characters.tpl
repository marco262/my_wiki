% rebase("common/base.tpl", title=title)
% if not characters:
<p><i>No characters created yet</i>
% else:
<ul>
    % for name in characters:
        <li><a href="/dnd/character/{{ name }}">{{ name }}</a></li>
    % end
</ul>
% end
