% rebase("common/base.tpl", title=title)
<link rel="stylesheet" type="text/css" href="/static/css/character_sheet.css">
% from data.dnd.enums import ability_scores, skills
<p>
    <b>Race:</b> <span id="race"></span><br>
    <b>Class:</b> <span id="class"></span><br>
    <b>Level:</b> <span id="level"></span><br>
    <b>Background:</b> <span id="background"></span><br>
</p>

<div id="tab-container">
    <div id="tab-bar">
        <button class="tab-button tab-active" id="stats-tab">Stats</button>
        <button class="tab-button" id="skills-tab">Skills</button>
        <button class="tab-button" id="combat-tab">Combat</button>
        <button class="tab-button" id="spellcasting-tab">Spellcasting</button>
    </div>

    <div class="tab-page" id="stats-page" style="display: inline-block;">
        <b>Ability Scores:</b>
        <br>
        <div id="ability-scores-grid">
            % for ability_score in ability_scores:
            <div id="{{ ability_score.lower() }}-check">{{ ability_score }}:</div>
            <div class="mod">
                <span id="{{ ability_score.lower() }}-score">10</span>
                (<span id="{{ ability_score.lower() }}-mod">+0</span>)
            </div>
            % end
        </div>
        <br>

        <b>Saves:</b>
        <br>
        <div id="saves-grid">
            <div class="tooltip" style="text-align: center;">P<div class="tooltiptext">Proficiency</div></div>
            <div></div>
            <div></div>
            <div></div>
            % for ability_score in ability_scores:
            <div><input type="checkbox" class="save-checkbox" id="{{ ability_score.lower() }}-prof"></div>
            <div id="{{ ability_score.lower() }}-save-label"><i>{{ ability_score }}:</i></div>
            <div class="mod" id="{{ ability_score.lower() }}-save-mod">+0</div>
            <div><button class="roll-button" value="{{ ability_score.lower() }}-save-mod">Roll</button></div>
            % end
        </div>
        <br>
    </div>

    <div class="tab-page" id="skills-page">
        <div id="skills-grid">
            <div class="tooltip" style="text-align: center;">P<div class="tooltiptext">Proficiency</div></div>
            <div class="tooltip" style="text-align: center;">E<div class="tooltiptext">Expertise</div></div>
            <div></div>
            <div></div>
            <div></div>
            % for skill, ability_score in skills:
            % skill_name = skill.lower().replace(" ", "-")
            <div><input type="checkbox" class="skill-prof-checkbox" id="{{ skill_name }}-prof"></div>
            <div><input type="checkbox" class="skill-ex-checkbox" id="{{ skill_name }}-ex"></div>
            <div id="{{ skill_name }}-label"><i>{{ skill }}:</i></div>
            <div class="mod" id="{{ skill_name }}-mod">+0</div>
            <div><button class="roll-button" value="{{ ability_score.lower() }}-skill-mod">Roll</button></div>
            % end
        </div>
    </div>

    <div class="tab-page" id="combat-page">
        <div id="combat-grid">
            <div><i>Proficiency Bonus:</i></div>
            <div class="mod" id="proficiency-bonus"></div>
            <div><i>Initiative:</i></div>
            <div class="mod" id="initiative"></div>
            <div><i>Melee Attack:</i></div>
            <div class="mod" id="melee-attack-bonus"></div>
            <div><i>Ranged Attack:</i></div>
            <div class="mod" id="ranged-attack-bonus"></div>
        </div>
    </div>

    <div class="tab-page" id="spellcasting-page">
        <div id="spellcasting-grid">
            <div><i>Spellcasting Bonus:</i></div>
            <div class="mod" id="spellcasting-bonus"></div>
            <div><i>Spell Attack Bonus:</i></div>
            <div class="mod" id="spell-attack-bonus"></div>
            <div><i>Spell DC:</i></div>
            <div class="mod" id="spell-dc"></div>
        </div>
    </div>
</div>
<br>
<b>Class Features:</b>
<br>
<div id="class-features">
    <div id="class-features-grid"></div>
</div>

<div id="overlay" hidden></div>


<script type="module">
    import { load_json } from "/js/dnd/character-sheet.js";
    load_json({{! json }});
    import { init_tabs } from "/js/common/utils.js";
    init_tabs();
</script>
