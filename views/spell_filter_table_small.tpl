<table border="1">
    <tr>
        <th>Spell Name</th>
        <th>School</th>
        <th>Source</th>
    </tr>
    % for s in spells:
    <tr>
        <td><a href="/spell/{{s["title"]}}">{{s["title"]}}</a></td>
        <td>{{s["school"].title()}}</td>
        <td>{{s["source"].split(", p")[0]}}</td>
    <tr>
    % end
</table>