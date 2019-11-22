% from data.enums import classes
% if not get("spells"):
<i>No Results</i>
% else:
<table>
    <tr>
        <th>Spell Name</th>
        <th>School</th>
        <%
        if get("show_classes"):
            for c in classes:
        %>
        <th>{{c.title()}}</th>
        <%
            end
        end
        %>
        <th>Source</th>
    </tr>
    % for k, s in spells:
    <tr>
        <td><a href="/spell/{{k}}">{{s["title"]}}</a></td>
        <td>{{s["school"].title()}}</td>
        <%
        if get("show_classes"):
            for c in classes:
        %>
        <td>{{"X" if c in s["classes"] or (get("ua_spells") and c in s.get("classes_ua", [])) else ""}}</td>
        <%
            end
        end
        %>
        <td>{{s["source"].split(", p")[0]}}</td>
    <tr>
    % end
</table>
% end
