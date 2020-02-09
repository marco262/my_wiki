<%
from data.numenera.enums import (beneficial_mutations, harmful_mutations, powerful_mutations, distinctive_mutations,
                                 cosmetic_mutations)
from math import ceil
%>

Some characters have been affected by mutation. Mutants are not visitants. They are humans who have changed over time, either through natural forces of evolution or through an unnatural manipulation --  intentional or not -- to an individual or his ancestors. Unnatural manipulation could mean exposure to mutagens, the result of genetic engineering, or the result of genetic engineering gone wrong.

In the Ninth World, mutants sometimes band together. Those with hideous deformities face discrimination and derision. Some are outcasts, and others are revered, flaunting their mutations as a sign of superiority, power, and influence. Their mutations are seen as a blessing, not a curse. Some people believe them to be divine.

There are five categories of mutations. Two of them -- beneficial mutations and powerful mutations -- bring about changes that are neither physically obvious nor extraordinary. Powerful mutations are more potent than beneficial ones. Harmful mutations are physical changes that are usually grotesque and somewhat debilitating. The fourth category, distinctive mutations, also provides significant abilities, but they mark the character as an obvious mutant. Last, cosmetic mutations bring no special capabilities at all and are merely cosmetic (although sometimes dramatically so).

In theory, there is a sixth category that might be called crippling mutations, but characters never have this kind of mutation. Mutants with crippling mutations might be born without limbs, with barely functional lungs, without most of their brain, and so on. Such mutations prevent a character from being viable.

If you want to play a mutant, you have special abilities, but they come at a cost. In lieu of a descriptor -- or rather, by choosing *mutant* as your descriptor -- you gain two beneficial mutations. If you opt to take a harmful mutation as well, you can have three beneficial mutations, or one powerful mutation, or one powerful and distinctive mutation. You can also have from zero to four distinctive mutations, which is completely up to you. Mutations are always rolled randomly, although the player and GM can work together to ensure that the resulting character is one that the player wants to play.

Unlike abilities gained from most other sources, mutations that affect the difficulty of tasks are assets, not skills. That means any step changes from a mutation are in addition to any step changes you might have from a skill.

## Beneficial Mutations

The following mutations do not require any visible changes or distinctions in the character. In other words, people who have these mutations are not obviously recognized as mutants. Using beneficial mutations never costs stat Pool points and never requires an action to "activate".

% for m in beneficial_mutations:
%   first_num = "{:>02}".format("00" if m[0] == 100 else m[0])
%   second_num = "-{:>02}".format("00" if m[1] == 100 else m[1]) if m[1] is not None else ""
**{{first_num}}{{second_num}} {{m[2]}}:** {{m[3]}}<br />
% end

## Harmful Mutations

Unless noted otherwise, the following mutations are visible, obvious, and grotesque. They offer no benefits, only drawbacks.

% for m in harmful_mutations:
%   first_num = "{:>02}".format("00" if m[0] == 100 else m[0])
%   second_num = "-{:>02}".format("00" if m[1] == 100 else m[1]) if m[1] is not None else ""
**{{first_num}}{{second_num}} {{m[2]}}:** {{m[3]}}<br />
% end

## Powerful Mutations

The following mutations do not require any visible changes in the character until used. People who have these mutations are not obviously recognized as mutants if they don't use their powers. Using some of these mutations costs stat Pool points. Some are actions.

% for m in powerful_mutations:
%   first_num = "{:>02}".format("00" if m[0] == 100 else m[0])
%   second_num = "-{:>02}".format("00" if m[1] == 100 else m[1]) if m[1] is not None else ""
**{{first_num}}{{second_num}} {{m[2]}}:** {{m[3]}}<br />
% end

## Distinctive Mutations

The following mutations involve dramatic physical changes to the character's appearance. People who have these mutations are always recognized as mutants. Using some of these mutations costs stat Pool points. Some are actions.

% for m in distinctive_mutations:
%   first_num = "{:>02}".format("00" if m[0] == 100 else m[0])
%   second_num = "-{:>02}".format("00" if m[1] == 100 else m[1]) if m[1] is not None else ""
**{{first_num}}{{second_num}} {{m[2]}}:** {{m[3]}}<br />
% end

## Cosmetic Mutations

Cosmetic mutations affect nothing but the appearance of a character. None is so pronounced as to make a character decidedly more or less attractive. They are simply distinguishing alterations.

<%
pivot = ceil(len(cosmetic_mutations) / 3)
m1 = cosmetic_mutations[:pivot]
m2 = cosmetic_mutations[pivot:pivot * 2]
m3 = cosmetic_mutations[pivot * 2:]
for i in range(len(m1)):
    first_num_1 = "{:>02}".format("00" if m1[i][0] == 100 else m1[i][0])
    second_num_1 = "-{:>02}".format("00" if m1[i][1] == 100 else m1[i][1]) if m1[i][1] is not None else ""
    text_1 = m1[i][2]
    first_num_2 = "{:>02}".format("00" if m2[i][0] == 100 else m2[i][0])
    second_num_2 = "-{:>02}".format("00" if m2[i][1] == 100 else m2[i][1]) if m2[i][1] is not None else ""
    text_2 = m2[i][2]
    if len(m3) > i:
        first_num_3 = "{:>02}".format("00" if m3[i][0] == 100 else m3[i][0])
        second_num_3 = "-{:>02}".format("00" if m3[i][1] == 100 else m3[i][1]) if m3[i][1] is not None else ""
        text_3 = m3[i][2]
    else:
        first_num_3 = "&nbsp;"
        second_num_3 = ""
        text_3 = ""
    end
%>
|| **{{first_num_1 + second_num_1}}** || {{text_1}} || **{{first_num_2 + second_num_2}}** || {{text_2}} || **{{first_num_3 + second_num_3}}** || {{text_3}} ||
% end