% rebase("common/base.tpl", title=title)

% from src.common.utils import ordinal

% if level == "0":
% fmt = "{school} Cantrip ({spell_lists})"
% else:
% fmt = "{level}-Level {school} Spell ({spell_lists})"
% end
<p>{{fmt.format(level=ordinal(level), school=school.title(), spell_lists=", ".join(spell_lists))}}</p>

<p>
<strong>Casting Time:</strong> {{casting_time}}<br />
<strong>Range:</strong> {{range}}<br />
<strong>Components:</strong> {{", ".join(components)}}{{" (" + material + ")" if "M" in components else ""}}<br />
<strong>Duration:</strong> {{duration}}</p>

{{!description_md}}
% if defined('at_higher_levels'):
<p><strong>At Higher Levels:</strong> {{at_higher_levels}}</p>

% end
% if defined('cantrip_upgrade'):
<p><strong>Cantrip Upgrade:</strong> {{cantrip_upgrade}}</p>

% end
% if defined('at_higher_levels_homebrew'):
<div class="homebrew-note"><strong>At Higher Levels (homebrew):</strong> {{at_higher_levels_homebrew}}</div>

% end
<hr class="no-float">
<p><em>
    % if defined('source_link'):
    Source: <a href="{{ source_link }}">{{ source }}</a>
    % else:
    Source: {{ source }}
    % end
</em></p>
