from typing import Tuple, Iterator, Dict, List

event_list: Dict[int, Dict[str, Dict[int, List[Dict[str, str]]]]] = {
    4707: {
        "Rova": {
            23: [
                {"name": "Fall Equinox", "type": "equinox"},
                {"name": "Swallowtail Festival"},
            ],
            25: [
                {"name": "Shalelu returns"},
            ],
            26: [
                {"name": "Hemlock leaves for Magnimar"},
            ],
            27: [
                {"name": "Glassworks Fire"},
                {"name": "Catacombs under Sandpoint discovered"},
            ],
            29: [
                {"name": "[Downtime Starts]"},
                {"name": "Aldern arrives safely at Foxglove Manor"},
            ],
            30: [
                {"name": "Mice experiments ramp up"},
            ],
        },
        "Lamashan": {
            1: [
                {"name": "Yendan Snazzyfeet killed"},
                {"name": "Wrath Pool power rises"},
            ],
            2: [
                {"name": "Hannah's garden destroyed"},
            ],
            3: [
                {"name": "Hemlock returns (est.)"},
                {"name": "Wrath pool destroyed"},
            ],
            4: [
                {"name": "Hemlock returns"},
            ],
            5: [
                {"name": "Heroes raid Thistletop"},
            ],
        }
    }
}

# Calendar data cribbed unapologetically from https://dungeonetics.com/calendar/

months = {
    "Abadius": {"days": 31},
    "Calistril": {"days": 28},
    "Pharast": {"days": 31},
    "Gozran": {"days": 30},
    "Desnus": {"days": 31},
    "Sarenith": {"days": 30},
    "Erastus": {"days": 31},
    "Arodus": {"days": 31},
    "Rova": {"days": 30},
    "Lamashan": {"days": 31},
    "Neth": {"days": 30},
    "Kuthona": {"days": 31},
}

weekdays = [
    "Sunday",
    "Moonday",
    "Toilday",
    "Wealday",
    "Oathday",
    "Fireday",
    "Starday",
]

first_year = 4707
first_month = "Sarenith"
first_moon_day = 1

moon_phase_start = 29.5  # Start with a full moon
moon_phase_period = 29.5
# The first moon phase in the list will show up first
moon_phases = [
    "full-moon",
    "waning-moon",
    "new-moon",
    "waxing-moon",
]


def generate_months(start_year, start_month, end_year, end_month) -> Iterator[Tuple[str, dict]]:
    current_year, current_month = first_year, first_month
    current_day = 1
    current_week = []
    moon_phase = moon_phases[0]
    moon_phase_counter = moon_phase_start
    last_month_to_process = False
    start_returning_months = False
    while True:
        current_year_month = get_month_name(current_year, current_month)
        # Reset weeks
        weeks = []
        # If this week doesn't start on day 1, use the last week for the start of this month
        if current_day > 1:
            weeks.append(current_week)
        # Don't start returning months until start_year and start_month
        if current_year == start_year and current_month == start_month:
            start_returning_months = True
        # Check if this is the last month to process
        if current_year == end_year and current_month == end_month:
            last_month_to_process = True
        month_finished = False
        while not month_finished:
            current_week = []
            for _ in weekdays:
                if moon_phase_counter >= moon_phase_period:
                    moon = moon_phase
                    moon_phase = next_moon_phase(moon_phase)
                    moon_phase_counter -= moon_phase_period
                else:
                    moon = None
                current_week.append({
                    "number": current_day,
                    "month": current_month,
                    "events": get_events(current_year, current_month, current_day),
                    "moon": moon,
                })
                current_day += 1
                moon_phase_counter += 4
                # If we've run out of months in the year, move to next month. But don't stop generating the week yet.
                if current_day > months[current_month]["days"]:
                    current_year, current_month = next_year_month(current_year, current_month)
                    current_day = 1
                    # Set the month loop to stop after this week is done
                    month_finished = True
            weeks.append(current_week)
        if start_returning_months:
            yield current_year_month, weeks
        if last_month_to_process:
            break


def get_month_name(year, month):
    return f"{month}, {year} AR"


def next_year_month(year, month):
    month_names = list(months.keys())
    if month == month_names[-1]:
        return year + 1, month_names[0]
    return year, month_names[month_names.index(month) + 1]


def next_moon_phase(moon_phase: str) -> str:
    return moon_phases[(moon_phases.index(moon_phase) + 1) % len(moon_phases)]


def get_events(current_year: int, current_month: str, current_day: int) -> list:
    if current_year in event_list:
        year = event_list[current_year]
        if current_month in year:
            month = year[current_month]
            return month.get(current_day, [])
    return []