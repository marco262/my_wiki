<link rel="stylesheet" type="text/css" href="/static/css/monster-sheet.css">
<%
from src.dnd.utils import ability_mod
str_mod = ability_mod(strength)
dex_mod = ability_mod(dexterity)
con_mod = ability_mod(constitution)
int_mod = ability_mod(intelligence)
wis_mod = ability_mod(wisdom)
cha_mod = ability_mod(charisma)
%>
<div class="monster-sheet" style="width: {{ width }};">
    <div class="top-bottom-bar"></div>
    <h1 class="name">{{ name }}</h1>
    <div class="type">{{ size }} {{ type }}, {{ alignment }}</div>
    <div class="red-bar"><img class="red-bar-img" src="/static/img/stat-block-header-bar.svg"></div>
    <div class="text"><strong>Armor Class</strong> {{ armor_class }}</div>
    <div class="text"><strong>Hit Points</strong> {{ hit_points }}</div>
    <div class="text"><strong>Speed</strong> {{ speed }}</div>
    <div class="red-bar"><img class="red-bar-img" src="/static/img/stat-block-header-bar.svg"></div>
    <div class="ability-scores">
        <span class="ability-score-name">STR</span>
        <span class="ability-score-name">DEX</span>
        <span class="ability-score-name">CON</span>
        <span class="ability-score-name">INT</span>
        <span class="ability-score-name">WIS</span>
        <span class="ability-score-name">CHA</span>
        <span class="ability-score-value">{{ strength }} ({{ str_mod }})</span>
        <span class="ability-score-value">{{ dexterity }} ({{ dex_mod }})</span>
        <span class="ability-score-value">{{ constitution }} ({{ con_mod }})</span>
        <span class="ability-score-value">{{ intelligence }} ({{ int_mod }})</span>
        <span class="ability-score-value">{{ wisdom }} ({{ wis_mod }})</span>
        <span class="ability-score-value">{{ charisma }} ({{ cha_mod }})</span>
    </div>
    <div class="red-bar"><img class="red-bar-img" src="/static/img/stat-block-header-bar.svg"></div>
    % if defined("saves"):
    <div class="text"><strong>Saving Throws:</strong> {{ saves }}</div>
    % end
    % if defined("skills"):
    <div class="text"><strong>Skills:</strong> {{ skills }}</div>
    % end
    % if defined("damage_vulnerabilities"):
    <div class="text"><strong>Damage Vulnerabilities:</strong> {{ damage_vulnerabilities }}</div>
    % end
    % if defined("damage_resistances"):
    <div class="text"><strong>Damage Resistances:</strong> {{ damage_resistances }}</div>
    % end
    % if defined("damage_immunities"):
    <div class="text"><strong>Damage Immunities:</strong> {{ damage_immunities }}</div>
    % end
    % if defined("condition_immunities"):
    <div class="text"><strong>Condition Immunities:</strong> {{ condition_immunities }}</div>
    % end
    % if defined("senses"):
    <div class="text"><strong>Senses:</strong> {{ senses }}</div>
    % end
    % if defined("languages"):
    <div class="text"><strong>Languages:</strong> {{ languages }}</div>
    % end
    % if defined("challenge"):
    <div class="text"><strong>Challenge:</strong> {{ challenge }}</div>
    % end
    <div class="red-bar"><img class="red-bar-img" src="/static/img/stat-block-header-bar.svg"></div>
    % if defined("special_abilities"):
    <div class="text-black">
        {{! special_abilities }}
    </div>
    % end
    % if defined("actions"):
    <h2 class="actions-header">Actions</h2>
    <div class="text-black">
        {{! actions }}
    </div>
    % end
    % if defined("legendary_actions"):
    <h2 class="actions-header">Legendary Actions</h2>
    <div class="text-black">
        {{! legendary_actions }}
    </div>
    % end
    % if defined("reactions"):
    <h2 class="actions-header">Reactions</h2>
    <div class="text-black">
        {{! reactions }}
    </div>
    % end
    <div class="top-bottom-bar"></div>
</div>