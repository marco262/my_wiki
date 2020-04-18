<link rel="stylesheet" type="text/css" href="/static/css/calendar.css">
% from src.dragon_heist.calendar_builder import CalendarBuilder
% cb = CalendarBuilder()
<div class="month" id="kythorn">
    <img class="month-img" src="../static/img/kythorn.png" style="width: 1400px;">
    {{ cb.day(5, "\nMet at\nYawning\nPortal") }}
    {{ cb.day(6, "\nSaved\nRenaer") }}
    {{ cb.day(7, "\nSaved\nFloon") }}
    {{ cb.day(8, "\nAcquired\nTS Manor") }}
    {{ cb.day(10, "\nSeance\nfor Lif") }}
    {{ cb.day(12, "\nZhent\nMission") }}
    {{ cb.day(13, "\nBorrowed money\nBought suit") }}
    {{ cb.day(19, "\nOpera") }}
    {{ cb.day(22, "\nMaxeene") }}
    {{ cb.day(26, "\nEmbric attacked") }}
    {{ cb.day(27, "\nJoined DR") }}
    {{ cb.day(30, "\nHouse-\nwarming\nParty") }}
</div>
<div class="month" id="flamerule">
    <img class="month-img" src="../static/img/flamerule.png" style="width: 1400px;">
    {{ cb.day(23, "\nFireball!") }}
    {{ cb.day(24, "\nMorgue trip", current_day=True) }}
</div>
<h1>Festival Day: Midsummer</h1>
<div class="month" id="eleasis">
    <img class="month-img" src="../static/img/eleasis.png" style="width: 1400px;">
</div>
<div class="month" id="elient">
    <img class="month-img" src="../static/img/elient.png" style="width: 1400px;">
    {{ cb.day(28, "\nOwe Istrid\nHorn 220gp") }}
</div>

<h1>Festival Day: High Harvest</h1>