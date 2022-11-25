% from data.onednd.enums import races, classes, spell_classes

[[div id="index-container"]]

[[div class="index-column"]]

## Races

[[[general:Races|Races Overview]]]

% for r in races:
* [[[race:{{r.title()}}]]]
% end

[[/div]]

[[div class="index-column"]]

## Published Classes

[[[general:Classes|Classes Overview]]]

% for c in classes:
* [[[class:{{c.title()}}]]]
% end

[[/div]]

[[div class="index-column"]]

## Spells

## Class Spell Lists

% for c in spell_classes:
* [{{c.title()}} Spells](/onednd/class_spell_list/{{c}}/true)
% end

[[/div]]

[[div class="index-column"]]

## Character Information

* [[[general:Backgrounds]]]
* [[[advancement:Feats]]]

[[/div]]

[[div class="index-column"]]

## Equipment

## Magic Items

[[/div]]

[[/div]]
