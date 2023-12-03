<!doctype html>
<html>
<!-- Blatantly stolen from https://dungeonetics.com/calendar/ -->
<!-- To change the events that show up on the calendar, edit the file `static/js/sandpoint/golarion.js` -->
<!-- Edit CustomCalendarData > holidaySet > holidays -->
<head>
	<meta charset="utf-8">
	<title>Heroes of Sandpoint Calendar</title>
    <script src="https://ajax.googleapis.com/ajax/libs/jquery/3.1.1/jquery.js"></script>
    <link href="/static/css/sandpoint/calendar_print.css" rel="stylesheet" type="text/css"/>
    <script src="/static/js/sandpoint/CustomCalendar.js"></script>
    <script src="/static/js/sandpoint/CustomCalendarView.js"></script>
    <script src="/static/js/sandpoint/golarion.js"></script>

    <script type="text/javascript">
$(document).ready(function(){
    let calendar_events = [];
    let defaults = {
        "lunar_period": 29.5,
        "first_full": 26,
        "founding_day": 1,
        "leap_interval": 8,
        "start_year": 4707,
        "start_month": 8,
        "start_dow": 1,
        "end_year": 4707,
        "end_month": 9,
    };
    let start_year = defaults.start_year;
    let start_month = defaults.start_month;
    let end_year = defaults.end_year;
    let end_month = defaults.end_month;
    let view, qs;

    //=========================================================================
    // Parse the query string and set initial options
    //=========================================================================
    // http://stackoverflow.com/questions/901115/how-can-i-get-query-string-values-in-javascript
    // BrunoLM (https://stackoverflow.com/users/340760)

    qs = (function(a) {
	    if (a === "") return {};
	    let b = {};
	    for (let i = 0; i < a.length; ++i)
	    {
	        let p=a[i].split('=', 2);
	        if (p.length === 1)
	            b[p[0]] = "";
	        else
	            b[p[0]] = decodeURIComponent(p[1].replace(/\+/g, " "));
	    }
	    return b;
	})(window.location.search.substr(1).split('&'));

    //=========================================================================
    // Initialize the calendar and the view
    //=========================================================================

    calendar = new CustomCalendar();
    calendar.Import(CustomCalendarData);
    view = new CustomCalendarView(calendar);

	//=========================================================================
	// Process incoming parameters
	//=========================================================================

	if ( 'calyear' in qs ) {
		let val = parseInt(qs.calyear);
		if ( ! isNaN(val) && val >= calendar.yearMin ) { year = val; }
	}

	if ( 'leap_interval' in qs ) {
		let intv = parseInt(qs.leap_interval);

		if ( ! isNaN(intv) ) {
			if ( intv === 0 ) {
				calendar.leapYearRuleSet.Clear();
			} else if ( intv > 0 ) {
				calendar.leapYearRuleSet.Item(0).Include(intv);
			}
        }
	}

    if ( 'lunarcycle' in qs ) {
		let period = parseFloat(qs.lunarcycle);

		if ( ! isNaN(period) ) {
			if ( period >= 4 ) {
				let ff = $("#firstfull");
				let moon = calendar.moonSet.Item(0);

				moon.Period(period);
				ff.spinner("option", "max", period);
				if ( ff.val() > period ) {
					ff.val(period);
					moon.firstFull = period;
				}
			}
		}
    }

    if ( 'firstfull' in qs ) {
        let dayN = parseFloat(qs.firstfull);

        if ( ! isNaN(dayN) ) {

			if ( dayN > 0 && dayN <= calendar.moonSet.Item(0).Period() ) {
				calendar.moonSet.Item(0).firstFull = dayN;
			}
        }
    }

    if ( 'founding_day_new' in qs ) {
        let v = parseInt(qs.founding_day_new);

        if ( ! isNaN(v) ) {
			if ( v >= 0 && v < calendar.weekdaySet.Size() ) calendar.foundingDay = v;
        }
    }

    if ( 'start_dow' in qs ) {
        let v =parseInt(qs.start_dow);
        if ( ! isNaN(v) ) {
			if ( v >= 0 && v < calendar.weekdaySet.Size() ) view.Config({ "startWeekOn": v });
        }
    }

	let render_calendars = function(view, start_year, start_month, end_year, end_month) {
        let year = start_year;
        let month = start_month;
        const num_months = calendar.monthSet.Size();

        let monthlyCalendars = $("#monthly_calendars");

        while (true) {
            let div_id = `monthly-calendar-${year}-${month + 1}`;
            let div = $(`<div id="${div_id}"></div>`).addClass("print_container large_calendar");
            div.append(view.RenderMonth(month, year, { "render_day": callback_month_day }));
            monthlyCalendars.append(div);
            // Advance month, go to new year if needed, and end at end_year/end_month
            month++;
            if (month >= num_months) {
                year++;
                month = 0;
            }
            if (year > end_year) break;
            if (year === end_year && month > end_month) break;
        }
    };

    let callback_month_day = function(view, divDay, divDayNum, egroups) {
        let divEvent = document.createElement('div');

        divEvent.setAttribute('class', 'day_event day_cell');

        divDay.appendChild(divDayNum);
        if ( view.EventTypeMoonPhase in egroups ) divDay.appendChild(egroups[view.EventTypeMoonPhase]);
        if ( view.EventTypeSeason in egroups ) divDay.appendChild(egroups[view.EventTypeSeason]);

        if ( view.EventTypeFullMoon in egroups ) divEvent.appendChild(egroups[view.EventTypeFullMoon]);
        if ( view.EventTypeHoliday in egroups ) divEvent.appendChild(egroups[view.EventTypeHoliday]);
        if ( view.EventTypeUser in egroups ) divEvent.appendChild(egroups[view.EventTypeUser]);

        divDay.appendChild(divEvent);
    };

	render_calendars(view, start_year, start_month, end_year, end_month);

});
</script>
</head>

<body>
	<div id="monthly_calendars"></div>
</body>