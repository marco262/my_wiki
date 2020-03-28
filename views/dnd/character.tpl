% include("common/header.tpl", title=name)
<h1>{{ name }}</h1>

<p>
    <b>Race:</b> {{ race }}<br>
    <b>Class:</b> {{ get("class") }}<br>
    <b>Level:</b> {{ level }}<br>
    <b>Proficiency:</b> {{ proficiency_bonus }}
</p>

<div class="tab-bar">
    <button class="tab-link">Ability Scores</button>
    <button class="tab-link">Skills</button>
</div>

<div class="tab-page" id="attributes">
    % for attr, values in attributes.items():
    <div><i>{{ attr }}:</i></div>
    <div class="mod">{{ values["score"] }} ({{ values["mod"] }})</div>
    % end
</div>

<div class="tab-page" id="skills">
    <div class="tooltip">P<div class="tooltiptext">Proficiency</div></div>
    <div class="tooltip">E<div class="tooltiptext">Expertise</div></div>
    <div></div>
    <div></div>
    % for skill, mod in skills:
    <div><input type="checkbox" id="{{ skill.lower() }}_prof"{{ " checked" if skill in proficiencies else "" }}></div>
    <div><input type="checkbox" id="{{ skill.lower() }}_ex"{{ " checked" if skill in expertises else "" }}></div>
    <div><i>{{ skill }}:</i></div>
    <div class="mod">{{ mod }}</div>
    % end
</div>
% end

% include("common/footer.tpl")
