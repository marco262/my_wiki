
var CustomCalendar= (function() {
    "use strict";

    var CustomCalendar= function() {

        this.monthSet= new MonthSet(this);
        this.weekdaySet= new WeekdaySet(this);
        this.moonSet= new MoonSet(this);
        this.holidaySet= new HolidaySet(this);
        this.leapYearRuleSet= new LeapYearRuleSet(this);
        this.seasonStarts= [ "northward equinox", "nothern solstice", "southward equinox", "southern solstice"];
        this.seasons= [ 'spring', 'summer', 'fall', 'winter' ];
        //this.seasonLengthPercents= [ 0.254023, 0.256488, 0.24608, 0.24341 ];
        this.seasonLengthPercents= [ .25399, .25637, .24601, .24363 ];
        //this.firstEquinoxPercent= 0.21766; // Percentage of year
        this.firstEquinoxPercent= 0.21587; // Percentage of year
        this.foundingDay= 0;
        this.yearMin= 1;
        this.name= "";
        this.era= "";

        var eccentricity= 0.0167;

        this.Clone = function () {
            "use strict";

            var cal= new CustomCalendar();

            this.weekdaySet.foreach(function(w) {
                var wday= w.Clone();
                cal.weekdaySet.Add(wday);
            });

            this.monthSet.forEach(function(m) {
                var month= m.Clone();
                cal.monthSet.Add(month);
            });

            this.leapYearRuleSet.foreach(function(lr) {
                var leaprule= lr.Clone();
                cal.leapYearRuleSet.Add(leaprule);
            });

            this.moonSet.foreach(function(m) {
                var moon= m.Clone();
                cal.moonSet.Add(moon);
            });

            this.holidaySet.foreach(function(h) {
                var holiday= h.Clone();
                cal.holidaySet.Add(holiday);
            });

            cal.seasons= this.seasons.slice();
            cal.Eccentricity(this.Eccentricity());
            cal.FirstEquinoxPercent(this.FirstEquinoxPercent());
            cal.foundingDay= this.foundingDay;
            cal.yearMin= this.yearMin;
            cal.name= this.name;
            cal.era= this.era;

            return cal;
        };

        // Set orbital eccentricity and adjust seasons

        this.Eccentricity = function (e) {
            "use strict";
            var mlam= [];
            var omegabar= 1.79647; // Hardcoded value for the earth, which is a reasonably arbitrary vlue for any planet.
            var PIx2= Math.PI*2;

            if ( e === undefined ) return;

            e= e*1;
            if ( e === "NaN" || e < 0 || e > 0.2 ) return; // Hardcoded min/max

            // http://farside.ph.utexas.edu/teaching/celestial/Celestialhtml/node35.html

            eccentricity= e;
            // autumn, winter, spring, summer
            mlam= [
                2*e*Math.sin(omegabar),
                Math.PI/2 - 2*e*Math.cos(omegabar),
                Math.PI - 2*e*Math.sin(omegabar),
                1.5*Math.PI + 2*e*Math.cos(omegabar)
            ];
            // Change to spring, summer, autumn, winter
            this.seasonLengthPercents= [
                (mlam[3]-mlam[2])/PIx2,
                (Math.PI*2+mlam[0]-mlam[3])/PIx2,
                (mlam[1]-mlam[0])/PIx2,
                (mlam[2]-mlam[1])/PIx2
            ];

            // Hardcoding: vernal equinox comes first.
            if ( this.firstEquinoxPercent > this.seasonLengthPercents[3] ) {
                this.firstEquinoxPercent= this.seasonLengthPercents[3]-.001;
            }
        };

        // Export as obj

        this.Export = function (flags) {
            "use strict";

            var obj= {};

            // Set default values for export flags if missing

            if ( flags === undefined || typeof flags !== "object" ) flags= {};
            if ( 'holidays' in flags ) {
                if ( typeof flags.holidays !== 'boolean' ) return null;
            } else flags.holidays= true;

            if ( 'moons' in flags ) {
                if ( typeof flags.moons !== 'boolean' ) return null;
            } else flags.moons= true;

            if ( this.monthSet.Size() > 0 ) obj.monthSet= this.monthSet.Export();
            if ( this.weekdaySet.Size() > 0 ) obj.weekdaySet= this.weekdaySet.Export();
            if ( this.holidaySet.Size() > 0 && flags.holidays ) obj.holidaySet= this.holidaySet.Export();
            if ( this.moonSet.Size() > 0 && flags.moons ) obj.moonSet= this.moonSet.Export();
            if ( this.leapYearRuleSet.Size() > 0 ) obj.leapYearRuleSet= this.leapYearRuleSet.Export();

            obj.seasons= this.seasons.slice();
            obj.foundingDay= this.foundingDay;
            obj.yearMin= this.yearMin;
            obj.name= this.name;
            obj.era= this.era;
            obj.eccentricity= eccentricity;
            obj.firstEquinoxPercent= this.firstEquinoxPercent;

            return obj;
        };

        this.FirstEquinoxPercent= function (val) {
            "use strict";

            if ( val !== undefined ) {
                if ( typeof val !== "number" ) return null;
                this.firstEquinoxPercent= Math.min(val, this.seasonLengthPercents[3]-.001);
            }

            return this.firstEquinoxPercent;
        };

        // Import from obj

        this.Import= function (obj) {
            "use strict";

            this.holidaySet.Clear();
            this.leapYearRuleSet.Clear();
            this.moonSet.Clear();
            this.monthSet.Clear();
            this.weekdaySet.Clear();

            if ( 'weekdaySet' in obj && typeof obj.weekdaySet === "object" ) {
                this.weekdaySet.Import(obj.weekdaySet);
            }
            if ( 'monthSet' in obj && typeof obj.monthSet === "object" ) {
                this.monthSet.Import(obj.monthSet);
            }
            if ( 'leapYearRuleSet' in obj && typeof obj.leapYearRuleSet === "object" ) {
			    this.leapYearRuleSet.Import(obj.leapYearRuleSet);
            }
            if ( 'moonSet' in obj && typeof obj.moonSet === "object" ) {
                this.moonSet.Import(obj.moonSet);
            }
            if ( 'holidaySet' in obj && typeof obj.holidaySet === "object" ) {
                this.holidaySet.Import(obj.holidaySet);
            }

            if ( 'eccentricity' in obj && typeof obj.eccentricity === "number" ) this.Eccentricity(obj.eccentricity);
            if ( 'seasons' in obj && typeof obj.seasons === "object" ) this.Seasons(obj.seasons);
            if ( 'foundingDay' in obj && typeof obj.foundingDay === "number" ) this.foundingDay= obj.foundingDay;
            if ( 'yearMin' in obj && typeof obj.yearMin === "number" ) this.yearMin= Math.floor(obj.yearMin);
            if ( 'name' in obj && typeof obj.name === "string" ) this.name= obj.name;
            if ( 'era' in obj && typeof obj.era === "string" ) this.era= obj.era;
        };

        this.NewHoliday = function () {
            "use strict";

            return new Holiday(this);
        };

        this.NewId = function () {
            "use strict";
            var crypto = window.crypto || window.msCrypto;
            var val= crypto.getRandomValues(new Uint8Array(8));
            var id='';

            for (var i= 0; i< 8; ++i) id+= val[i].toString(32);

            return id;
        };

        this.NewLeapYearRule = function () {
            "use strict";

            return new LeapYearRule(this);
        };

        this.NewMonth = function () {
            "use strict";

            return new Month(this);
        };

        this.NewMoon = function () {
            "use strict";

            return new Moon(this);
        };


        this.NewWeekday = function () {
            "use strict";

            return new Weekday(this);
        };

        // Get/set seasons

        this.Season = function (idx, name) {
            "use strict";

            if ( idx === undefined || typeof idx !== "number") return null;

            idx= Math.floor(idx);
            if ( name !== undefined && typeof name === "string" ) {
                this.seasons[idx]= name;
            }

            return this.seasons[idx];
        };

        this.SeasonEventName= function(idx) {
            "use strict";
            return this.Season(idx)+((idx%2) ? " solstice" : " equinox");
        };

        this.SeasonStartPercent= function(idx) {
            "use strict";

            var pcent= this.firstEquinoxPercent;
            for (var i= 0; i< idx; ++i) {
                pcent+= this.seasonLengthPercents[i];
            }
            return pcent;
        };

        this.SeasonStartsOn= function(idx, daysInYear) {
            "use strict";

            return Math.floor(this.SeasonStartPercent(idx)*daysInYear);
        };

        this.Seasons = function (slist) {
            "use strict";

            var sarr= [];
            if ( slist !== undefined ) {
                if ( typeof slist !== "object" && slist.length !== 4 ) return null;
                var i;
                for (i= 0; i< 4; ++i) {
                    if (typeof slist[i] === "string" ) {
                        sarr.push(slist[i]);
                    } else return null;
                    this.seasons= slist;
                }
            }

            return this.seasons;
        };

        // Stringify

        this.toString = function (flags) {
            "use strict";

            return JSON.stringify(this.Export(flags), null, 4);
        };

        this.id= this.NewId();
    };

    //=============================================================
    // Holiday class
    //=============================================================

    var Holiday= (function(){
        var Holiday = function (cal) {
            "use strict";

            var calendar= cal;
            var definition= {};

            this.parent= null;
            this.name= '';
            this.rule= null;
            this.parameters= {};
            this.observedBy= null;
            this.category= null;
            this.id= calendar.NewId();

            // Constants

            this.HolidayRule= {
                "NthDayOfMonth": 0,
                "NthWeekdayOfMonth": 1,
                "NthWeekOfMonth": 2,
                "NthDayOfSeason": 3,
                "PhaseOfMoonInMonth": 4
            };

            this.HolidayRules= [
                { name:'NthDayOfMonth', description:'Nth day of Month', value:this.HolidayRule.NthDayOfMonth, template:['%N%',' of ','%MONTH%'] },
                { name:'NthWeekdayOfMonth', description:'Nth Weekday of Month', value:this.HolidayRule.NthWeekdayOfMonth, template:['%N%',' ','%WEEKDAY%',' of ','%MONTH%'] },
                { name:'NthWeekOfMonth', description:'Nth week of Month', value:this.HolidayRule.NthWeekOfMonth, template:['%N%',' week of ','%MONTH%'] },
                { name:'NthDayOfSeason', description:'Nth day of Season', value:this.HolidayRule.NthDayOfSeason, template:['%N%',' day of ','%SEASON%'] },
                { name:'PhaseOfMoonInMonth', description:'Phase of Moon in Month', value:this.HolidayRule.PhaseOfMoonInMonth, template:['%PHASE%', ' of ','%MOON%',' in ','%MONTH%'] }
            ];

            // Clone this holiday

            this.Clone= function () {
                "use strict";

                var holiday= calendar.NewHoliday();

                holiday.parent= null;
                holiday.name= this.name;
                holiday.observedBy= this.observedBy;
                holiday.category= this.category;
                holiday.Rule(this.rule, this.parameters);

                return holiday;
            };

            // Export as obj

            this.Export= function () {
                "use strict";

                var obj= {
                    "name": this.name,
                    "rule": definition.name,
                    "parameters": this.parameters
                };

                if ( this.observedBy !== null && this.observedBy !== "" ) obj.observedBy= this.observedBy;
                if ( this.category !== null && this.category !== "" ) obj.category= this.category;

                return obj;
            };

            // Import from obj

            this.Import= function (obj) {
                "use strict";

                if ( 'name' in obj && typeof obj.name === "string" ) this.name= obj.name;
                if ( 'observedBy' in obj && typeof obj.observedBy === "string" ) this.observedBy= obj.observedBy;
                if ( 'category' in obj && typeof obj.category === "string" ) this.category= obj.category;
                if ( 'rule' in obj && typeof obj.rule === "string" &&
                        'parameters' in obj && typeof obj.parameters === "object" ) this.Rule(this.HolidayRule[obj.rule], obj.parameters);
            };

            // Index of this holiday

            this.Index= function () {
                "use strict";

                if ( this.parent === null ) { return -1; }

                return this.parent.Index({holiday: this});
            };

            // Get/set the rule and parameters. Takes a rule num. and a
            // list of params, returns an object.

            this.Parameter= function (param, value) {
                "use strict";

                if ( typeof param !== "string" ) return null;
                if ( value !== undefined ) {
                    if ( typeof value !== "string" && typeof value !== "number" ) return false;
                    this.parameters[param]= value;
                }

                if ( param in this.parameters ) return this.parameters[param];
                return null;
            };

            this.Parameters= function (params) {
                "use strict";

                if ( typeof params !== "object" ) return false;

                this.parameters= {};
                for (var key in params) {
                    this.parameters[key]= params[key];
                }

                return true;
            };

            this.Rule= function (rule, params) {
                "use strict";

                if ( rule !== undefined ) {
                    rule= parseInt(rule);
                    if ( rule < 0 || rule > 4 ) return null;

                    this.rule= rule;
                    definition= {
                        "name": this.HolidayRules[rule].name,
                        "template": this.HolidayRules[rule].template
                    };

                    this.parameters= {};
                    if ( params !== undefined && typeof params === "object" ) {
                        for (var key in params) {
                            this.parameters[key]= params[key];
                        }
                    }
                }

                return {
                    "rule": this.rule,
                    "parameters": this.parameters,
                    "definition": definition
                };
            };

            // Stringify

            this.toString= function () {
                "use strict";

                return JSON.stringify(this.Export(), null, 4);
            };
        };
        return Holiday;
    })();

    //=============================================================
    // Holiday class
    //=============================================================

    var HolidaySet= (function() {
        var HolidaySet = function (calendar) {
            "use strict";

            this.parent= calendar;

            var holidays= [];

            this.forEach= function(x) {
                "use strict";

                holidays.forEach(x);
            };

            // Add a holiday to the end of the array

            this.Add= function (holiday) {
                "use strict";

                if ( typeof holiday !== "object" ) { return -1; }

                holiday.parent= this;
                holidays.push(holiday);

                return holidays.length-1;
            };

            // Clear the set

            this.Clear= function (month) {
                "use strict";
                holidays= [];
            };

            // Export as obj

            this.Export= function () {
                "use strict";

                return {
                    "holidays": this.Items().map(function(h) { return h.Export(); })
                };
            };

            // Return a new HolidaySet based on the (simple) search filter. The
            // filters work as an "OR" condition.
            //
            //  filter= {
            //     "category": string,
            //     "observedBy": string,
            //     "rule": number
            //     "regex": true/false
            //  }
            //
            // If no filter, returns null. If empty filter, returns empty HolidaySet
            //
            // To get an AND filter, run again on the result set.

            this.Find= function(filter) {
                "use strict";

                var hset;
                var regex= {};

                if ( filter === undefined ) return null;
                if ( typeof filter !== "object" ) return null;
                if ( ! "regex" in filter ) filter.regex= false;

                hset= new HolidaySet(this.parent);

                this.forEach(function (x) {
                    var include= false;

                    if ( "category" in filter ) {
                        if ( filter.regex ) {
                            if ( ! "category" in regex ) regex.category= new Regex(filter.category);
                            include= _find_string(regex.category, x.category, true);
                        } else {
                            include= _find_string(filter.category, x.category, false);
                        }
                    }

                    if ( ! include && "observedBy" in filter  ) {
                        if ( filter.regex ) {
                            if ( ! "observedBy" in regex ) regex.observedBy= new Regex(filter.observedBy);
                            include= _find_string(regex.category, x.category, true);
                        } else {
                            include= _find_string(filter.category, x.category, false);
                        }
                    }

                    if ( ! include && "rule" in filter ) {
                        var rule= x.Rule().rule;

                        if ( filter.rule.constructor === Array ) {
                            for (var i= 0; ! include && i< filter.rule.length; ++i) {
                                include= ( rule === filter.rule[i] );
                            }
                        } else {
                            include= (rule === filter.rule);
                        }
                    }

                    if ( include ) hset.Add(x);
                });

                return hset;
            };

            // Works for a string or array.

            var _find_string= function (pattern, string, regex) {
                if ( string.constructor === Array ) {
                    if ( regex ) {
                        for (var i= 0; i< string.length; ++i ) {
                            if ( pattern.match(string[i]) ) return true;
                        }
                        return false;
                    }

                    for (var i= 0; i< string.length; ++i ) {
                        if ( string[i] === pattern ) return true;
                    }
                    return false;
                }

                if ( regex ) {
                    return pattern.match(string);
                }

                return (pattern === string);
            };

            // Import from obj

            this.Import= function(obj) {
                "use strict";

                var hset= this;
                var cal= this.parent;

                this.Clear();
                if ( 'holidays' in obj && typeof obj.holidays === "object" && obj.holidays.length > 0 ) {
                    obj.holidays.forEach(function(h) {
                        if ( typeof h === "object" ) {
                            var holiday= cal.NewHoliday();
                            holiday.Import(h);
                            hset.Add(holiday);
                        }
                    });
                }
            };

            // Get the array index of the specified holiday.

            this.Index= function (option) {
                "use strict";

                var i;

                if ( option === undefined || typeof option !== "object" ) return -1;

                if ( 'index' in option ) {
                    if ( typeof option.index === "number" ) return option.index;
                };

                if ( 'holiday' in option ) {
                    if ( typeof option['holiday'] !== "object" ) {
                         return -1;
                    }
                }

                for (i= 0; i< holidays.length; ++i) {
                    var holiday= holidays[i];
                    if ( 'holiday' in option ) {
                        if ( option['holiday'].id === holiday.id ) { return i; }
                    } else if ( 'name' in option ) {
                        if ( holiday.name === option['name'] ) { return i; }
                    } else if ( 'id' in option ) {
                        if ( holiday.id === option['id'] ) { return i; }
                    }
                }

                return  -1;
            };

            // Insert a holiday before the specified holiday

            this.Insert= function (holiday, option) {
                "use strict";

                var idx;

                if ( typeof holiday !== "object" ) { return false; }

                if ( 'index' in option ) {
                    idx= option['index'];
                } else {
                    idx= this.Index(option);
                }

                if ( idx < 0 || idx >= holidays.length ) {
                    return false;
                }

                holiday.parent= this;
                holidays.splice(idx, 0, holiday);

                return true;
            };

            // Return the specified holiday

            this.Item= function (idx) {
                "use strict";

                if ( idx < 0 || idx >= holidays.length ) {
                    return null;
                }

                return holidays[idx];
            };

            // Return an array of items

            this.Items= function () {
                "use strict";

                return holidays;
            };

            this.ItemById= function (id) {
                "use strict";
                return this.Item(this.Index({"id": id}));
            };

            // Remove the specified holiday

            this.Remove= function (option) {
                "use strict";

                var idx;

                if ( 'index' in option ) {
                    idx= option['index'];
                } else {
                    idx= this.Index(option);
                }

                if ( idx === -1 || idx >= holidays.length ) {
                    return false;
                }

                holidays.splice(idx, 1);

                return true;
            };

            this.Size= function() {
                return holidays.length;
            };

            // Stringify

            this.toString= function () {
                "use strict";

                return JSON.stringify(this.Export(), null, 4);
            };
        };

        return HolidaySet;
    })();
    //=============================================================
    // LeapYearRule class
    //=============================================================

    var LeapYearRule= (function() {
        var LeapYearRule = function (cal) {
            "use strict";

            var interval= 0;
            var isLeap= true;
            var calendar= cal;

            this.parent= null;
            this.id= cal.NewId();


            // Clone this leap year rule

            this.Clone= function () {
                "use strict";

                var leaprule= calendar.NewLeapYearRule();

                leaprule.parent= null;
                leaprule.Interval(this.Interval());

                return leaprule;
            };

            // Set an exclusion interval

            this.Exclude= function (n) {
                "use strict";

                if ( typeof n === "number" ) {
                    interval= n;
                    isLeap= false;
                } else return false;

                return true;
            };

            // Export as an object

            this.Export= function () {
                return {
                    "interval": interval,
                    "isLeap": isLeap
                };
            };

            // Import from obj

            this.Import= function (obj) {
                "use strict";

                if ( "interval" in obj && typeof obj.interval === "number" ) interval= Math.floor(obj.interval);
                if ( "isLeap" in obj && typeof obj.isLeap === "boolean" ) isLeap= obj.isLeap;
            };

            // Set an inclusive interval

            this.Include= function (n) {
                "use strict";

                if ( typeof n === "number" ) {
                    interval= n;
                    isLeap= true;
                } else return false;

                return true;
            };

            // Index of this leaprule

            this.Index= function () {
                "use strict";

                if ( this.parent === null ) { return -1; }

                return this.parent.Index({leaprule: this});
            };

            // Get/set the leap interval (+n include, -n exclude)

            this.Interval= function (n) {
                "use strict";

                if ( n !== undefined ) {
                    n= Math.floor(n);
                    if ( n > 0 ) {
                        isLeap= true;
                        interval= n;
                    } else if ( n < 0 ) {
                        isLeap= false;
                        interval= -n;
                    } else {
                        return null;
                    }
                }

                return ((isLeap) ? 1 : -1) * interval;
            };

            // Stringify

            this.toString= function () {
                "use strict";

                return JSON.stringify(this.Export());
            };
        };
        return LeapYearRule;
    })();

    //=============================================================
    // LeapYearRuleSet class
    //=============================================================

    var LeapYearRuleSet = (function(){
        var LeapYearRuleSet = function (cal) {
            "use strict";

            var leaprules= [];
            var calendar= cal;

            this.parent= calendar;

            this.forEach= function(x) {
                "use strict";

                leaprules.forEach(x);
            };

            // Add a leaprule to the end of the array

            this.Add= function (leaprule) {
                "use strict";

                if ( typeof leaprule !== "object" ) { return -1; }

                leaprule.parent= this;
                calendar= this.parent;
                leaprules.push(leaprule);

                return leaprules.length-1;
            };

            // Clear the set

            this.Clear= function () {
                "use strict";
                leaprules= [];
            };

            // Export as obj

            this.Export= function () {
                "use strict";

                var obj= {
                    "leaprules": this.Items().map(function(x) {return x.Export();})
                };

                return obj;
            };

            // Import from obj

            this.Import= function (obj) {
                "use strict";

                var cal= this.parent;
                var lset= this;
                this.Clear();

                if ( 'leaprules' in obj && typeof obj.leaprules === "object" && obj.leaprules.length > 0 ) {
                    obj.leaprules.forEach(function(l) {
                        if ( typeof l === "object" ) {
                            var leaprule= cal.NewLeapYearRule();
                            leaprule.Import(l);
                            lset.Add(leaprule);
                        }
                    });
                }
            };

            // Get the array index of the specified leaprule.

            this.Index= function (option) {
                "use strict";

                var i;

                if ( option === undefined || typeof option !== "object" ) return -1;

                if ( 'leaprule' in option ) {
                    if ( typeof option['leaprule'] !== "object" ) {
                         return -1;
                    }
                }

                for (i= 0; i< leaprules.length; ++i) {
                    var leaprule= leaprules[i];
                    if ( 'leaprule' in option ) {
                        if ( option['leaprule'].id === leaprule.id ) { return i; }
                    } else if ( 'id' in option ) {
                        if ( leaprule.id === option['id'] ) { return i; }
                    }
                }

                return  -1;
            };

            // Insert a leaprule before the specified leaprule

            this.Insert= function (leaprule, option) {
                "use strict";

                var idx;

                if ( typeof leaprule !== "object" ) { return false; }

                if ( 'index' in option ) {
                    idx= option['index'];
                } else {
                    idx= this.Index(option);
                }

                if ( idx < 0 || idx >= (this.length) ) {
                    return false;
                }

                leaprule.parent= this;
                calendar= this.parent;
                leaprules.splice(idx, 0, leaprule);

                return true;
            };

            // Is the specified year a leap year?

            this.IsLeapYear= function(year) {
                "use strict";

                var isleap= false;

                this.Items().forEach(function(l) {
                    var n= l.Interval();
                    if ( n > 0 && !(year % n) ) {
                        isleap= true;
                    } else if ( n < 0 && !(year % -n) ) {
                        isleap= false;
                    }
                });

                return isleap;
            };

            // Return the specified leaprule

            this.Item= function (idx) {
                "use strict";

                if ( idx < 0 || idx >= leaprules.length ) {
                    return null;
                }

                return leaprules[idx];
            };

            // Return an array of items

            this.Items= function () {
                "use strict";

                return leaprules;
            };

            this.ItemById= function (id) {
                "use strict";
                return this.Item(this.Index({"id": id}));
            };

            // Remove the specified leaprule

            this.Remove= function (option) {
                "use strict";

                var idx;

                if ( 'index' in option ) {
                    idx= option['index'];
                } else {
                    idx= this.Index(option);
                }

                if ( idx === -1 || idx >= leaprules.length ) {
                    return false;
                }

                leaprules.splice(idx, 1);

                return true;
            };

            this.Size= function () {
                return leaprules.length;
            };

            this.toString= function () {
                "use strict";

                return JSON.stringify(this.Export());
            };
        };
        return LeapYearRuleSet;
    })();

    //=============================================================
    // Month class
    //=============================================================

    var Month = (function(){
        var Month = function (cal) {
            "use strict";

            var calendar= cal;
            var days= 30;

            this.parent= null;
            this.name= '';
            this.nameShort= '';
            this.nameAbbrev= '';
            this.id= calendar.NewId();


            // Clone this month

            this.Clone= function () {
                "use strict";

                var month= new Month(calendar);

                month.parent= null;
                month.name= this.name;
                month.nameShort= this.nameShort;
                month.nameAbbrev= this.nameAbbrev;
                month.Days(days);

                return month;
            };

            // Get/Set the days

            this.Days= function (n) {
                "use strict";

                if ( n !== undefined ) {
                    var pdays= days;
                    if ( typeof n !== "number" ) return null;
                    days= Math.floor(n);

                    if ( this.parent !== null ) {
                        // Update total months in year
                        this.parent.Recalculate();
                    }
                }

                return days;
            };

            // Export as an object

            this.Export= function () {
                return {
                    "name": this.name,
                    "nameShort": this.nameShort,
                    "nameAbbrev": this.nameAbbrev,
                    "days": days
                };
            };

            // Import from obj

            this.Import= function (obj) {
                "use strict";

                if ( 'name' in obj && typeof obj.name === "string" ) this.name= obj.name;
                if ( 'nameShort' in obj && typeof obj.nameShort === "string" ) this.nameShort= obj.nameShort;
                if ( 'nameAbbrev' in obj && typeof obj.nameAbbrev === "string" ) this.nameAbbrev= obj.nameAbbrev;
                if ( 'days' in obj && typeof obj.days === "number" ) days= Math.floor(obj.days);
            };

            // Index of this month

            this.Index= function () {
                "use strict";

                if ( this.parent === null ) { return -1; }

                return this.parent.Index({month: this});
            };

            // Boolean: is this a leap month?

            this.IsLeapMonth= function () {
                "use strict";

                if ( this.parent === null ) { return false; }

                return (this.parent.leapMonth === this);
            };

            // Set all names at once

            this.Names= function(name, sname, aname) {
                "use strict";

                this.name= name;
                if ( sname !== undefined ) this.nameShort= sname;
                if ( aname !== undefined ) this.nameAbbrev= aname;
            };

            // Stringify

            this.toString= function () {
                "use strict";

                return JSON.stringify(this.Export());
            };
        };

        return Month;
    })();

    //=============================================================
    // MonthSet class
    //=============================================================

    var MonthSet= (function(){
        var MonthSet = function (calendar) {
            "use strict";

            this.parent= calendar;
            this.leapMonth= null;

            var months= [];
            var daysInYear= 0;
            var daysInMonthMax= 0;

            this.forEach= function(x) {
                "use strict";

                months.forEach(x);
            };

            // Add a month to the end of the array

            this.Add= function (month) {
                "use strict";

                if ( typeof month !== "object" ) { return -1; }

                month.parent= this;
                month.calendar= this.parent;
                months.push(month);
                daysInYear+= month.Days();

                return months.length-1;
            };

            // Base days in year

            this.BaseDaysInYear= function (month) {
                return daysInYear;
            };

            // Clear the set

            this.Clear= function (month) {
                "use strict";
                months= [];
                this.leapMonth= null;
                daysInYear= 0;
                daysInMonthMax= 0;
            };

            // Export as obj

            this.Export= function () {
                "use strict";

                var obj= {
                    "months": this.Items().map(function(x) {return x.Export();})
                };

                if ( this.leapMonth !== null ) {
                    obj["leapMonth"]= this.LeapMonth().Index();
                };

                return obj;
            };

            // Import from obj

            this.Import= function (obj) {
                "use strict";

                var cal= this.parent;
                var mset= this;
                this.Clear();

                if ( 'months' in obj && typeof obj.months === "object" && obj.months.length > 0 ) {
                    obj.months.forEach(function(m) {
                        if ( typeof m === "object" ) {
                            var month= cal.NewMonth();
                            month.Import(m);
                            mset.Add(month);
                        }
                    });

                    if ( 'leapMonth' in obj && typeof obj.leapMonth === "number" &&
                        obj.leapMonth >= 0 && obj.leapMonth < months.length ) {

                        this.LeapMonth({index: obj.leapMonth});
                    }
                }
            };

            // Get the array index of the specified month.

            this.Index= function (option) {
                "use strict";

                var i;

                if ( option === undefined || typeof option !== "object" ) return -1;

                if ( 'index' in option ) {
                    if ( typeof option.index === "number" ) return option.index;
                };

                if ( 'month' in option ) {
                    if ( typeof option['month'] !== "object" ) {
                         return -1;
                    }
                }

                for (i= 0; i< months.length; ++i) {
                    var month= months[i];
                    if ( 'month' in option ) {
                        if ( option['month'].id === month.id ) { return i; }
                    } else if ( 'name' in option ) {
                        if ( month.name === option['name'] ) { return i; }
                    } else if ( 'id' in option ) {
                        if ( month.id === option['id'] ) { return i; }
                    }
                }

                return  -1;
            };

            // Insert a month before the specified month

            this.Insert= function (month, option) {
                "use strict";

                var idx;

                if ( typeof month !== "object" ) { return false; }

                if ( 'index' in option ) {
                    idx= option['index'];
                } else {
                    idx= this.Index(option);
                }

                if ( idx < 0 || idx >= months.length ) {
                    return false;
                }

                month.parent= this;
                month.calendar= this.parent;
                months.splice(idx, 0, month);
                daysInYear+= month.Days();

                return true;
            };

            // Return the specified month

            this.Item= function (idx) {
                "use strict";

                if ( idx < 0 || idx >= months.length ) {
                    return null;
                }

                return months[idx];
            };

            // Return an array of items

            this.Items= function () {
                "use strict";

                return months;
            };

            this.ItemById= function (id) {
                "use strict";
                return this.Item(this.Index({"id": id}));
            };

            // Get/set the leap month

            this.LeapMonth= function (option) {
                if ( option !== undefined ) {
                    var idx= this.Index(option);

                    if ( idx === -1 ) return null;

                    this.leapMonth= this.Item(idx);
                }

                return this.leapMonth;
            };

            // Get the max days in a month

            this.MaxMonthLength= function () {
                "use strict";
                return daysInMonthMax;
            };

            // Recalc dervied properties

            this.Recalculate= function (){
                "use strict";

                daysInYear= 0;

                this.forEach(function(m) {
                    daysInYear+= m.Days();
                    daysInMonthMax= Math.max(m.Days(), daysInMonthMax);
                });
            };

            // Remove the specified month

            this.Remove= function (option) {
                "use strict";

                var idx;

                if ( 'index' in option ) {
                    idx= option['index'];
                } else {
                    idx= this.Index(option);
                }

                if ( idx === -1 || idx >= (this.length) ) {
                    return false;
                }

                if ( this.leapMonth === this.Item(idx) ) {
                    this.leapMonth= null;
                }

                daysInYear-= this.Item(idx).Days();
                months.splice(idx, 1);
                --length;

                return true;
            };

            this.Size= function () {
                return months.length;
            };

            this.toString= function () {
                "use strict";

                return JSON.stringify(this.Export());
            };
        };

        return MonthSet;
    })();

    //=============================================================
    // Weekday class
    //=============================================================

    var Weekday= (function() {
        var Weekday = function (cal) {
            "use strict";

            var calendar= cal;

            this.parent= null;
            this.name= '';
            this.nameShort= '';
            this.nameAbbrev= '';
            this.id= calendar.NewId();

            // Import from obj

            this.Import= function (obj) {
                "use strict";

                if ( 'name' in obj && typeof obj.name === "string" ) this.name= obj.name;
                if ( 'nameShort' in obj && typeof obj.nameShort === "string" ) this.nameShort= obj.nameShort;
                if ( 'nameAbbrev' in obj && typeof obj.nameAbbrev === "string" ) this.nameAbbrev= obj.nameAbbrev;
            };

            // Index of this weekday

            this.Index= function () {
                "use strict";

                if ( this.parent === null ) { return -1; }

                return this.parent.Index({month: this});
            };

            // Clone this weekday

            this.Clone= function () {
                "use strict";

                var wday= calendar.NewWeekday();

                wday.parent= null;
                wday.name= this.name;
                wday.nameShort= this.nameShort;
                wday.nameAbbrev= this.nameAbbrev;

                return wday;
            };

            this.Export= function () {
                "use strict";

                return {
                    "name": this.name,
                    "nameShort": this.nameShort,
                    "nameAbbrev": this.nameAbbrev
                };
            };

            this.Index= function () {
                "use strict";

                if ( this.parent === null ) { return -1; }

                return this.parent.Index({month: this});
            };

            // Set all names at once

            this.Names= function(name, sname, aname) {
                "use strict";

                this.name= name;
                if ( sname !== undefined ) this.nameShort= sname;
                if ( aname !== undefined ) this.nameAbbrev= aname;
            };

            this.toString= function () {
                "use strict";

                return JSON.stringify(this.Export());
            };
        };

        return Weekday;
    })();

    //=============================================================
    // WeekdaySet class
    //=============================================================

    var WeekdaySet = (function() {
        var WeekdaySet = function (calendar) {
            "use strict";

            this.parent= calendar;

            var weekdays= [];

            this.forEach= function (x) {
                "use strict";
                weekdays.forEach(x);
            };

            // Add a weekday to the end of the array

            this.Add= function (weekday) {
                "use strict";

                if ( typeof weekday !== "object" ) { return -1; }

                weekday.parent= this;
                weekday.calendar= this.parent;
                weekdays.push(weekday);

                return weekdays.length-1;
            };

            // Clear everything

            this.Clear= function () {
                "use strict";

                weekdays= [];
            };

            // Export as an obj

            this.Export= function () {
                "use strict";

                return {
                    "weekdays": this.Items().map(function(w) { return w.Export(); })
                };
            };
            // Import from obj

            this.Import= function (obj) {
                "use strict";

                var cal= this.parent;
                var wset= this;
                this.Clear();

                if ( 'weekdays' in obj && typeof obj.weekdays === "object" && obj.weekdays.length > 0 ) {
                    obj.weekdays.forEach(function(w) {
                        if ( typeof w === "object" ) {
                            var wday= cal.NewWeekday();
                            wday.Import(w);
                            wset.Add(wday);
                        }
                    });
                }
            };

            // Get the array index of the specified weekday.

            this.Index= function (option) {
                "use strict";

                var i;

                if ( option === undefined || typeof option !== "object" ) return -1;

                if ( 'index' in option ) {
                    if ( typeof option.index === "number" ) return option.index;
                };

                if ( 'weekday' in option ) {
                    if ( typeof option['weekday'] !== "object" ) {
                         return -1;
                    }
                }

                for (i= 0; i< weekdays.length; ++i) {
                    var weekday= weekdays[i];
                    if ( 'weekday' in option ) {
                        if ( option['weekday'].id === weekday.id ) { return i; }
                    } else if ( 'name' in option ) {
                        if ( weekday.name === option['name'] ) { return i; }
                    } else if ( 'id' in option ) {
                        if ( weekday.id === option['id'] ) { return i; }
                    }
                }

                return  -1;
            };

            // Insert a weekday before the specified weekday

            this.Insert= function (weekday, option) {
                "use strict";

                var idx;

                if ( typeof weekday !== "object" ) { return false; }

                if ( 'index' in option ) {
                    idx= option['index'];
                } else {
                    idx= this.Index(option);
                }

                if ( idx < 0 || idx >= (this.length) ) {
                    return false;
                }

                weekday.parent= this;
                weekday.calendar= this.parent;
                weekdays.splice(idx, 0, weekday);

                return true;
            };

            // Return the weekday at index idx

            this.Item= function (idx) {
                "use strict";

                if ( idx < 0 || idx >= weekdays.length ) {
                    return null;
                }

                return weekdays[idx];
            };

            // Return an array of items

            this.Items= function () {
                "use strict";

                return weekdays;
            };

            this.ItemById= function (id) {
                "use strict";
                return this.Item(this.Index({"id": id}));
            };

            // Remove the specified weekday

            this.Remove= function (option) {
                "use strict";

                var idx;

                if ( 'index' in option ) {
                    idx= option['index'];
                } else {
                    idx= this.Index(option);
                }

                if ( idx === -1 || idx >= weekdays.length ) {
                    return false;
                }

                weekdays.splice(idx, 1);

                return true;
            };

            this.Size= function() {
                return weekdays.length;
            };

            // Stringify

            WeekdaySet.prototype.toString= function () {
                "use strict";

                return JSON.stringify(this.Export());
            };
        };

        return WeekdaySet;
    })();

    //=============================================================
    // Moon class
    //=============================================================

    var Moon = (function() {


        // Prevent silliness
        var minPeriod= 4;

        var Moon = function (cal) {
            "use strict";

            // Constants
            this.moonPhases= {
                    'new_moon': 1,
                    'first_quarter': 2,
                    'full_moon': 3,
                    'last_quarter': 4
            };

            // phase 0, 1, 2, 3, 4 ( 0 == not a quarter phase )
            this.phaseNames = [ '', 'new moon', 'first quarter', 'full moon', 'last quarter' ];

            var calendar= cal;
            var period= 30;
            var quarter= 7.5;
            var color= '#ffffff';
            var shadowColor= '#000000';
            // Names the first full moon in each month, with moons from 0 to N
            var fullNames= [];

            this.parent= null;
            this.name= '';
            this.firstFull= 1;
            this.id= calendar.NewId();

            // Clone this moon

            this.Clone= function () {
                "use strict";

                var moon= calendar.NewMoon();

                moon.parent= null;
                moon.name= this.name;
                moon.Period(period);
                moon.Colors(color, shadowColor);
                moon.FullMoonNames(fullNames.join(","));
                moon.firstFull= this.firstFull;

                return moon;
            };

            // Get/set moon color

            this.Color = function(c) {
                "use strict";
                if ( c !== undefined ) {
                    color= c;
                }

                return color;
            };

            // Set the moon color and shadow color, returns both.

            this.Colors = function (c, s) {
                "use strict";

                if ( c !== undefined ) {
                    color= c;
                    if (s === undefined) shadowColor= ShadeColor(c, -0.6);
                    else shadowColor= s;
                }
                return new Array(color, shadowColor);
            };

            // Export as object

            this.Export= function () {
                "use strict";

                return {
                    "name": this.name,
                    "period": period,
                    "color": color,
                    "shadowColor": shadowColor,
                    "firstFull": this.firstFull,
                    "fullNames": fullNames.slice()
                };
            };

            // Full moon name for month idx

            this.FullMoonName= function (idx) {
                "use strict";

                if ( idx < 0 || idx >= fullNames.length ) return "";

                return fullNames[idx];
            };

            // Set full moon names from comma-separated string, trimming whitespace

            this.FullMoonNames= function (s) {
                "use strict";

                if (s !== undefined ) {
                    fullNames= [];
                    var fnames= [];

                    if ( s === undefined ) { return; }

                    s.split(",").forEach(function(name) {
                        fnames.push(name.trim());
                    });
                    fullNames= fnames.slice();
                }

                return fullNames;
            };

            // Get a half period

            this.Half= function() {
                "use strict";
                return period/2;
            };

            // Import from obj

            this.Import= function(obj) {
                "use strict";

                if ( 'name' in obj && typeof obj.name === "string" ) this.name= obj.name;
                if ( 'period' in obj && typeof obj.period === "number" ) this.Period(obj.period);
                if ( 'color' in obj && typeof obj.color === "string" ) this.Color(obj.color);
                if ( 'shadowColor' in obj && typeof obj.shadowColor === "string" ) this.ShadowColor(obj.shadowColor);
                if ( 'firstFull' in obj && typeof obj.firstFull === "number" ) this.firstFull= obj.firstFull;
                if ( 'fullNames' in obj && typeof obj.fullNames === "object" && obj.fullNames.length > 0 ) {
                    var fnames= [];
                    obj.fullNames.forEach(function(x) {
                        if ( typeof x === "string") fnames.push(x);
                    });
                    fullNames= fnames;
                }
            };


            // Index of this moon

            this.Index= function () {
                "use strict";

                if ( this.parent === null ) { return -1; }

                return this.parent.Index({moon: this});
            };

            // Return a calendar of lunar events between the given days

            this.LunarCalendar= function(startDayN, endDayN) {
                "use strict";

                var phase, dayN;
                var lunarCalendar= [];

                // Get the first full moon after startDayN

                dayN= this.firstFull + period * Math.ceil((startDayN-this.firstFull)/period);
                phase= this.moonPhases.full_moon;

                // Now back up by quarters until we hit startDayN

                while ( (dayN-quarter) >= startDayN ) {
                    dayN-= quarter;
                    --phase;
                    if ( phase < this.moonPhases.new_moon ) phase= this.moonPhases.last_quarter;
                }

                // Now we can generate a calendar by fractional day.

                while ( dayN <= endDayN ) {
                    lunarCalendar.push({"dayN": dayN, "phase": phase});
                    dayN+= quarter;
                    ++phase;
                    if ( phase > this.moonPhases.last_quarter ) phase= this.moonPhases.new_moon;
                }

                return lunarCalendar;
            };

            // Get/set the moon period

            this.Period= function (days) {
                "use strict";

                if ( days !== undefined && days !== null ) {
                    if ( days < minPeriod ) {
                        period= minPeriod;
                    } else {
                        period= days;
                    }
                    quarter= period/4;
                }

                return period;
            };

            this.Quarter= function () {
                return quarter;
            };

             // https://stackoverflow.com/questions/5560248/programmatically-lighten-or-darken-a-hex-color-or-rgb-and-blend-colors
            var ShadeColor= function(color, percent) {
                var f=parseInt(color.slice(1),16),t=percent<0?0:255,p=percent<0?percent*-1:percent,R=f>>16,G=f>>8&0x00FF,B=f&0x0000FF;
                return "#"+(0x1000000+(Math.round((t-R)*p)+R)*0x10000+(Math.round((t-G)*p)+G)*0x100+(Math.round((t-B)*p)+B)).toString(16).slice(1);
            };

            // Get/set moon color

            this.ShadowColor = function(s) {
                "use strict";
                if ( s !== undefined ) {
                    shadowColor= s;
                }

                return shadowColor;
            };


            // Stringify

            this.toString= function () {
                "use strict";

                return JSON.stringify(this.Export());
            };
        };
        return Moon;
    })();

    //=============================================================
    // MoonSet class
    //=============================================================

    var MoonSet = (function(){
        var MoonSet = function (calendar) {
            "use strict";

            this.parent= calendar;

            var moons= [];

            this.forEach= function(x) {
                "use strict";

                moons.forEach(x);
            };

            // Add a moon to the end of the array

            this.Add= function (moon) {
                "use strict";

                if ( typeof moon !== "object" ) { return -1; }

                moon.parent= this;
                moon.calendar= this.parent;
                moons.push(moon);

                return moons.length-1;
            };

            // Clear everything

            this.Clear= function() {
                "use strict";

                moons= [];
            };

            // Export as obj

            this.Export= function () {
                "use strict";

                return {
                    "moons": this.Items().map(function(x) {return x.Export();})
                };
            };

            // Import from obj

            this.Import= function (obj) {
                "use strict";

                var cal= this.parent;
                var mnset= this;

                this.Clear();
                if ( "moons" in obj ) {
                    obj.moons.forEach(function(m) {
                        if ( typeof m === "object" ) {
                            var moon= cal.NewMoon();
                            moon.Import(m);
                            mnset.Add(moon);
                        }
                    });
                };
            };

            // Get the array index of the specified moon.

            this.Index= function (option) {
                "use strict";

                var i;

                if ( option === undefined || typeof option !== "object" ) return -1;

                if ( 'index' in option ) {
                    if ( typeof option.index === "number" ) return option.index;
                };

                if ( 'moon' in option ) {
                    if ( typeof option['moon'] !== "object" ) {
                         return -1;
                    }
                }

                for (i= 0; i< moons.length; ++i) {
                    var moon= moons[i];
                    if ( 'moon' in option ) {
                        if ( option['moon'].id === moon.id ) { return i; }
                    } else if ( 'name' in option ) {
                        if ( moon.name === option['name'] ) { return i; }
                    } else if ( 'id' in option ) {
                        if ( moon.id === option['id'] ) { return i; }
                    }
                }

                return  -1;
            };

            // Insert a moon before the specified moon

            this.Insert= function (moon, option) {
                "use strict";

                var idx;

                if ( typeof moon !== "object" ) { return false; }

                if ( 'index' in option ) {
                    idx= option['index'];
                } else {
                    idx= this.Index(option);
                }

                if ( idx < 0 || idx >= (this.length) ) {
                    return false;
                }

                moon.parent= this;
                moon.calendar= this.parent;
                moons.splice(idx, 0, moon);

                return true;
            };

            // Return the specified moon

            this.Item= function (idx) {
                "use strict";

                if ( idx < 0 || idx >= moons.length ) {
                    return null;
                }

                return moons[idx];
            };

            // Return an array of items

            this.Items= function () {
                "use strict";

                return moons;
            };

            this.ItemById= function (id) {
                "use strict";
                return this.Item(this.Index({"id": id}));
            };

            // Remove the specified moon

            this.Remove= function (option) {
                "use strict";

                var idx;

                if ( 'index' in option ) {
                    idx= option['index'];
                } else {
                    idx= this.Index(option);
                }

                if ( idx === -1 || idx >= moons.length ) {
                    return false;
                }

                moons.splice(idx, 1);

                return true;
            };

            this.Size= function () {
                return moons.length;
            };

            // Export as obj

            this.toString= function () {
                "use strict";

                return JSON.stringify(this.Export());
            };

        };
        return MoonSet;
    })();

    return CustomCalendar;
})();