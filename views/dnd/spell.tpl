% include("common/header.tpl", title=title)

<h1>{{title}}</h1>
<%
from data.enums import classes as class_list
spell_class_list = []
for c in class_list:
    if c in classes or c in get("classes_ua", []):
        link = '<a href="/class_spell_list/{}">{}</a>'.format(c, c.title())
        if c in get("classes_ua", []):
            link = "[" + link + "]"
        end
        spell_class_list.append(link)
    end
end
%>
<p><em>{{!('&nbsp;' * 4).join(spell_class_list)}}</em></p>

<p>Level {{level}} {{school.title()}}{{" (ritual)" if ritual_spell else ""}}</p>

<p><strong>Casting Time:</strong> {{casting_time}}<br />
<strong>Components:</strong> {{", ".join(components)}}{{" (" + material + ")" if "M" in components else ""}}<br />
<strong>Duration:</strong> {{duration}}</p>

{{!description_md}}
% if defined('at_higher_levels'):
<p><strong>At Higher Levels:</strong> {{at_higher_levels}}</p>

% end
<p><em>Source: {{source}}</em></p>

% include("common/footer.tpl")
