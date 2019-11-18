% if not get("spells"):
<i>No Results</i>
% else:
<table border="1">
    <tr>
        <th>Spell Name</th>
        <th>School</th>
        % if get("show_classes"):
        <th>Bard</th>
        <th>Cleric</th>
        <th>Druid</th>
        <th>Paladin</th>
        <th>Ranger</th>
        <th>Sorcerer</th>
        <th>Warlock</th>
        <th>Wizard</th>
        % end
        <th>Source</th>
    </tr>
    % for k, s in spells:
    <tr>
        <td><a href="/spell/{{k}}">{{s["title"]}}</a></td>
        <td>{{s["school"].title()}}</td>
        % if get("show_classes"):
        <td>{{"X" if "bard" in s["classes"] else ""}}</td>
        <td>{{"X" if "cleric" in s["classes"] else ""}}</td>
        <td>{{"X" if "druid" in s["classes"] else ""}}</td>
        <td>{{"X" if "paladin" in s["classes"] else ""}}</td>
        <td>{{"X" if "ranger" in s["classes"] else ""}}</td>
        <td>{{"X" if "sorcerer" in s["classes"] else ""}}</td>
        <td>{{"X" if "warlock" in s["classes"] else ""}}</td>
        <td>{{"X" if "wizard" in s["classes"] else ""}}</td>
        % end
        <td>{{s["source"].split(", p")[0]}}</td>
    <tr>
    % end
</table>
% end
