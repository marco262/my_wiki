<div class="npc-sheet">
    <link rel="stylesheet" type="text/css" href="/static/css/monster-sheet.css">
    <span class="npc-sheet-hover">npc</span>
    <div class="monster-sheet" style="max-width: {{ width }};">
        <div class="top-bottom-bar"></div>
        <h1 class="name">{{ f"CR {cr}" if cr is not None else f"Level {level}" }} {{ race }} {{ role }}</h1>
        <div class="red-bar"></div>
        <div class="text"><strong>Armor Class</strong> {{ armor_class }}</div>
        <div class="text"><strong>Hit Points</strong> {{ hit_points }}</div>
        <div class="text"><strong>Speed</strong> {{ speed }}</div>
        <div class="red-bar"></div>
        % if defined("saves"):
        <div class="text"><strong>Saving Throws</strong> {{ saves }}</div>
        % end
        <div class="text"><strong>Skills</strong> Untrained {{ untrained }}, Proficient {{ proficient }}, Expertise {{ expertise }}</div>
        % if defined("damage_vulnerabilities"):
        <div class="text"><strong>Damage Vulnerabilities</strong> {{ damage_vulnerabilities }}</div>
        % end
        % if damage_resistances:
        <div class="text"><strong>Damage Resistances</strong> {{ damage_resistances }}</div>
        % end
        % if damage_immunities:
        <div class="text"><strong>Damage Immunities</strong> {{ damage_immunities }}</div>
        % end
        % if defined("condition_immunities"):
        <div class="text"><strong>Condition Immunities</strong> {{ condition_immunities }}</div>
        % end
        % if senses:
        <div class="text"><strong>Senses</strong> {{ senses }}</div>
        % end
        <div class="red-bar"></div>
        % if special_abilities:
        <div class="text-black">
            {{! special_abilities }}
        </div>
        % end
        % if bonus_actions:
        <h2 class="actions-header">Bonus Actions</h2>
        <div class="text-black">
            {{! bonus_actions }}
        </div>
        % end
        <h2 class="actions-header">Actions</h2>
        <div class="text-black">
            {{! actions }}
        </div>
        % if reactions:
        <h2 class="actions-header">Reactions</h2>
        <div class="text-black">
            {{! reactions }}
        </div>
        % end
        % if villain_actions:
        <h2 class="actions-header">Villain Actions</h2>
        <div class="text-black">
            {{! villain_actions }}
        </div>
        % end
        <div class="top-bottom-bar"></div>
    </div>
</div>