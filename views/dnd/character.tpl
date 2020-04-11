<link rel="stylesheet" type="text/css" href="/static/css/character_sheet.css">
% include("common/header.tpl", title=name)
% from data.dnd.enums import ability_scores, skills
<h1>{{ name }}</h1>

<p>
    <b>Race:</b> <span id="race"></span><br>
    <b>Class:</b> <span id="class"></span><br>
    <b>Level:</b> <span id="level"></span><br>
</p>

<div class="tab-bar">
    <button class="tab-button tab-active" id="stats-tab">Stats</button>
    <button class="tab-button" id="skills-tab">Skills</button>
    <button class="tab-button" id="combat-tab">Combat</button>
</div>

<div class="tab-page" id="stats-page" style="display: inline-block;">
    <b>Ability Scores:</b>
    <div id="ability-scores-grid">
        % for ability_score in ability_scores:
        <div><a class="dice-roll" id="{{ ability_score.lower() }}-check">{{ ability_score }}:</div>
        <div class="mod">
            <span id="{{ ability_score.lower() }}-score">10</span>
            (<span id="{{ ability_score.lower() }}-mod">+0</span>)
        </div>
        % end
    </div>

    <b>Saves:</b>
    <div id="saves-grid">
        <div class="tooltip" style="text-align: center;">P<div class="tooltiptext">Proficiency</div></div>
        <div></div>
        <div></div>
        % for ability_score in ability_scores:
        <div><input type="checkbox" class="save-checkbox" id="{{ ability_score.lower() }}-prof"></div>
        <div id="{{ ability_score.lower() }}-save-label"><i>{{ ability_score }}:</i></div>
        <div class="mod" id="{{ ability_score.lower() }}-save-mod">+0</div>
        % end
    </div>
</div>

<div class="tab-page" id="skills-page">
    <div id="skills-grid">
        <div class="tooltip" style="text-align: center;">P<div class="tooltiptext">Proficiency</div></div>
        <div class="tooltip" style="text-align: center;">E<div class="tooltiptext">Expertise</div></div>
        <div></div>
        <div></div>
        % for skill, ability_score in skills:
        % skill_name = skill.lower().replace(" ", "-")
        <div><input type="checkbox" class="skill-prof-checkbox" id="{{ skill_name }}-prof"></div>
        <div><input type="checkbox" class="skill-ex-checkbox" id="{{ skill_name }}-ex"></div>
        <div id="{{ skill_name }}-label"><i>{{ skill }}:</i></div>
        <div class="mod" id="{{ skill_name }}-mod">+0</div>
        % end
    </div>
</div>

<div class="tab-page" id="combat-page">
    <div id="misc-grid">
        <div><i>Proficiency Bonus:</i></div>
        <div class="mod" id="proficiency-bonus"></div>
        <div><i>Initiative:</i></div>
        <div class="mod" id="initiative"></div>
        <div><i>Melee:</i></div>
        <div class="mod" id="melee-stats"></div>
        <div><i>Ranged:</i></div>
        <div class="mod" id="ranged-stats"></div>
    </div>
</div>


<script type="module">
    import { load_json } from "/js/dnd/character-sheet.js";
    load_json({{! json }});
    import { init_tabs } from "/js/common/utils.js";
    init_tabs();
</script>

% include("common/footer.tpl")
