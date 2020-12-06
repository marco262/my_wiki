% rebase("common/base.tpl", title=name)

<p>{{type}}, {{rarity.lower()}}{{!" <i>(requires attunement)</i>" if attunement else ""}}</p>

{{!description_md}}

<hr>
<p><em>Source: {{source}}</em></p>
