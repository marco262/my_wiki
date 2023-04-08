% rebase("common/base.tpl", title=name)
<%
subtype = f" ({subtype})" if subtype else ""
if notes:
    pass
elif classes:
    notes = f"requires attunement by a {', '.join(classes)}"
elif attunement:
    notes = "requires attunement"
end
notes = f" ({notes})" if notes else ""
%> 
<p><em>{{type.title()}}{{!subtype}}, {{ rarity_type.lower() }} {{rarity.lower()}}{{!notes}}</em></p>

{{!description_md}}

<hr>
<p><em>Source: {{source}}</em></p>
