% from data.dnd.enums import classes, spell_classes

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

[Spell Filter](/dnd/spell_filter)

### Spell Lists

% for c in spell_classes:
* [{{c.title()}} Spells](/dnd/spell_list/{{c}})
% end

</div>

<div class="index-column" markdown="1">

## Character Information

* [[[advancement:Creating a Character]]]
* [[[advancement:Character Generation]]]
    * [[[advancement:Character Generation#backgrounds|Backgrounds]]]
    * [[[advancement:Character Generation#languages|Languages]]]
* [[[advancement:Feats]]]

## Equipment

* [[[general:equipment#armor-and-shields|Armor and Shields]]]
* [[[general:equipment#weapons|Weapons]]]
* [[[general:equipment#adventuring-gear|Adventuring Gear]]]
* [[[general:equipment#tools|Tools]]]
* [[[general:equipment#mounts-and-vehicles|Mounts and Vehicles]]]
* [[[general:equipment#trade-goods|Trade Goods]]]
* [[[general:equipment#expenses|Expenses]]]
* [[[general:equipment#trinkets|Trinkets]]]

## System Info

* [[[general:Playing the Game]]]
* [[[general:Rules Glossary]]]

</div>

</div>
