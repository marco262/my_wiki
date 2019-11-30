% include("header.tpl", title=title)
<h1>Mutants</h1>
% from data.numenera.enums import beneficial_mutations

<p>Some characters have been affected by mutation. Mutants are not visitants. They are humans who have changed over time, either through natural forces of evolution or through an unnatural manipulation --  intentional or not -- to an individual or his ancestors. Unnatural manipulation could mean exposure to mutagens, the result of genetic engineering, or the result of genetic engineering gone wrong.</p>

<p>In the Ninth World, mutants sometimes band together. Those with hideous deformities face discrimination and derision. Some are outcasts, and others are revered, flaunting their mutations as a sign of superiority, power, and influence. Their mutations are seen as a blessing, not a curse. Some people believe them to be divine.</p>

<p>There are five categories of mutations. Two of them -- beneficial mutations and powerful mutations -- bring about changes that are neither physically obvious nor extraordinary. Powerful mutations are more potent than beneficial ones. Harmful mutations are physical changes that are usually grotesque and somewhat debilitating. The fourth category, distinctive mutations, also provides significant abilities, but they mark the character as an obvious mutant. Last, cosmetic mutations bring no special capabilities at all and are merely cosmetic (although sometimes dramatically so).</p>

<p>In theory, there is a sixth category that might be called crippling mutations, but characters never have this kind of mutation. Mutants with crippling mutations might be born without limbs, with barely functional lungs, without most of their brain, and so on. Such mutations prevent a character from being viable.</p>

<p>If you want to play a mutant, you have special abilities, but they come at a cost. In lieu of a descriptor -- or rather, by choosing <em>mutant</em> as your descriptor -- you gain two beneficial mutations. If you opt to take a harmful mutation as well, you can have three beneficial mutations, or one powerful mutation, or one powerful and distinctive mutation. You can also have from zero to four distinctive mutations, which is completely up to you. Mutations are always rolled randomly, although the player and GM can work together to ensure that the resulting character is one that the player wants to play.</p>

<p>Unlike abilities gained from most other sources, mutations that affect the difficulty of tasks are assets, not skills. That means any step changes from a mutation are in addition to any step changes you might have from a skill.</p>

<h2>Beneficial Mutations</h2>

<p>The following mutations do not require any visible changes or distinctions in the character. In other words, people who have these mutations are not obviously recognized as mutants. Using beneficial mutations never costs stat Pool points and never requires an action to "activate".</p>

% for m in beneficial_mutations:
%   first_num = "{:>02}".format("00" if m[0] == 100 else m[0])
%   second_num = "-{:>02}".format("00" if m[1] == 100 else m[1]) if m[1] is not None else ""
<strong>{{first_num}}{{second_num}} {{m[2]}}:</strong> {{m[3]}}<br />
% end

% include("footer.tpl")