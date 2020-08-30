% rebase("common/base.tpl", title="Monsters by Name")

<ul>
% for name, link in monsters.items():
    <li><a href="{{ link }}">{{ name }}</a></li>
% end
</ul>
