class CalendarBuilder:

    def __init__(self, top_start=148, left_start=100, day_width=120.3, day_height=125.1):
        self.top_start = top_start
        self.left_start = left_start
        self.day_width = day_width
        self.day_height = day_height

    def get_offsets(self, day):
        return self.top_start + ((day - 1) // 10) * self.day_height, \
               self.left_start + ((day - 1) % 10) * self.day_width

    def day(self, day, text, current_day=False):
        top, left = self.get_offsets(day)
        text = text.replace("\n", "<br>")
        border = ""
        if current_day:
            border = " border: 5px solid green;"
        return '<div class="day" style="top: {}px; left: {}px;{}">{}</div>'.format(top, left, border, text)