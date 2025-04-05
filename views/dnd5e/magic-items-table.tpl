% from data.dnd.enums import source_acronyms

<table>
    <tr>
        <th>Name</th>
        <th>Minor/Major</th>
        <th style="min-width: 110px;">Type</th>
        <th>Attunement?</th>
        <th>Subtype</th>
        <th>Class Restrictions</th>
        <th>Source</th>
    </tr>
% for filename, magic_item in magic_items:
    <tr>
        <td><a href="/dnd/equipment/magic-item/{{ filename }}">{{ magic_item["name"] }}</a></td>
        <td>{{ magic_item["rarity_type"] }}</td>
        <td>{{ magic_item["type"] }}</td>
        <td>{{ "yes" if magic_item["attunement"] else "no" }}</td>
        <td>{{ magic_item["subtype"] }}</td>
        <td>{{ ", ".join(magic_item["classes"]) }}</td>
        <td>
            % source = magic_item["source"].split(", p")[0]
            <div class="tooltip">{{source_acronyms[source]}}
                <span class="tooltiptext" style="width: 10em;">{{source}}</span>
            </div>
        </td>
    </tr>
% end
</table>
