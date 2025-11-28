% from data.dnd.enums import classes, spell_classes

<div id="index-container" markdown="1">

<div class="index-column" markdown="1">

## Races

### Common Races

* [[[advancement:Races#Dwarf]]]
* [[[advancement:Races#Elf]]]
* [[[advancement:Races#Gnome]]]
* [[[advancement:Races#Halfling]]]
* [[[advancement:Races#Human]]]

### Uncommon Races

* [[[advancement:Races#Aasimar]]]
* [[[advancement:Races#Dragonborn]]]
* [[[advancement:Races#Goliath]]]
* [[[advancement:Races#Orc]]]
* [[[advancement:Races#Tiefling]]]

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
