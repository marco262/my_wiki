% from data.dnd.enums import spell_classes
% if not get("spells"):
<i>No Results</i>
% else:
<table>
    <tr>
        <th>Spell Name</th>
        <th>School</th>
        <%
        if get("show_classes"):
            for c in spell_classes:
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
        <td style="min-width: 264px;">
            <%
            r = "<sup>r</sup>" if s["ritual_spell"] else ""
            c = "<sup>c</sup>" if s["concentration_spell"] else ""
            %>
            <a href="/dnd/spell/{{k}}">{{s["title"]}}</a>{{! r }}{{! c }}
        </td>
        <td style="min-width: 102px;">{{s["school"].title()}}</td>
        <%
        if get("show_classes"):
            for c in spell_classes:
        %>
        <td style="text-align: center;">
            {{"X" if c in s["classes"] or (get("ua_spells") and c in s.get("classes_ua", [])) else ""}}
        </td>
        <%
            end
        end
        %>
        <td style="min-width: 233px;">{{s["source"].split(", p")[0]}}</td>
    <tr>
    % end
</table>
% end
