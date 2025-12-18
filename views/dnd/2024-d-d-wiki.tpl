% from data.dnd.enums import classes, spell_classes

<div id="index-container" markdown="1">

<div class="index-column" markdown="1">

## Races

### Common Races

* [[[race:Dwarf]]]
* [[[race:Elf]]]
* [[[race:Halfling]]]
* [[[race:Human]]]

### Uncommon Races

* [[[race:Aasimar]]]
* [[[race:Dragonborn]]]
* [[[race:Gnome]]]
* [[[race:Goliath]]]
* [[[race:Orc]]]
* [[[race:Tiefling]]]

</div>

<div class="index-column" markdown="1">

## Classes

[[[advancement:Classes|Classes Overview]]]

% for c in classes:
% if c == "Artificer":
* [Artificer](/dnd/class/Artificer)
% else:
* [[[class:{{c.title()}}]]]
% end
% end

</div>

<div class="index-column" markdown="1">

## Spells

[Spell Filter](/dnd/spell_filter)

### Spell Lists

% for c in spell_classes:
* [{{c.title()}} Spells](/dnd/spell_list/{{c}})
% end

</div>

<div class="index-column" markdown="1">

## Character Information

* [[[advancement:Creating a Character]]]
* [[[advancement:Character Origins]]]
    * [[[advancement:Races]]]
    * [[[advancement:Backgrounds]]]
* [[[advancement:Feats]]]

## Equipment

* [[[general:equipment#Coins]]]
* [[[general:equipment#Weapons]]]
* [[[general:equipment#Armor]]]
* [[[general:equipment#Tools]]]
* [[[general:equipment#Adventuring Gear]]]
* [[[general:equipment#Mounts and Vehicles]]]
* [[[general:equipment#Services]]]
* [[[general:equipment#Magic Items]]]
* [[[general:equipment#Crafting Equipment]]]

## System Info

* [[[general:Playing the Game]]]
* [[[general:Rules Glossary]]]
* [[[general:Spellcasting Rules]]]

</div>

</div>
