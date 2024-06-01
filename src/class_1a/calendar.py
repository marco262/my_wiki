from typing import Tuple, Iterator, Dict, List

EVENT_LIST: Dict[int, Dict[str, Dict[int, List[Dict[str, str]]]]] = {
    1495: {
        "Eleint": {
            21: [
                {"name": "Fall Equinox", "type": "equinox"},
                {"name": "Orientation"},
            ],
        },
    }
}

MONTHS = {
    "Hammer": {"days": 30},
    "Alturiak": {"days": 30},
    "Ches": {"days": 30},
    "Tarsakh": {"days": 30},
    "Mirtul": {"days": 30},
    "Kythorn": {"days": 30},
    "Flamerule": {"days": 30},
    "Eleasis": {"days": 30},
    "Eleint": {"days": 30},
    "Marpenoth": {"days": 30},
    "Uktar": {"days": 30},
    "Nightal": {"days": 30},
}

WEEKDAYS = [
    "First",
    "Second",
    "Third",
    "Fourth",
    "Fifth",
    "Sixth",
    "Seventh",
    "Eighth",
    "Ninth",
    "Tenth",
]

first_year = 1495
first_month = "Hammer"
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
            for _ in WEEKDAYS:
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
                if current_day > MONTHS[current_month]["days"]:
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
    month_names = list(MONTHS.keys())
    if month == month_names[-1]:
        return year + 1, month_names[0]
    return year, month_names[month_names.index(month) + 1]


def next_moon_phase(moon_phase: str) -> str:
    return moon_phases[(moon_phases.index(moon_phase) + 1) % len(moon_phases)]


def get_events(current_year: int, current_month: str, current_day: int) -> list:
    if current_year in EVENT_LIST:
        year = EVENT_LIST[current_year]
        if current_month in year:
            month = year[current_month]
            return month.get(current_day, [])
    return []
