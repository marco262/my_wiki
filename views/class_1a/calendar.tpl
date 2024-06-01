<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <title>Heroes of Sandpoint Calendar</title>
    <link href="/static/css/sandpoint/calendar.css" rel="stylesheet" type="text/css"/>
</head>
<body>

% for month_name, weeks in months.items():
<table class="month" id="{{ month_name.lower().replace(" ", "_").replace(",", "") }}">
    <tr>
        <td class="month-header" colspan="7">{{ month_name }}</td>
    </tr>
    <tr class="weekday-row">
        <td>Sunday</td>
        <td>Moonday</td>
        <td>Toilday</td>
        <td>Wealday</td>
        <td>Oathday</td>
        <td>Fireday</td>
        <td>Starday</td>
    </tr>
    % for days in weeks:
    <tr class="week">
        % for day in days:
        % disabled = "disabled" if not month_name.startswith(day["month"]) else ""
        <td class="day {{ disabled }}">
            <div class="day-number">{{ day["number"] }}</div>
            % if "moon" in day:
            <div class="moon {{ day["moon"] }}"></div>
            % end
            % if day["events"]:
            <div class="events">
                <div class="events-inner">
                    % for event in day["events"]:
                    <div class="{{ event.get("type", "event") }}">{{ event.get("name") }}</div>
                    % end
                </div>
            </div>
            % end
        </td>
        % end
    </tr>
    % end
</table>
% end

</body>
</html>