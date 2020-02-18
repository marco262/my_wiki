% include("common/header.tpl", title=name)
<h1>{{ name }}</h1>

<p>
<b>Race: {{ race }}</b><br>
<b>Class: {{ dnd_class }}</b><br>
<ul>
    % for attr, value in attributes.items():
    <li>{{ attr }}: {{ value }}</li>
    % end
</ul>
% end

% include("common/footer.tpl")
