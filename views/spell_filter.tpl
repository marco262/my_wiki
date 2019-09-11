% include("header.tpl")

<title>Private 5e Wiki - {{title}}</title>

<h1>{{title}}</h1>

% if get("level_cantrip"):
<h2>Cantrips</h2>
% include(table_template, spells=level_cantrip)

% end
% if get("level_1"):
<h2>1st Level</h2>
% include(table_template, spells=level_1)

% end
% if get("level_2"):
<h2>2nd Level</h2>
% include(table_template, spells=level_2)

% end
% if get("level_3"):
<h2>3rd Level</h2>
% include(table_template, spells=level_3)

% end
% if get("level_4"):
<h2>4th Level</h2>
% include(table_template, spells=level_4)

% end
% if get("level_5"):
<h2>5th Level</h2>
% include(table_template, spells=level_5)

% end
% if get("level_6"):
<h2>6th Level</h2>
% include(table_template, spells=level_6)

% end
% if get("level_7"):
<h2>7th Level</h2>
% include(table_template, spells=level_7)

% end
% if get("level_8"):
<h2>8th Level</h2>
% include(table_template, spells=level_8)

% end
% if get("level_9"):
<h2>9th Level</h2>
% include(table_template, spells=level_9)
% end

% include("footer.tpl")
