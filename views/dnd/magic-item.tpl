% rebase("common/base.tpl", title=name)
<%
subtype_str = f" ({subtype_str})" if subtype_str else ""
attunement_str = f" ({attunement_str})" if attunement_str else ""
%> 
<p><em>{{type.title()}}{{!subtype_str}}, {{rarity}}{{!attunement_str}}</em></p>

{{!description_md}}

<hr>
<p><em>Source: {{source}}</em></p>
