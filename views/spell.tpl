<h1>{{title}}</h1>

<p>{{"    ".join([c.title() for c in classes])}}</p>

<p>Level {{level}} {{school.title()}}{{" (ritual)" if ritual_spell else ""}}</p>

<p><strong>Casting Time:</strong> {{casting_time}}<br />
<strong>Components:</strong> {{", ".join(components)}}{{" (" + material + ")" if "M" in components else ""}}<br />
<strong>Duration:</strong> 8 hours</p>

<p>{{description}}</p>

<p><strong>At Higher Levels:</strong> {{at_higher_levels}}</p>

<hr />

<p><em>Source: {{source}}</em></p>
