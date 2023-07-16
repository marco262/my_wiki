let CustomCalendarView = (function(cal) {
    "use strict";

    let CustomCalendarView = function(cal) {
        this.moonRenderSize = 18;

        this.EventTypeHoliday = CalendarEventTypeHoliday;
        this.EventTypeMoonPhase = CalendarEventTypeMoonPhase;
        this.EventTypeSeason = CalendarEventTypeSeason;
        this.EventTypeFullMoon = CalendarEventTypeFullMoon;
        this.EventTypeUser = CalendarEventTypeUser;

        let calendar = cal;
        let startWeekOn = 0;
        let classPrefix = "ccal";
        let yearThis = new YearData(calendar);
        let yearPrev = null;
        let yearNext = null;

        document.documentElement.style.setProperty("--weekdays", calendar.weekdaySet.Size());

        // Derived states

        // Convenience method to append class prefix to a list of class names

        let Classes = function(obj) {
            "use strict";

            if ( typeof obj === "string" ) return classPrefix+"_"+obj;

            return obj.map(function(c) { return classPrefix+"_"+c; }).join(" ");
        };

        // Get/set configuration options. Either as an object, or a key/value

        this.Config = function(opt, value) {
            "use strict";

            if ( opt === null || opt === undefined ) return null;
            if ( typeof opt === "object" ) {
                let options = {};

                Object.keys(opt).forEach( function(k) {
                    options[k]= ConfigOption(k, opt[k]);
                });
                return options;
            } else if ( typeof opt === "string" ) {
                return ConfigOption(opt, value);
            }

            return null;
        };

        let ConfigName = function(obj, param, options)
        {
            "use strict";

            if ( obj === null ) return null;
            if ( options === null || typeof options !== "object" ) return obj.name;

            if ( param in options ) {
                if ( options[param] === "abbrev" ) {
                    return obj.nameAbbrev;
                } else if ( options[param] === "short" ) {
                    return obj.nameShort;
                }
            }
            return obj.name;
        };

        let ConfigOption = function(key, val) {
            "use strict";

            if ( key === null || key === undefined || typeof key !== "string" ) return null;

            // Which day to start the week on when rendering

            if ( key === "startWeekOn" ) {
                if ( val !== undefined && typeof val === "number" ) {
                    val = parseInt(val);

                    if ( val !== "NaN" && val >= 0 || val < cal.weekdaySet.Size()) startWeekOn = Math.floor(val);
                }

                return startWeekOn;
            }

            // UI class name prefix to use

            if ( key === "classPrefix" ) {
                if ( val !== undefined && typeof val === "string" ) {
                    classPrefix = val;
                }

                return classPrefix;
            }
        };

        // Make a unique DOM element ID for each calendar element

        this.DomID = function(what, id) {
            return "cal_"+calendar.id+"_"+what+"_"+id;
        };


        // Render events to the calendar.

        this.RenderEvents = function(dayN, cells) {
            "use strict";

            let events;
            let view = this;
            let egroups = {};

            if ( ! yearThis.calendarEvents.HasEventsOn(dayN) ) return egroups;
            events = yearThis.calendarEvents.EventsOn(dayN);

            for (let i = 0; i< events.length; ++i) {
                let e = events[i];
                let typeName = CalendarEventTypes[e.type.toString()];
                let divEvent = document.createElement("div");

                divEvent.setAttribute("class", Classes(["event", typeName+"_event"]));

                if ( ! egroups[e.type] ) {
                    let divGroup = document.createElement("div");

                    divGroup.setAttribute('class', Classes([ "event_group", typeName+"_event_group" ]));
                    egroups[e.type]= divGroup;
                }

                if ( e.type === CalendarEventTypeSeason ) {
                    divEvent.innerHTML = e.name;
                } else if ( e.type === CalendarEventTypeMoonPhase ) {
                    let cnv = document.createElement('canvas');
                    let span = document.createElement('span');
                    let ctx = cnv.getContext("2d");
                    let phase = e.data;
                    let moon = e.object;
                    let sz = this.moonRenderSize/2;

                    cnv.setAttribute('width', this.moonRenderSize+'px');
                    cnv.setAttribute('height', this.moonRenderSize+'px');

                    ctx.beginPath();
                    if ( phase === moon.moonPhases.new_moon ) {
                        ctx.fillStyle=moon.ShadowColor();
                        ctx.arc(sz, sz, sz, 0, 2*Math.PI);
                    } else if ( phase === moon.moonPhases.full_moon ) {
                        ctx.fillStyle = moon.Color();
                        ctx.arc(sz, sz, sz, 0, 2*Math.PI);
                    } else if ( phase === moon.moonPhases.last_quarter ) {
                        ctx.fillStyle = moon.Color();
                        ctx.arc(sz, sz, sz, 0.5*Math.PI, 1.5*Math.PI);
                        ctx.fill();
                        ctx.beginPath();
                        ctx.fillStyle = moon.ShadowColor();
                        ctx.arc(sz, sz, sz, 1.5*Math.PI, 0.5*Math.PI);
                    } else if ( phase === moon.moonPhases.first_quarter ) {
                        ctx.fillStyle = moon.ShadowColor();
                        ctx.arc(sz, sz, sz, 0.5*Math.PI, 1.5*Math.PI);
                        ctx.fill();
                        ctx.beginPath();
                        ctx.fillStyle = moon.Color();
                        ctx.arc(sz, sz, sz, 1.5*Math.PI, 0.5*Math.PI);
                    }
                    span.innerHTML = cnv.innerHTML = moon.name+" "+moon.phaseNames[phase];
                    span.setAttribute("class", Classes("moon_phase"));
                    cnv.setAttribute("title", cnv.innerHTML);
                    ctx.fill();
                    divEvent.appendChild(cnv);
                    divEvent.appendChild(span);
                } else if ( e.type === CalendarEventTypeFullMoon ) {
                    divEvent.innerHTML = e.name;
                } else if ( e.type === CalendarEventTypeHoliday ) {
                    let divHoliday = document.createElement('div');
                    let hday = e.object;
                    let classlist = ['event_holiday'];
                    let title = e.name;
                    let span;

                    if ( hday.category !== null ) {
                        classlist.push('event_category_'+hday.category);
                        title += '\nHoliday category: '+hday.category;
                    }
                    if ( hday.observedBy !== null ) {
                        span = document.createElement('span');
                        span.setAttribute('class', Classes("holiday_observedby"));
                        classlist.push('holiday_observedby_'+hday.observedBy);
                        title += '\nObserved by: '+hday.observedBy;
                        span.innerHTML = "&mdash;" + hday.observedBy;
                    }
                    if ( title.length ) divHoliday.setAttribute('title', title);
                    divHoliday.setAttribute('class', Classes(classlist));
                    divHoliday.innerHTML = e.name;
                    if ( hday.observedBy !== null ) {
                        divHoliday.appendChild(span);
                    }
                    divEvent.appendChild(divHoliday);
                }

                egroups[e.type].appendChild(divEvent);
            }

            return egroups;
        };

        this.RenderMonth = function(monthidx, year, options) {
            "use strict";

            let name, month, elem, dayN, startDoW, startDayN, endDayN;
            let divCalendar, divMonthHeader, divDayHeader, divWeek, spanYear;
            let nWeekdays = calendar.weekdaySet.Size();
            let idprefix = "";

            divCalendar = document.createElement('div');
            divCalendar.setAttribute('class', classPrefix+'_calendar');

            if ( monthidx === undefined || year === undefined ||
                    monthidx < 0 || monthidx >= calendar.monthSet.Size() ||
                    year < calendar.yearMin ) return divCalendar;

            month = calendar.monthSet.Item(monthidx);
            year *= 1;
            monthidx *= 1;

            name = ConfigName(month, 'monthNameFormat', options);
            if ( "id_prefix" in options && typeof options.id_prefix === "string" ) {
				idprefix = options.id_prefix;
			}

            if ( yearThis.Year() !== year ) {
                yearThis.Derive(year);
            }

            if ( yearThis.Invalid() ) return divCalendar;

            divCalendar.setAttribute('id',  idprefix + this.DomID('month', month.id));
            divCalendar.setAttribute('data-xid', month.id);

            divMonthHeader = document.createElement('div');
            divMonthHeader.setAttribute('class', Classes(["calendar_row" , "month_header"]));
            spanYear = document.createElement('span');
            spanYear.setAttribute('class', 'calendar_year');
            spanYear.innerHTML = ", "+year+" "+calendar.era;
            divMonthHeader.innerHTML = name;
            divMonthHeader.appendChild(spanYear);
            divCalendar.appendChild(divMonthHeader);

            //divCalendar.appendChild(this.RenderWeekHeader());
            this.RenderWeekHeader(options).forEach(function (x) {
                divCalendar.appendChild(x);
            });

            // Get the day number for the start of the month, then get the
            // day of the week.

            startDayN = yearThis.MonthStartDayNumber(monthidx);
            endDayN = yearThis.MonthEndDayNumber(monthidx);
            startDoW = yearThis.DayOfWeek(startDayN);
            if ( startWeekOn > startDoW ) {
                dayN = startDayN - nWeekdays + (startWeekOn-startDoW);
            } else if ( startWeekOn < startDoW ) {
                dayN = startDayN - (startDoW - startWeekOn);
            } else {
                dayN = startDayN;
            }

            while ( dayN <= endDayN ) {
                let lastWeek = ( dayN+nWeekdays > endDayN );

                this.RenderWeek(dayN, monthidx, startDayN, endDayN, lastWeek, options).forEach(function(x) {
                    divCalendar.appendChild(x);
                });
                dayN += nWeekdays;
            }

            // Return our div

            return divCalendar;
        };

        this.RenderWeekHeader = function (options)
        {
            "use strict";
            let nweekdays = calendar.weekdaySet.Size();

            //let divDayHeader = document.createElement('div');
            let dayHeader = [];

            //divDayHeader.setAttribute('class', Classes(["calendar_row", "day_header_row"]));
            for (let i = 0; i< calendar.weekdaySet.Size(); ++i) {
                let idx = (startWeekOn+i)%nweekdays;
                let wday = calendar.weekdaySet.Item(idx);
                let divDay = document.createElement('div');
                let name=ConfigName(wday, 'weekdayNameFormat', options);

                if ( i === 0 ) {
                    divDay.setAttribute('class', Classes(["day", "day_name", "day_row_start"]));
                } else if ( i === (nweekdays-1) ) {
                    divDay.setAttribute('class', Classes(["day", "day_name", "day_row_end"]));
                } else {
                    divDay.setAttribute('class', Classes(["day", "day_name"]));
                }
                divDay.innerHTML = name;
                //divDayHeader.appendChild(divDay);
                dayHeader.push(divDay);
            }
            //return divDayHeader;
            return dayHeader;
        };

        this.RenderWeek = function(dayN, monthidx, startDayN, endDayN, lastWeek, options)
        {
            "use strict";

            //let divDayRow = document.createElement('div');
            let dayRow = [];
            let mday = dayN-startDayN;
            let wdays = calendar.weekdaySet.Size();
            let last_monthidx = calendar.monthSet.Size()-1;

            // divDayRow.setAttribute('class', Classes(["calendar_row", "day_row"]));

            for (let i = 0; i< wdays; ++i) {
                let divDay = document.createElement('div');
                let classes = [ "day", "day_num" ];
                let divNum = document.createElement('div');
                let egroups;

                ++mday;

                if ( i === 0 ) classes.push("day_row_start");
                else if ( i === wdays-1 ) classes.push("day_row_end");

                if ( dayN < startDayN ) {
                    let tday = yearThis.DayOfMonth(dayN);

                    if ( tday > 0 ) {
                        divNum.innerHTML = tday;
                    } else {
                        if ( yearPrev === null ) {
                            yearPrev = new YearData(calendar);
                            yearPrev.Derive(yearThis.Year()-1);
                        }

                        if ( ! yearPrev.Invalid() ) {
                            tday = yearPrev.DayOfMonth(dayN);
                            if ( tday > 0 ) divNum.innerHTML = tday;
                        }
                    }

                    classes.push("day_prev_month");
                } else if ( dayN > endDayN ) {
                    let tday = yearThis.DayOfMonth(dayN);

                    if ( tday > 0 ) {
                        divNum.innerHTML = tday;
                    } else {
                        if ( yearNext === null ) {
                            yearNext = new YearData(calendar);
                            yearNext.Derive(yearThis.Year()+1);
                        }

                        if ( ! yearNext.Invalid() ) {
                            tday = yearNext.DayOfMonth(dayN);
                            if ( tday > 0 ) divNum.innerHTML = tday;
                        }
                    }

                    classes.push("day_next_month");
                } else {
                    divNum.innerHTML = mday;
                }
                if ( lastWeek ) classes.push('day_last_row');

                divNum.setAttribute("class", Classes("day_number day_cell"));

                divDay.setAttribute("id", this.DomID('day', dayN));
                divDay.setAttribute("class", Classes(classes));

                // Render events

                egroups = this.RenderEvents(dayN);
                if ( typeof options === "object" && 'render_day' in options ) {
                    let func = options.render_day;
                    func(this, divDay, divNum, egroups);
                } else {
                    divDay.appendChild(divNum);
                    Object.keys(egroups).forEach(function(t) {
                        divDay.appendChild(egroups[t]);
                    });
                }

                dayRow.push(divDay);

                ++dayN;
            }

            //return divDayRow;
            return dayRow;
        };

        this.Ordinal = function(n) {
            if ( n === undefined || n === null ) return "th";

            if ( typeof n === "number" ) {
                n = n.toString();
            }
            if ( n.match(/1\d$/)) { return 'th'; }
            else if ( n.match(/1$/) ) { return 'st'; }
            else if ( n.match(/2$/) ) { return 'nd'; }
            else if ( n.match(/3$/) ) { return 'rd'; }
            return 'th';
        };

        this.RenderDayDetail = function(dayN, options) {
            let divDay = document.createElement('div');
            let divDate = document.createElement('div');
            let dt = yearThis.DateFromDayN(dayN);
            let datestr;
            let egroups;

            if ( dt[1] === yearThis.DateBeforeYear ) {
                dt = yearPrev.DateFromDayN(dayN);
            } else if ( dt[1] === yearThis.DateAfterYear ) {
                dt = yearNext.DateFromDayN(dayN);
            }

            divDay.setAttribute("class", Classes("day_detail"));

            datestr = calendar.weekdaySet.Item(dt[2]).name+", "+
                calendar.monthSet.Item(dt[0]).name+" "+
                dt[1]+this.Ordinal(dt[1])+", "+yearThis.Year()+" "+
                calendar.era;

            egroups = this.RenderEvents(dayN);
            if ( 'render_day_detail' in options ) {
                let f = options.render_day_detail;
                f(this, datestr, divDay, egroups);
            } else {
                divDay.appendChild(divNum);
                Object.keys(egroups).forEach(function(t) {
                    divDay.appendChild(egroups[t]);
                });
            }

            return divDay;
        };
    };

    let CalendarEventTypeHoliday = 0;
    let CalendarEventTypeMoonPhase = 1;
    let CalendarEventTypeSeason = 2;
    let CalendarEventTypeFullMoon = 3;
    let CalendarEventTypeUser = 4;
    let CalendarEventTypeCurrentDay = 5;
    let CalendarEventTypes = [ "holiday", "moon_phase", "season", "first_full", "user", "current_day" ];

    let CalendarEvent = function(name, type, obj) {
        this.name = name;
        this.type = type;
        this.object = obj;
        this.data = null;
        this.dayN = null;
    };

    let CalendarEventList = function() {
        "use strict";

        let events = {};

        this.Add = function (cevent, dayN) {
            "use strict";
            let sdayN = dayN.toString();

            if ( ! (dayN in events) ) {
                events[sdayN]= [];
            }

            events[sdayN].push(cevent);
            cevent.dayN = dayN;
        };

        this.EventsOn = function(dayN) {
            let sdayN = dayN.toString();
            if ( sdayN in events ) return events[sdayN];

            return [];
        };

        this.HasEventsOn = function(dayN) {
            if ( dayN in events ) return true;
            return false;
        };
    };

    let YearData = function(cal) {
        "use strict";

        this.calendarEvents = null;
        this.DateBeforeYear = -1;
        this.DateAfterYear = 0;
        this.foundingDay = null;

        let invalid = true;
        let startDayN = null;
        let endDayN = null;
        let startDayOfWeek = null;
        let isLeapYear = false;
        let calendar = cal;
        let year = null;
        let daysInYear = null;
        let daysInMonthMax = null;
        let daysFromEpoch = null;
        let daysInMonth = [];
        let daysInWeek = null;
        let monthsInYear = null;
        let monthStartDayN = [];
        let monthEndDayN = [];
        let lunarCalendar = {};
        let seasons = [];
        let firstFullInMonth = [];


        // Returns [ month_idx, daynum, dayOfWeek_idx ]
        this.DateFromDayN = function(dayN) {
            "use strict";

            if ( dayN < startDayN ) return [ null, this.DateBeforeYear, null ];
            if ( dayN > endDayN ) return [ null, this.DateAfterYear, null ];

            for (let i = 0; i< monthsInYear; ++i) {
                let s = monthEndDayN[i];
                if ( dayN <= s ) {
                    return [i, dayN-monthStartDayN[i]+1, this.DayOfWeek(dayN)];
                }
            }
        };

        this.DaysInMonth = function(monthidx) {
            "use strict";

            if ( monthidx < 0 || monthidx >= daysInMonth.length ) return null;

            return daysInMonth[monthidx];
        };

        this.DayOfMonth = function(dayN) {
            "use strict";

            if ( dayN < startDayN ) return this.DateBeforeYear;
            if ( dayN > endDayN ) return this.DateAfterYear;

            for (let i = 0; i< monthsInYear; ++i) {
                let s = monthEndDayN[i];
                if ( dayN <= s ) {
                    return dayN-monthStartDayN[i]+1;
                }
            }
        };

        this.DayOfWeek = function(dayN) {
            "use strict";

            return (dayN+startDayOfWeek-1)%daysInWeek;
        };

        this.Derive = function(y) {
            "use strict";

            let cevents, ythis;

            this.calendarEvents = new CalendarEventList();

            cevents = this.calendarEvents;
            ythis = this;

            this.foundingDay = calendar.foundingDay;
            monthsInYear = calendar.monthSet.Size();
            daysInWeek = calendar.weekdaySet.Size();

            // Reset data structures

            startDayN = endDayN = null;
            invalid = true;
            seasons = [];
            firstFullInMonth = [];
            lunarCalendar = {};
            daysInMonth = [];
            monthStartDayN = [];
            monthEndDayN = [];
            year = y;

            // Validate basic calendar data

            if ( monthsInYear < 2 || year < 1 || year < calendar.yearMin || daysInWeek < 2 ) return false;
            invalid = false;


            // Is the current year a leap year?
            isLeapYear = calendar.leapYearRuleSet.IsLeapYear(year);

            // Get the number of days in the year, and the number of days in each month.

            daysInYear = calendar.monthSet.BaseDaysInYear();

            //daysInMonthMax = calendar.monthSet.MaxMonthLength();

            // Get the number of days in each month

            calendar.monthSet.forEach(function(m) {
                let days = m.Days();

                if ( isLeapYear && calendar.monthSet.LeapMonth() === m ) ++days;
                daysInMonth.push(days);
            });

            // Get the number of days that have come before 1/1/year.

            startDayOfWeek = this.foundingDay;
            startDayN = daysInYear*(year-1)+1;

            // Account for previous leap years
            calendar.leapYearRuleSet.forEach( function(lr) {
                let interval = lr.Interval();
                if ( interval > 0 ) {
                    startDayN += Math.floor((year-1)/interval);
                } else if ( interval < 0 ) {
                    // Subtract leap days for excluded intervals
                    startDayN += Math.ceil((year-1)/interval); // negative
                }
            });

            // Add a day if this year is a leap year.
            if ( isLeapYear ) ++daysInYear;


            // Get the day number for the start of each month

            monthStartDayN[0]= startDayN;
            monthEndDayN[0]= startDayN+daysInMonth[0]-1;
            for (let i = 1; i< daysInMonth.length; ++i) {
                monthStartDayN[i]= monthEndDayN[i-1]+1;
                monthEndDayN[i]= monthEndDayN[i-1]+daysInMonth[i];
            }
            endDayN = startDayN+daysInYear-1;

            // Add the seasons

            for (let i = 0; i< 4; ++i) {
                let dayN = startDayN + calendar.SeasonStartsOn(i, daysInYear);
                let cevent = new CalendarEvent(calendar.SeasonEventName(i), CalendarEventTypeSeason);

                seasons[i]= dayN;

                cevents.Add(cevent, dayN);
            }

            // Add lunar events

            calendar.moonSet.forEach(function(moon) {
                let thisMonth = -1;

                lunarCalendar[moon.id]= moon.LunarCalendar(startDayN, endDayN);
                lunarCalendar[moon.id].forEach( function(info) {
                    // These come as fractional days. Round them down.
                    let cevent = new CalendarEvent(moon.phaseNames[info.phase], CalendarEventTypeMoonPhase);

                    cevent.object = moon;
                    cevent.data = info.phase;
                    cevents.Add(cevent, Math.floor(info.dayN));

                    if ( info.phase === moon.moonPhases.full_moon && (thisMonth+1) < monthsInYear &&
                            info.dayN >= monthStartDayN[thisMonth+1] ) {

                        let fevent, name;

                        thisMonth++;
                        if ( ! (moon.id in firstFullInMonth) ) {
                            firstFullInMonth[moon.id]= [];
                        }
                        firstFullInMonth[moon.id][thisMonth]= info.dayN;

                        name = moon.FullMoonName(thisMonth);
                        if ( name ) {
                            fevent = new CalendarEvent(moon.FullMoonName(thisMonth)+" Moon", CalendarEventTypeFullMoon);
                            fevent.object = moon;
                            cevents.Add(fevent, Math.floor(info.dayN));
                        }
                    }
                });
            });

            // Holidays

            calendar.holidaySet.forEach(function(hday) {
                let cevent, dayN;
                let rule = hday.Rule();
                let name = hday.name;
                let param = rule.parameters;

                if ( rule.rule === hday.HolidayRule.NthDayOfMonth ) {
                    let n = parseInt(param.n);
                    let monthidx = parseInt(param.month);

                    if ( n > daysInMonth[monthidx] ) return;

                    dayN = monthStartDayN[monthidx]+parseInt(n)-1;
                    if ( dayN > monthEndDayN[monthidx] ) return;
                } else if ( rule.rule === hday.HolidayRule.NthWeekdayOfMonth ) {
                    let n = parseInt(param.n);
                    let monthidx = parseInt(param.month);
                    let weekdayidx = parseInt(param.weekday);

                    dayN = ythis.NthWeekdayOfMonth(n, weekdayidx, monthidx);
                } else if ( rule.rule === hday.HolidayRule.NthWeekOfMonth ) {
                    let n = parseInt(param.n);
                    let monthidx = parseInt(param.month);

                    dayN = ythis.NthWeekOfMonth(n, monthidx);
                    if ( dayN === null ) return;

                    cevent = new CalendarEvent(name+" begins", CalendarEventTypeHoliday);
                    cevent.object = hday;
                    cevents.Add(cevent, dayN);

                    cevent = new CalendarEvent(name+" ends", CalendarEventTypeHoliday);
                    cevent.object = hday;
                    cevents.Add(cevent, dayN+daysInWeek-1);

                    return;
                } else if ( rule.rule === hday.HolidayRule.NthDayOfSeason ) {
                    let n = parseInt(param.n);
                    let seasonidx = parseInt(param.season);

                    dayN = ythis.NthDayOfSeason(n, seasonidx);
                } else if ( rule.rule === hday.HolidayRule.PhaseOfMoonInMonth ) {
                    let moonidx = parseInt(param.month);
                    let monthidx = parseInt(param.month);
                    let phase = parseInt(param.phase);

                    // Can return a fraction
                    dayN = ythis.PhaseOfMoonInMonth(phase, moonidx, monthidx);
                    if ( dayN === null ) return null;
                    dayN = parseInt(dayN);
                } else {
                    return;
                }

                if ( dayN === null ) return;

                cevent = new CalendarEvent(name, CalendarEventTypeHoliday);
                cevent.object = hday;
                cevents.Add(cevent, dayN);
            });

            return true;
        };

        this.Invalid = function() {
            "use strict";
            return invalid;
        };

        this.MonthEndDayNumber = function(monthidx) {
            "use strict";
            return monthEndDayN[monthidx];
        };

        this.MonthStartDayNumber = function(monthidx) {
            "use strict";
            return monthStartDayN[monthidx];
        };

        this.NthDayOfSeason = function(n, seasonidx) {
            "use strict";

            let dayN;


            if ( n > 0 ) {
                dayN = seasons[seasonidx] + n-1;
            } else if ( n <= 0 ) {
                seasonidx++;
                if ( seasonidx === 4 ) seasonidx = 0;
                dayN = seasons[seasonidx]+n; // n is negative
            }

            return ( dayN > endDayN ) ? null : dayN;
        };

        this.PhaseOfMoonInMonth = function(phase, moonidx, monthidx) {
            "use strict";

            let moon = calendar.moonSet.Item(moonidx);
            let id, dayN;
            let startDayN = monthStartDayN[monthidx];
            let endDayN = monthEndDayN[monthidx];

            if ( moon === null ) return null;
            id = moon.id;

            // Start with the first full moon in the month and work forwards/backwards

            dayN = firstFullInMonth[moon.id][monthidx];

            if ( phase === moon.moonPhases.full_moon ) {
                return dayN;
            } else if ( phase === moon.moonPhases.first_quarter ) {
                // One quarter period earlier, or 3/4 period ahead
                dayN -= moon.Quarter();
                if ( dayN < startDayN ) dayN += moon.Period();
            } else if ( phase === moon.moonPhases.new_moon ) {
                dayN -= moon.Half();
                if ( dayN < startDayN ) dayN += moon.Period();
            } else if ( phase === moon.moonPhases.last_quarter ) {
                dayN += moon.Quarter();
                if ( dayN > endDayN ) dayN -= moon.Period();
                if ( dayN < startDayN ) return null;
                return dayN;
            } else {
                return null;
            }

            if ( dayN > endDayN ) return null;
            return dayN;
        };

        this.NthWeekOfMonth = function(n, monthidx) {
            "use strict";

            return this.NthWeekdayOfMonth(n, 0, monthidx);
        };

        this.NthWeekdayOfMonth = function(n, weekdayidx, monthidx) {
            "use strict";
            let endDayN = monthEndDayN[monthidx];
            let startDayN = monthStartDayN[monthidx];
            let count, wnum, dayN;

            if ( n > 0 ) {
                let wnum;

                count = 1;
                dayN = startDayN;
                wnum = this.DayOfWeek(dayN);
                if ( wnum < weekdayidx ) {
                    dayN += (weekdayidx-wnum);
                } else if ( wnum > weekdayidx ) {
                    dayN = dayN+daysInWeek-(wnum-weekdayidx);
                }
                while ( count < n ) {
                    dayN += daysInWeek;
                    ++count;
                    if ( dayN > endDayN ) return null;
                }
            } else {
                let wnum;
                count = -1;

                dayN = endDayN;
                wnum = this.DayOfWeek(dayN);
                if ( wnum > weekdayidx ) {
                    dayN -= (wnum-weekdayidx);
                } else if ( wnum < weekdayidx ) {
                    dayN = dayN-daysInWeek+(weekdayidx-wnum);
                }
                while ( count > n ) {
                    dayN -= daysInWeek;
                    --count;
                    if ( dayN < startDayN ) return null;
                }
            }

            return dayN;
        };

        this.Year = function() {
            return year;
        };
    };

    return CustomCalendarView;
})();
