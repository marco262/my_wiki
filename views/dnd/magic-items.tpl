<%
from data.dnd.enums import magic_item_rarities

if not magic_items:
%>
<i>No Results</i>
<%
else:
    for rarity in magic_item_rarities:
        if rarity in magic_items:
%>

<h2>{{rarity}}</h2>
<%
            include("dnd/magic-items-table.tpl", magic_items=magic_items[rarity])
        end
    end
end
%>
