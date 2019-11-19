% include("header.tpl", title=title)

<h1>{{title}}</h1>

<p><em>{{!('&nbsp;' * 4).join(['<a href="/class_spell_list/{}">{}</a>'.format(c, c.title()) for c in classes])}}</em></p>

<p>Level {{level}} {{school.title()}}{{" (ritual)" if ritual_spell else ""}}</p>

<p><strong>Casting Time:</strong> {{casting_time}}<br />
<strong>Components:</strong> {{", ".join(components)}}{{" (" + material + ")" if "M" in components else ""}}<br />
<strong>Duration:</strong> {{duration}}</p>

{{!description_md}}
% if defined('at_higher_levels'):
<p><strong>At Higher Levels:</strong> {{at_higher_levels}}</p>

% end
<p><em>Source: {{source}}</em></p>

% include("footer.tpl")
