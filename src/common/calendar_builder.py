class CalendarBuilder:

    def __init__(self, month_width, month_height, top_start, left_start, day_width, day_height):
        self.top_start = month_height * top_start
        self.left_start = month_width * left_start
        self.day_width = month_width * day_width
        self.day_height = month_height * day_height

    def get_offsets(self, day):
        return self.top_start + ((day - 1) // 10) * self.day_height, \
               self.left_start + ((day - 1) % 10) * self.day_width

    def day(self, day, text, current_day=False):
        top, left = self.get_offsets(day)
        text = text.replace("\n", "<br>")
        outline = ""
        if current_day:
            outline = " outline: 5px solid green;"
        return '<div class="day" style="top: {}px; left: {}px;{}">{}</div>'.format(top, left, outline, text)

    def add_recurring(self):
        img_url = "https://upload.wikimedia.org/wikipedia/commons/thumb/6/68/Eye_open_font_awesome.svg/1200px-Eye_open_font_awesome.svg.png"
        out = ""
        for i in range(3):
            top, left = self.get_offsets(i * 10 + 1)
            top += self.day_height - 32
            left += 4
            out += f'<img class="neighborhood-watch" src="{img_url}" style="top: {top}px; left: {left}px;">\n'
        return out
