% rebase("common/base.tpl", title=title)

<%
from data.dnd.enums import classes as class_list
spell_class_list = []
for c in class_list:
    if c in classes or c in get("classes_ua", []):
        link = '<a href="/dnd/class_spell_list/{}/true">{}</a>'.format(c, c.title())
        if c in get("classes_ua", []):
            link = "[" + link + "]"
        end
        spell_class_list.append(link)
    end
end
%>
<p><em>{{!('&nbsp;' * 4).join(spell_class_list)}}</em></p>

% fmt = "{school} cantrip" if level.lower() == "cantrip" else "Level {level} {school}" 
<p>{{fmt.format(level=level, school=school.title())}}{{" (ritual)" if ritual_spell else ""}}</p>

<p>
<strong>Casting Time:</strong> {{casting_time}}<br />
<strong>Range:</strong> {{range}}<br />
<strong>Components:</strong> {{", ".join(components)}}{{" (" + material + ")" if "M" in components else ""}}<br />
<strong>Duration:</strong> {{duration}}</p>

{{!description_md}}
% if defined('at_higher_levels'):
<p><strong>At Higher Levels:</strong> {{at_higher_levels}}</p>

% end
% if defined('at_higher_levels_homebrew'):
<div class="homebrew-note"><strong>At Higher Levels (homebrew):</strong> {{at_higher_levels_homebrew}}</div>

% end
<hr class="no-float">
<p><em>
    % if defined('source_link'):
    Source: <a href="{{ source_link }}">{{ source }}</a>
    % else:
    Source: {{ source }}
    % end
</em></p>
