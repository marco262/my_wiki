<title>Private 5e Wiki - {{title}}</title>

<h1>{{title}}</h1>

<p><em>{{!('&nbsp;' * 4).join([c.title() for c in classes])}}</em></p>

<p>Level {{level}} {{school.title()}}{{" (ritual)" if ritual_spell else ""}}</p>

<p><strong>Casting Time:</strong> {{casting_time}}<br />
<strong>Components:</strong> {{", ".join(components)}}{{" (" + material + ")" if "M" in components else ""}}<br />
<strong>Duration:</strong> 8 hours</p>

<p>{{!description_md}}</p>
% if defined('at_higher_levels'):

<p><strong>At Higher Levels:</strong> {{at_higher_levels}}</p>
% end
<hr />

<p><em>Source: {{source}}</em></p>
