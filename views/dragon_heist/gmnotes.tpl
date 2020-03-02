% include("common/header.tpl", title="Dragon Heist GM Notes")
<h1>Dragon Heist GM Notes</h1>

<ul>
    % for note in notes:
        <li><a href="{{ note[1] }}">{{ note[0] }}</a></li>
    % end
</ul>

<h3>Images:</h3>
<ul>
    % for image in images:
        <li><a href="{{ image[1] }}" target="popup" onclick="window.open('{{ image[1] }}','popup','width=600,height=600', menubar=yes); return false;">
            {{ image[0] }}
        </a></li>
    % end
</ul>

<h3>Friendly NPCs:</h3>
<ul>
    % for image in friendly_npcs_1:
        <li><a href="{{ image[1] }}" target="popup" onclick="window.open('{{ image[1] }}','popup','width=600,height=600', menubar=yes); return false;">
            {{ image[0] }}
        </a></li>
    % end
</ul>

<h3>Trollskull Alley NPCs:</h3>
<ul>
    % for image in trollskull_alley_npcs:
        <li><a href="{{ image[1] }}" target="popup" onclick="window.open('{{ image[1] }}','popup','width=600,height=600', menubar=yes); return false;">
            {{ image[0] }}
        </a></li>
    % end
</ul>

<h3>Guild NPCs:</h3>
<ul>
    % for image in guild_npcs:
        <li><a href="{{ image[1] }}" target="popup" onclick="window.open('{{ image[1] }}','popup','width=600,height=600', menubar=yes); return false;">
            {{ image[0] }}
        </a></li>
    % end
</ul>

<h3>Faction NPCs:</h3>
<h4>Force Grey</h4>
<ul>
    % for image in force_grey_npcs:
        <li><a href="{{ image[1] }}" target="popup" onclick="window.open('{{ image[1] }}','popup','width=600,height=600', menubar=yes); return false;">
            {{ image[0] }}
        </a></li>
    % end
</ul>

<h4>Harpers</h4>
<ul>
    % for image in harpers_npcs:
        <li><a href="{{ image[1] }}" target="popup" onclick="window.open('{{ image[1] }}','popup','width=600,height=600', menubar=yes); return false;">
            {{ image[0] }}
        </a></li>
    % end
</ul>

<h4>Lords' Alliance</h4>
<ul>
    % for image in lords_alliance_npcs:
        <li><a href="{{ image[1] }}" target="popup" onclick="window.open('{{ image[1] }}','popup','width=600,height=600', menubar=yes); return false;">
            {{ image[0] }}
        </a></li>
    % end
</ul>

<h4>Order of the Gauntlet</h4>
<ul>
    % for image in order_of_the_gauntlet_npcs:
        <li><a href="{{ image[1] }}" target="popup" onclick="window.open('{{ image[1] }}','popup','width=600,height=600', menubar=yes); return false;">
            {{ image[0] }}
        </a></li>
    % end
</ul>

<h4>Zhentarim</h4>
<ul>
    % for image in zhentarim_npcs:
        <li><a href="{{ image[1] }}" target="popup" onclick="window.open('{{ image[1] }}','popup','width=600,height=600', menubar=yes); return false;">
            {{ image[0] }}
        </a></li>
    % end
</ul>

<h3>Enemy NPCs:</h3>
<ul>
    % for image in enemy_npcs:
        <li><a href="{{ image[1] }}" target="popup" onclick="window.open('{{ image[1] }}','popup','width=600,height=600', menubar=yes); return false;">
            {{ image[0] }}
        </a></li>
    % end
</ul>

% include("common/footer.tpl")