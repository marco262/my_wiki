% from data.onednd.enums import classes, spell_classes

<div id="index-container" markdown="1">

<div class="index-column" markdown="1">

## Races

### Common Races

* [[[race:Dwarf]]]
* [[[race:Elf]]]
* [[[race:Gnome]]]
* [[[race:Halfling]]]
* [[[race:Human]]]

### Uncommon Races

* [[[race:Ardling]]]
* [[[race:Dragonborn]]]
* [[[race:Goliath]]]
* [[[race:Orc]]]
* [[[race:Tiefling]]]

</div>

<div class="index-column" markdown="1">

## Classes

[[[general:Classes|Classes Overview]]]

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

[Spell Filter](/onednd/spell_filter)

### Spell Lists

% for c in spell_classes:
* [{{c.title()}} Spells](/onednd/spell_list/{{c}})
% end

</div>

<div class="index-column" markdown="1">

## Character Information

* [[[advancement:Character Generation]]]
* [[[advancement:Feats]]]

## Equipment

* [[[general:equipment#weapons|Weapons]]]
* [[[general:equipment#adventuring-gear|Adventuring Gear]]]

## System Info

[[[general:Rules Glossary]]]

</div>

</div>
