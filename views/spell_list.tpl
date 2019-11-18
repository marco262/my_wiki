% include("header.tpl", title=title)
<h1>{{title}}</h1>
<%
from utils import ordinal
for level in ["cantrip", "1", "2", "3", "4", "5", "6", "7", "8", "9"]:
    if level in spell_dict:
%>

<h2>{{ordinal(level)}}</h2>
<%
        include("spell_list_table.tpl", spells=spell_dict[level], show_classes=get("show_classes"))
    end
end
include("footer.tpl")
%>
