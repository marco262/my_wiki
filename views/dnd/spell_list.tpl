<%
from src.common.utils import ordinal

if not spell_dict:
%>
<i>No Results</i>
<%
else:
    for level in ["cantrip", "1", "2", "3", "4", "5", "6", "7", "8", "9"]:
        if level in spell_dict:
%>

<h2>{{ordinal(level)}}</h2>
<%
            include("dnd/spell_list_table.tpl", spells=spell_dict[level])
        end
    end
    %>
    <em><sup>r = ritual, c = concentration</sup></em>
% end
