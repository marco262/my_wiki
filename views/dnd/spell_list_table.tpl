% from data.dnd.enums import spell_classes, source_acronyms
% if not get("spells"):
<i>No Results</i>
% else:
<table style="width: 100%">
    <tr>
        <th style="min-width: 264px;">Spell Name</th>
        <th style="min-width: 100px;">School</th>
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
        <td>
            <%
            r = "<sup>r</sup>" if s["ritual_spell"] else ""
            c = "<sup>c</sup>" if s["concentration_spell"] else ""
            %>
            <a href="/dnd/spell/{{k}}">{{s["title"]}}</a>{{! r }}{{! c }}
        </td>
        <td>{{s["school"].title()}}</td>
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
        <td>
            % source = s["source"].split(", p")[0]
            <div class="tooltip">{{source_acronyms[source]}}
                <span class="tooltiptext">{{source}}</span>
            </div>
        </td>
    <tr>
    % end
</table>
% end
