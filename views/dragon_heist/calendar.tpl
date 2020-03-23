<link rel="stylesheet" type="text/css" href="/static/css/calendar.css">
% from src.dragon_heist.calendar_builder import CalendarBuilder
% cb = CalendarBuilder(150, 121)
<div class="month" id="kythorn">
    <img class="month-img" src="../static/img/kythorn.png" style="width: 1400px;">
    {{ cb.day(5, "\nMet at\nYawning\nPortal") }}
    {{ cb.day(6, "\nSaved\nRenaer") }}
    {{ cb.day(7, "\nSaved\nFloon") }}
    {{ cb.day(8, "\nAcquired\nTS Manor") }}
    {{ cb.day(10, "\nSeance\nfor Lif") }}
    {{ cb.day(12, "\nZhent\nMission") }}
    {{ cb.day(13, "\nBorrowed money\nBought suit", current_day=True) }}
    {{ cb.day(19, "\nOpera") }}
    {{ cb.day(30, "\nHouse-\nwarming\nParty") }}
</div>


# 13th of Elient, they owe Istrid Horn 220gp