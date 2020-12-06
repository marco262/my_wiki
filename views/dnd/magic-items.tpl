% rebase("common/base.tpl", title="Magic Items")

<table>
    <tr>
        <th>Name</th>
        <th>Type</th>
        <th>Rarity</th>
        <th>Attunement?</th>
        <th>Notes</th>
        <th style="width: 70px;">Source</th>
    </tr>
% for filename, magic_item in magic_items:
    <tr>
        <td><a href="/dnd/equipment/magic-item/{{ filename }}">{{ magic_item["name"] }}</a></td>
        <td>{{ magic_item["type"] }}</td>
        <td>{{ magic_item["rarity"] }}</td>
        <td>{{ "yes" if magic_item["attunement"] else "no" }}</td>
        <td>{{ magic_item["notes"] }}</td>
        <td>{{ magic_item["source"] }}</td>
    </tr>
% end
</table>
