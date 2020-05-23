<link rel="stylesheet" type="text/css" href="/static/css/calendar.css">
% from src.dragon_heist.calendar_builder import CalendarBuilder
% cb = CalendarBuilder()
<div class="month" id="kythorn">
    <img class="month-img" src="../static/img/kythorn.png" style="width: 1400px;">
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
<div class="month" id="flamerule">
    <img class="month-img" src="../static/img/flamerule.png" style="width: 1400px;">
    {{ cb.day(23, "Fireball!") }}
    {{ cb.day(24, "Morgue trip") }}
    {{ cb.day(26, "Delivered Potions / Met Zardoz Zord") }}
    {{ cb.day(27, "Searched North Ward") }}
    {{ cb.day(28, "Tea with Tommasin Gralhund") }}
    {{ cb.day(29, "More tea with Tommasin Gralhund") }}
    {{ cb.day(30, "Tea and Violence") }}
</div>
<h1>Festival Day: Midsummer</h1>
<div class="month" id="eleasis">
    <img class="month-img" src="../static/img/eleasis.png" style="width: 1400px;">
</div>
<div class="month" id="elient">
    <img class="month-img" src="../static/img/elient.png" style="width: 1400px;">
    {{ cb.day(28, "Owe Istrid Horn 220gp") }}
</div>

<h1>Festival Day: High Harvest</h1>