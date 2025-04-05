<%
from src.common.utils import ordinal

if not spell_dict:
%>
<i>No Results</i>
<%
else:
    for level in ["0", "1", "2", "3", "4", "5", "6", "7", "8", "9"]:
        if level in spell_dict:
            level_name = "Cantrips" if level == "0" else f"{ordinal(level)} Level"
%>

<h2>{{level_name}}</h2>
<%
            include("onednd/spell_list_table.tpl", spells=spell_dict[level])
        end
    end
    %>
    <em><sup>r = ritual, c = concentration</sup></em>
% end
