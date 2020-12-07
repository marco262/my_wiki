% rebase("common/base.tpl", title=name)
<%
subtype = f" <i>({subtype})</i>" if subtype else ""
if notes:
    pass
elif classes:
    notes = f"requires attunement by a {', '.join(classes)}"
elif attunement:
    notes = "requires attunement"
end
notes = f" <i>({notes})</i>" if notes else ""
%> 
<p>{{type.title()}}{{!subtype}}, {{rarity.lower()}}{{!notes}}</p>

{{!description_md}}

<hr>
<p><em>Source: {{source}}</em></p>
