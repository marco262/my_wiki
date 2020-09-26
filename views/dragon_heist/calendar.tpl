<link rel="stylesheet" type="text/css" href="/static/css/calendar.css">

<h2>Current Year: 1494 DR</h2>

<%
from src.dragon_heist.calendar_builder import CalendarBuilder
month_width = 1110
cb = CalendarBuilder(
    month_width=month_width,
    month_height=month_width * 0.4365,
    top_start=0.2422,
    left_start=0.0714,
    day_width=0.08595,
    day_height=0.2055
)
%>
<div class="month" id="kythorn">
    <img class="month-img" src="/static/img/kythorn.png">
    {{ cb.day(5, "Met at Yawning Portal") }}
    {{ cb.day(6, "Saved Renaer") }}
    {{ cb.day(7, "Saved Floon") }}
    {{ cb.day(8, "Acquired TS Manor") }}
    {{ cb.day(10, "Seance for Lif") }}
    {{ cb.day(12, "Zhent Mission") }}
    {{ cb.day(13, "Borrowed money / Bought suit") }}
    {{ cb.day(19, "Opera") }}
    {{ cb.day(22, "Maxeene") }}
    {{ cb.day(26, "Embric attacked") }}
    {{ cb.day(27, "Joined DR") }}
    {{ cb.day(30, "House-warming Party") }}
</div>  
<span class="visual-aid-link" title="iframe|/dragon_heist/calendar#kythorn">Send to Visual Aid</span>

<div class="month" id="flamerule">
    <img class="month-img" src="/static/img/flamerule.png">
    {{ cb.add_recurring() }}
    {{ cb.day(23, "Fireball!") }}
    {{ cb.day(24, "Morgue trip") }}
    {{ cb.day(26, "Delivered Potions / Met Zardoz Zord") }}
    {{ cb.day(27, "Searched North Ward") }}
    {{ cb.day(28, "Tea with Tommasin Gralhund") }}
    {{ cb.day(29, "More tea with Tommasin Gralhund") }}
    {{ cb.day(30, "Tea and Violence") }}
</div>  
<span class="visual-aid-link" title="iframe|/dragon_heist/calendar#flamerule">Send to Visual Aid</span>

<h1>Festival Day: Midsummer</h1>

* Fought gazer in bookstore

<div class="month" id="eleasis">
    <img class="month-img" src="/static/img/eleasis.png">
    {{ cb.add_recurring() }}
    {{ cb.day(1, "Took in Istrid Horn") }}
    {{ cb.day(2, "Nimblewright") }}
    {{ cb.day(3, "Met Grinda / Mausoleum") }}
    {{ cb.day(4, "Mommy issues uwu") }}
    {{ cb.day(5, "") }}
    {{ cb.day(6, "Home Security with Ulkoria") }}
    {{ cb.day(7, "Bringing Dasher Home / Windmill") }}
    {{ cb.day(8, "Wig Shopping") }}
    {{ cb.day(9, "Assault on Trollskull") }}
    {{ cb.day(10, "Cabin in the Woods") }}
    {{ cb.day(11, "Istrid Horn owes party 180gp / Play!") }}
    {{ cb.day(12, "Sewer Plague") }}
    {{ cb.day(13, "Mark Dragonscale") }}
    {{ cb.day(14, "Dragon Heist!", current_day=True) }}
    {{ cb.day(16, "Remalia's Party") }}
</div>  
<span class="visual-aid-link" title="iframe|/dragon_heist/calendar#eleasis">Send to Visual Aid</span>

<div class="month" id="elient">
    <img class="month-img" src="/static/img/elient.png">
    {{ cb.add_recurring() }}
    {{ cb.day(1, "Skeemo Sting") }}
</div>  
<span class="visual-aid-link" title="iframe|/dragon_heist/calendar#elient">Send to Visual Aid</span>

<h1>Festival Day: High Harvest</h1>

<hr>

<a href="https://natural20.co.uk/wp-content/uploads/2019/06/calendar_natural20.pdf">Full Calendar PDF</a>

<script type="module">
    import {init_links} from "/js/dragon_heist/gm_notes.js";
    init_links();
</script>
