let  CustomCalendarData = {
    "monthSet": {
        "months": [{
            "name": "Abadius",
            "nameShort": "Aba",
            "nameAbbrev": "A",
            "days": 31
        }, {"name": "Calistril", "nameShort": "Cal", "nameAbbrev": "C", "days": 28}, {
            "name": "Pharast",
            "nameShort": "Phar",
            "nameAbbrev": "P",
            "days": 31
        }, {"name": "Gozran", "nameShort": "Goz", "nameAbbrev": "G", "days": 30}, {
            "name": "Desnus",
            "nameShort": "Des",
            "nameAbbrev": "D",
            "days": 31
        }, {"name": "Sarenith", "nameShort": "Sar", "nameAbbrev": "S", "days": 30}, {
            "name": "Erastus",
            "nameShort": "Eras",
            "nameAbbrev": "E",
            "days": 31
        }, {"name": "Arodus", "nameShort": "Aro", "nameAbbrev": "Ar", "days": 31}, {
            "name": "Rova",
            "nameShort": "Rov",
            "nameAbbrev": "R",
            "days": 30
        }, {"name": "Lamashan", "nameShort": "Lam", "nameAbbrev": "L", "days": 31}, {
            "name": "Neth",
            "nameShort": "Neth",
            "nameAbbrev": "N",
            "days": 30
        }, {"name": "Kuthona", "nameShort": "Kuth", "nameAbbrev": "K", "days": 31}], "leapMonth": 1
    },
    "weekdaySet": {
        "weekdays": [{"name": "Sunday", "nameShort": "Sun", "nameAbbrev": "Su"}, {
            "name": "Moonday",
            "nameShort": "Moon",
            "nameAbbrev": "M"
        }, {"name": "Toilday", "nameShort": "Toil", "nameAbbrev": "T"}, {
            "name": "Wealday",
            "nameShort": "Weal",
            "nameAbbrev": "W"
        }, {"name": "Oathday", "nameShort": "Oath", "nameAbbrev": "O"}, {
            "name": "Fireday",
            "nameShort": "Fire",
            "nameAbbrev": "F"
        }, {"name": "Starday", "nameShort": "Star", "nameAbbrev": "St"}]
    },
    "holidaySet": {
        "holidays": [
            {
                "name": "New Year",
                "rule": "NthDayOfMonth",
                "parameters": {"month": "0", "n": "1"}
            },
            // {
            //     "name": "Foundation Day",
            //     "rule": "NthDayOfMonth",
            //     "parameters": {"n": "1", "month": "0"},
            //     "observedBy": "Absalom, Milani",
            //     "category": "Regional"
            // },
            // {
            //     "name": "Merrymead",
            //     "rule": "NthDayOfMonth",
            //     "parameters": {"n": "2", "month": "1"}
            // },
            // {
            //     "name": "Loyalty Day",
            //     "rule": "NthDayOfMonth",
            //     "parameters": {"n": "19", "month": "1"},
            //     "observedBy": "Cheliax, Asmodeus",
            //     "category": "Regional"
            // }, {
            //     "name": "Batul al-Alim",
            //     "rule": "NthWeekdayOfMonth",
            //     "parameters": {"n": "-1", "weekday": "4", "month": "1"},
            //     "observedBy": "Qadira",
            //     "category": "Regional"
            // },
            {
                "name": "Leap Day",
                "rule": "NthDayOfMonth",
                "parameters": {"n": "29", "month": "1"}
            },
            // {
            //     "name": "Day of Bones",
            //     "rule": "NthDayOfMonth",
            //     "parameters": {"n": "5", "month": "2"},
            //     "observedBy": "Pharasma",
            //     "category": "Religious"
            // }, {
            //     "name": "Kaliashahrim",
            //     "rule": "NthDayOfMonth",
            //     "parameters": {"n": "13", "month": "2"},
            //     "observedBy": "Qadira",
            //     "category": "Regional"
            // }, {
            //     "name": "Conquest Day",
            //     "rule": "NthDayOfMonth",
            //     "parameters": {"n": "26", "month": "2"},
            //     "observedBy": "Nex",
            //     "category": "Regional"
            // }, {
            //     "name": "Currentseve",
            //     "rule": "NthDayOfMonth",
            //     "parameters": {"n": "7", "month": "3"},
            //     "observedBy": "Gozreh",
            //     "category": "Religious"
            // }, {
            //     "name": "Taxfest",
            //     "rule": "NthDayOfMonth",
            //     "parameters": {"n": "15", "month": "3"},
            //     "observedBy": "Abadar, Brigh",
            //     "category": "Religious"
            // }, {
            //     "name": "Wrights of Augustana Begins",
            //     "rule": "NthDayOfMonth",
            //     "parameters": {"n": "16", "month": "3"},
            //     "observedBy": "Augustana (Andoran) Brigh",
            //     "category": "Local"
            // }, {
            //     "name": "Wrights of Augustana Ends",
            //     "rule": "NthDayOfMonth",
            //     "parameters": {"n": "30", "month": "3"},
            //     "observedBy": "Augustana (Andoran)",
            //     "category": "Local"
            // }, {
            //     "name": "Ascendance Day",
            //     "rule": "NthDayOfMonth",
            //     "parameters": {"n": "2", "month": "4"},
            //     "observedBy": "Norgorber",
            //     "category": "Religious"
            // }, {
            //     "name": "Old-Mage Day",
            //     "rule": "NthDayOfMonth",
            //     "parameters": {"n": "13", "month": "4"},
            //     "observedBy": "Nantambu (Mwangi Expanse)",
            //     "category": "Local"
            // }, {
            //     "name": "Goblin Flea Market",
            //     "rule": "NthWeekdayOfMonth",
            //     "parameters": {"n": "-1", "weekday": "0", "month": "4"},
            //     "observedBy": "Andoran",
            //     "category": "Regional"
            // }, {
            //     "name": "Liberty Day",
            //     "rule": "NthDayOfMonth",
            //     "parameters": {"n": "3", "month": "5"},
            //     "observedBy": "Andoran, Milani",
            //     "category": "Regional"
            // }, {
            //     "name": "Burning Blades",
            //     "rule": "NthDayOfMonth",
            //     "parameters": {"n": "10", "month": "5"},
            //     "observedBy": "Sarenrae",
            //     "category": "Religious"
            // }, {
            //     "name": "Talon Tag",
            //     "rule": "NthDayOfMonth",
            //     "parameters": {"n": "21", "month": "5"},
            //     "observedBy": "Andoran",
            //     "category": "Regional"
            // }, {
            //     "name": "Goblin Flea Market",
            //     "rule": "NthWeekdayOfMonth",
            //     "parameters": {"n": "-1", "weekday": "0", "month": "5"},
            //     "observedBy": "Andoran",
            //     "category": "Regional"
            // }, {
            //     "name": "Archerfeast",
            //     "rule": "NthDayOfMonth",
            //     "parameters": {"n": "3", "month": "6"},
            //     "observedBy": "Erastil",
            //     "category": "Religious"
            // }, {
            //     "name": "Founding Festival",
            //     "rule": "NthDayOfMonth",
            //     "parameters": {"n": "14", "month": "6"},
            //     "observedBy": "Korvosa (Varisia)",
            //     "category": "Local"
            // }, {
            //     "name": "Burning Night",
            //     "rule": "NthDayOfMonth",
            //     "parameters": {"n": "17", "month": "6"},
            //     "observedBy": "Razmiran",
            //     "category": "Regional"
            // }, {
            //     "name": "Kianidi Festival Begins",
            //     "rule": "NthDayOfMonth",
            //     "parameters": {"n": "15", "month": "6"},
            //     "observedBy": "Garund",
            //     "category": "Regional"
            // }, {
            //     "name": "Kianidi Festival Ends",
            //     "rule": "NthDayOfMonth",
            //     "parameters": {"n": "21", "month": "6"},
            //     "observedBy": "Garund",
            //     "category": "Regional"
            // }, {
            //     "name": "Goblin Flea Market",
            //     "rule": "NthWeekdayOfMonth",
            //     "parameters": {"n": "-1", "weekday": "0", "month": "6"},
            //     "observedBy": "Andoran",
            //     "category": "Regional"
            // }, {
            //     "name": "First Crusader Day",
            //     "rule": "NthDayOfMonth",
            //     "parameters": {"n": "6", "month": "7"},
            //     "observedBy": "Mendev",
            //     "category": "Regional"
            // }, {
            //     "name": "Day of Silenced Whispers",
            //     "rule": "NthDayOfMonth",
            //     "parameters": {"n": "9", "month": "7"},
            //     "observedBy": "Ustalav",
            //     "category": "Regional"
            // }, {
            //     "name": "Armasse",
            //     "rule": "NthDayOfMonth",
            //     "parameters": {"n": "16", "month": "7"},
            //     "observedBy": "Aroden, Iomedae, Milani",
            //     "category": "Religious"
            // }, {
            //     "name": "Silverglazer Sunday",
            //     "rule": "NthWeekdayOfMonth",
            //     "parameters": {"n": "-1", "weekday": "0", "month": "7"},
            //     "observedBy": "Andoran",
            //     "category": "Regional"
            // }, {
            //     "name": "Silverglazer Sunday",
            //     "rule": "NthWeekdayOfMonth",
            //     "parameters": {"n": "1", "weekday": "0", "month": "8"},
            //     "observedBy": "Andoran",
            //     "category": "Regional"
            // }, {
            //     "name": "Signing Day",
            //     "rule": "NthWeekdayOfMonth",
            //     "parameters": {"n": "2", "weekday": "4", "month": "8"},
            //     "observedBy": "Andoran, Cheliax, Galt, Isger",
            //     "category": "Regional"
            // }, {
            //     "name": "Day of the Inheritor",
            //     "rule": "NthDayOfMonth",
            //     "parameters": {"n": "19", "month": "8"},
            //     "observedBy": "Iomedae",
            //     "category": "Religious"
            // },
            // {
            //     "name": "Harvest Feast",
            //     "rule": "NthWeekdayOfMonth",
            //     "parameters": {"n": "2", "weekday": "1", "month": "9"}
            // },
            // {
            //     "name": "Ascendance Day",
            //     "rule": "NthDayOfMonth",
            //     "parameters": {"n": "6", "month": "9"},
            //     "observedBy": "Iomedae",
            //     "category": "Religious"
            // }, {
            //     "name": "Jestercap",
            //     "rule": "NthDayOfMonth",
            //     "parameters": {"n": "27", "month": "9"},
            //     "observedBy": "Andoran, Druma, Taldor",
            //     "category": "Regional"
            // }, {
            //     "name": "All Kings Day",
            //     "rule": "NthDayOfMonth",
            //     "parameters": {"n": "5", "month": "10"},
            //     "observedBy": "Galt",
            //     "category": "Regional"
            // }, {
            //     "name": "Abjurant Day",
            //     "rule": "NthDayOfMonth",
            //     "parameters": {"n": "8", "month": "10"},
            //     "observedBy": "Nethys",
            //     "category": "Religious"
            // }, {
            //     "name": "Even-Tongued Day",
            //     "rule": "NthDayOfMonth",
            //     "parameters": {"n": "14", "month": "10"},
            //     "observedBy": "Andoran, Cheliax, Galt, Isger",
            //     "category": "Regional"
            // }, {
            //     "name": "Evoking Day",
            //     "rule": "NthDayOfMonth",
            //     "parameters": {"n": "18", "month": "10"},
            //     "observedBy": "Nethys",
            //     "category": "Religious"
            // }, {
            //     "name": "Seven Veils (IS World Guide)",
            //     "rule": "NthDayOfMonth",
            //     "parameters": {"n": "23", "month": "10"},
            //     "observedBy": "Sivanah"
            // }, {
            //     "name": "Transmutatum",
            //     "rule": "NthDayOfMonth",
            //     "parameters": {"n": "28", "month": "10"},
            //     "observedBy": "Nethys",
            //     "category": "Religious"
            // },
            // {
            //     "name": "Winter Week",
            //     "rule": "NthWeekOfMonth",
            //     "parameters": {"n": "2", "month": "11"}
            // },
            // {
            //     "name": "Ascendance Day",
            //     "rule": "NthDayOfMonth",
            //     "parameters": {"n": "11", "month": "11"},
            //     "observedBy": "Cayden Cailean",
            //     "category": "Religious"
            // },
            // {
            //     "name": "Night of the Pale",
            //     "rule": "NthDayOfMonth",
            //     "parameters": {"n": "31", "month": "11"}
            // },
            // {
            //     "name": "Firstbloom",
            //     "rule": "NthDayOfSeason",
            //     "parameters": {"n": "1", "season": "0"},
            //     "observedBy": "Gozreh",
            //     "category": "Religious"
            // }, {
            //     "name": "Planting Week",
            //     "rule": "NthDayOfSeason",
            //     "parameters": {"n": "1", "season": "0"},
            //     "observedBy": "Erastil",
            //     "category": "Religious"
            // }, {
            //     "name": "Ritual of Stardust",
            //     "rule": "NthDayOfSeason",
            //     "parameters": {"n": "1", "season": "1"},
            //     "observedBy": "Desna",
            //     "category": "Religious"
            // }, {
            //     "name": "Sunwrought Festival",
            //     "rule": "NthDayOfSeason",
            //     "parameters": {"n": "1", "season": "1"},
            //     "observedBy": "Sarenrae, Brigh",
            //     "category": "Religious"
            // }, {
            //     "name": "Harvest Feast",
            //     "rule": "NthDayOfSeason",
            //     "parameters": {"n": "1", "season": "2"},
            //     "observedBy": "Erastil",
            //     "category": "Religious"
            // },
            {
                "name": "Swallowtail Festival",
                "rule": "NthDayOfSeason",
                "parameters": {"n": "1", "season": "2"},
                "category": "Local"
            },
            // {
            //     "name": "Crystalhue",
            //     "rule": "NthDayOfSeason",
            //     "parameters": {"n": "1", "season": "3"},
            //     "observedBy": "Shelyn",
            //     "category": "Religious"
            // }, {
            //     "name": "Ritual of Stardust",
            //     "rule": "NthDayOfSeason",
            //     "parameters": {"n": "1", "season": "3"},
            //     "observedBy": "Desna",
            //     "category": "Religious"
            // },
            // {
            //     "name": "Longnight",
            //     "rule": "PhaseOfMoonInMonth",
            //     "parameters": {"moon": "0", "month": "0", "phase": "3"}
            // },
            // {
            //     "name": "Remembrance Moon",
            //     "rule": "PhaseOfMoonInMonth",
            //     "parameters": {"moon": "0", "month": "4", "phase": "3"},
            //     "observedBy": "Lastwall, Ustalav, Iomedae",
            //     "category": "Regional"
            // }, {
            //     "name": "Admani Upastuti",
            //     "rule": "PhaseOfMoonInMonth",
            //     "parameters": {"moon": "0", "month": "9", "phase": "3"},
            //     "observedBy": "Jalmeray, Vudra",
            //     "category": "Regional"
            // }, {
            //     "name": "Turning Day",
            //     "rule": "NthDayOfMonth",
            //     "parameters": {"n": "31", "month": "11"},
            //     "observedBy": "Alseta",
            //     "category": "Religious"
            // }, {
            //     "name": "Time of Reminiscence",
            //     "rule": "NthDayOfSeason",
            //     "parameters": {"n": "1", "season": "3"},
            //     "observedBy": "Apsu",
            //     "category": "Religious"
            // }, {
            //     "name": "Wanderer's Escape",
            //     "rule": "NthDayOfSeason",
            //     "parameters": {"n": "1", "season": "1"},
            //     "observedBy": "Apsu",
            //     "category": "Religious"
            // }, {
            //     "name": "Harmattan Revel",
            //     "rule": "NthDayOfSeason",
            //     "parameters": {"n": "1", "season": "3"},
            //     "observedBy": "Besmara",
            //     "category": "Religious"
            // }, {
            //     "name": "The Final Day",
            //     "rule": "NthDayOfMonth",
            //     "parameters": {"n": "31", "month": "11"},
            //     "observedBy": "Groetus",
            //     "category": "Religious"
            // }, {
            //     "name": "Winterbloom",
            //     "rule": "NthDayOfMonth",
            //     "parameters": {"n": "15", "month": "11"},
            //     "observedBy": "Naderi",
            //     "category": "Religious"
            // }, {
            //     "name": "Seven Veils (IS Faiths)",
            //     "rule": "NthDayOfMonth",
            //     "parameters": {"n": "7", "month": "10"},
            //     "observedBy": "Sivanah"
            // }, {
            //     "name": "Day of Gritted Teeth",
            //     "rule": "NthDayOfMonth",
            //     "parameters": {"n": "5", "month": "2"},
            //     "observedBy": "Zyphus",
            //     "category": "Religious"
            // }, {
            //     "name": "The Inheritor's Ascendance",
            //     "rule": "NthDayOfMonth",
            //     "parameters": {"n": "1", "month": "7"},
            //     "observedBy": "Iomedae",
            //     "category": "Religious"
            // }, {
            //     "name": "Candlemark",
            //     "rule": "NthDayOfSeason",
            //     "parameters": {"n": "1", "season": "3"},
            //     "observedBy": "Sarenrae",
            //     "category": "Religious"
            // }, {
            //     "name": "Pjallarane Day",
            //     "rule": "NthDayOfMonth",
            //     "parameters": {"n": "1", "month": "0"},
            //     "observedBy": "Irrisen",
            //     "category": "Regional"
            // }, {
            //     "name": "Vault Day",
            //     "rule": "NthDayOfMonth",
            //     "parameters": {"n": "6", "month": "0"},
            //     "observedBy": "Abadar",
            //     "category": "Religious"
            // }, {
            //     "name": "Ruby Prince's Birthday",
            //     "rule": "NthDayOfMonth",
            //     "parameters": {"n": "20", "month": "0"},
            //     "observedBy": "Osirion",
            //     "category": "Regional"
            // }, {
            //     "name": "Fateless Day",
            //     "rule": "NthDayOfMonth",
            //     "parameters": {"n": "29", "month": "1"},
            //     "observedBy": "Mahathallah",
            //     "category": "Religious"
            // }, {
            //     "name": "Golemwalk Parade",
            //     "rule": "NthWeekdayOfMonth",
            //     "parameters": {"n": "1", "weekday": "0", "month": "2"},
            //     "observedBy": "Magnimar (Varisia)",
            //     "category": "Local"
            // }, {
            //     "name": "Sable Company Founding Day",
            //     "rule": "NthDayOfMonth",
            //     "parameters": {"n": "6", "month": "2"},
            //     "observedBy": "Korvosa (Varisia)",
            //     "category": "Local"
            // }, {
            //     "name": "Night of Tears",
            //     "rule": "NthDayOfMonth",
            //     "parameters": {"n": "7", "month": "2"},
            //     "observedBy": "Solku (Katapesh)",
            //     "category": "Local"
            // }, {
            //     "name": "Days of Wrath",
            //     "rule": "NthDayOfSeason",
            //     "parameters": {"n": "1", "season": "1"},
            //     "observedBy": "Cheliax, Asmodeus",
            //     "category": "Regional"
            // }, {
            //     "name": "First Cut",
            //     "rule": "NthDayOfSeason",
            //     "parameters": {"n": "1", "season": "0"},
            //     "observedBy": "Falcon's Hollow (Andoran)",
            //     "category": "Local"
            // }, {
            //     "name": "Gala of Sails",
            //     "rule": "NthDayOfMonth",
            //     "parameters": {"n": "27", "month": "3"},
            //     "observedBy": "Absalom",
            //     "category": "Regional"
            // }, {
            //     "name": "Eternal Kiss",
            //     "rule": "PhaseOfMoonInMonth",
            //     "parameters": {"phase": "1", "moon": "0", "month": "0"},
            //     "observedBy": "Zon-Kuthon",
            //     "category": "Religious"
            // }, {
            //     "name": "King Erod II's Birthday",
            //     "rule": "NthDayOfMonth",
            //     "parameters": {"n": "16", "month": "1"},
            //     "observedBy": "Korvosa (Varisia)",
            //     "category": "Local"
            // }, {
            //     "name": "Azvadeva Dejal",
            //     "rule": "NthDayOfMonth",
            //     "parameters": {"n": "3", "month": "4"},
            //     "observedBy": "Gruhastha",
            //     "category": "Religious"
            // }, {
            //     "name": "Angel Day",
            //     "rule": "NthDayOfMonth",
            //     "parameters": {"n": "31", "month": "4"},
            //     "observedBy": "Magnimar (Varisia)",
            //     "category": "Local"
            // }, {
            //     "name": "Breaching Festival",
            //     "rule": "NthWeekdayOfMonth",
            //     "parameters": {"n": "-1", "weekday": "0", "month": "4"},
            //     "observedBy": "Korvosa (Varisia)",
            //     "category": "Local"
            // },
            // {
            //     "name": "First Day of Summer",
            //     "rule": "NthDayOfSeason",
            //     "parameters": {"n": "1", "season": "1"},
            //     "observedBy": "Sarenrae",
            //     "category": "Religious"
            // },
            // {
            //     "name": "Day of Destiny Festival",
            //     "rule": "NthDayOfMonth",
            //     "parameters": {"n": "3", "month": "5"},
            //     "observedBy": "Korvosa (Varisia)",
            //     "category": "Local"
            // }, {
            //     "name": "Riverwind Festival",
            //     "rule": "NthDayOfMonth",
            //     "parameters": {"n": "22", "month": "5"},
            //     "observedBy": "Korvosa (Varisia)",
            //     "category": "Local"
            // }, {
            //     "name": "Festival of the Ruling Sun",
            //     "rule": "NthDayOfSeason",
            //     "parameters": {"n": "1", "season": "1"},
            //     "observedBy": "Shizuru",
            //     "category": "Religious"
            // }, {
            //     "name": "Founder's Folly",
            //     "rule": "NthDayOfSeason",
            //     "parameters": {"n": "1", "season": "1"},
            //     "observedBy": "Ular Kel (Karazh)",
            //     "category": "Local"
            // }, {
            //     "name": "Harvest Bounty Festival",
            //     "rule": "NthDayOfSeason",
            //     "parameters": {"n": "1", "season": "1"},
            //     "observedBy": "Segada (Degasi)",
            //     "category": "Local"
            // }, {
            //     "name": "Runefeast",
            //     "rule": "NthDayOfSeason",
            //     "parameters": {"n": "1", "season": "1"},
            //     "observedBy": "Magrim",
            //     "category": "Religious"
            // }, {
            //     "name": "Founding Day",
            //     "rule": "NthDayOfMonth",
            //     "parameters": {"n": "10", "month": "7"},
            //     "observedBy": "Ilsurian",
            //     "category": "Local"
            // }, {
            //     "name": "Saint Alika's Birthday",
            //     "rule": "NthDayOfMonth",
            //     "parameters": {"n": "31", "month": "7"},
            //     "observedBy": "Korvosa (Varisia)",
            //     "category": "Local"
            // },
            // {
            //     "name": "Last Day of Summer",
            //     "rule": "NthDayOfSeason",
            //     "parameters": {"n": "-1", "season": "1"},
            //     "observedBy": "Sarenrae",
            //     "category": "Religious"
            // },
            // {
            //     "name": "Crabfest",
            //     "rule": "NthWeekdayOfMonth",
            //     "parameters": {"n": "1", "weekday": "3", "month": "8"},
            //     "observedBy": "Korvosa (Varisia)",
            //     "category": "Local"
            // }, {
            //     "name": "Feast of Szurpade",
            //     "rule": "NthDayOfMonth",
            //     "parameters": {"n": "26", "month": "8"},
            //     "observedBy": "Irrisen",
            //     "category": "Regional"
            // }, {
            //     "name": "Day of Sundering",
            //     "rule": "NthDayOfMonth",
            //     "parameters": {"n": "29", "month": "8"},
            //     "observedBy": "Ydersius",
            //     "category": "Religious"
            // }, {
            //     "name": "Festival of Night's Return",
            //     "rule": "NthDayOfSeason",
            //     "parameters": {"n": "1", "season": "2"},
            //     "observedBy": "Nidal",
            //     "category": "Regional"
            // }, {
            //     "name": "Waning Light Festival",
            //     "rule": "NthDayOfSeason",
            //     "parameters": {"n": "1", "season": "2"},
            //     "observedBy": "Segada (Degasi)",
            //     "category": "Local"
            // }, {
            //     "name": "Kraken Festival",
            //     "rule": "NthDayOfMonth",
            //     "parameters": {"n": "6", "month": "9"},
            //     "observedBy": "Absalom",
            //     "category": "Local"
            // }, {
            //     "name": "Bastion Day begins",
            //     "rule": "NthDayOfMonth",
            //     "parameters": {"n": "19", "month": "9"},
            //     "observedBy": "Solku (Katapesh)",
            //     "category": "Local"
            // }, {
            //     "name": "Bastion Day ends",
            //     "rule": "NthDayOfMonth",
            //     "parameters": {"n": "20", "month": "9"},
            //     "observedBy": "Solku (Katapesh)",
            //     "category": "Local"
            // }, {
            //     "name": "Allbirth",
            //     "rule": "NthDayOfMonth",
            //     "parameters": {"n": "30", "month": "9"},
            //     "observedBy": "Lamashtu",
            //     "category": "Religious"
            // }, {
            //     "name": "Festival of the Witch",
            //     "rule": "NthDayOfMonth",
            //     "parameters": {"n": "30", "month": "9"},
            //     "observedBy": "Irrisen",
            //     "category": "Regional"
            // }, {
            //     "name": "The Feast of the Survivors",
            //     "rule": "NthWeekdayOfMonth",
            //     "parameters": {"n": "3", "weekday": "1", "month": "9"},
            //     "observedBy": "Nidal, Zon-Kuthon",
            //     "category": "Regional"
            // }, {
            //     "name": "Great Fire Remembrance",
            //     "rule": "NthDayOfMonth",
            //     "parameters": {"month": "10", "n": "13"},
            //     "observedBy": "Korvosa (Varisia)",
            //     "category": "Local"
            // }, {
            //     "name": "Baptism of Ice begins",
            //     "rule": "NthDayOfMonth",
            //     "parameters": {"n": "24", "month": "10"},
            //     "observedBy": "Irrisen",
            //     "category": "Regional"
            // }, {
            //     "name": "Baptism of Ice ends",
            //     "rule": "NthDayOfMonth",
            //     "parameters": {"n": "30", "month": "10"},
            //     "observedBy": "Irrisen",
            //     "category": "Regional"
            // }, {
            //     "name": "The Shadowchaining",
            //     "rule": "NthDayOfMonth",
            //     "parameters": {"n": "1", "month": "11"},
            //     "observedBy": "Nidal, Zon-Kuthon",
            //     "category": "Regional"
            // }, {
            //     "name": "Pseudodragon Festival",
            //     "rule": "NthDayOfMonth",
            //     "parameters": {"n": "7", "month": "11"},
            //     "observedBy": "Korvosa (Varisia)",
            //     "category": "Local"
            // }, {
            //     "name": "Days of Wrath",
            //     "rule": "NthDayOfSeason",
            //     "parameters": {"n": "1", "season": "3"},
            //     "observedBy": "Cheliax, Asmodeus",
            //     "category": "Regional"
            // }, {
            //     "name": "Long Dark Night",
            //     "rule": "NthDayOfSeason",
            //     "parameters": {"n": "1", "season": "3"},
            //     "observedBy": "Segada (Degasi)",
            //     "category": "Local"
            // },
            {
                "name": "Shalelu returns",
                "rule": "NthDayOfMonth",
                "parameters": {"n": "25", "month": "8"},
                "category": "Story"
            },
            {
                "name": "Hemlock leaves for Magnimar",
                "rule": "NthDayOfMonth",
                "parameters": {"n": "26", "month": "8"},
                "category": "Story"
            },
            {
                "name": "Glassworks Fire",
                "rule": "NthDayOfMonth",
                "parameters": {"n": "27", "month": "8"},
                "category": "Story"
            },
            {
                "name": "Hemlock returns (estimated)",
                "rule": "NthDayOfMonth",
                "parameters": {"n": "3", "month": "9"},
                "category": "Story"
            },
        ]
    },
    "moonSet": {
        "moons": [{
            "name": "Somal",
            "period": 29.5,
            "color": "#e8df4d",
            "shadowColor": "#5d591f",
            "firstFull": 26,
            // "fullNames": ["Long", "Fated", "Rebirth", "Flood", "Blossom", "Sweet", "Lover's", "Swarm", "Harvest", "Hunter's", "Black", "Cold"]
        }]
    },
    "leapYearRuleSet": {"leaprules": [{"interval": 8, "isLeap": true}]},
    "seasons": ["spring", "summer", "fall", "winter"],
    "foundingDay": 1,
    "yearMin": 1,
    "name": "Golarion",
    "era": "AR"
};