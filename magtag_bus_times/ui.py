import terminalio
from adafruit_datetime import datetime
from adafruit_display_text import label
from adafruit_magtag import Graphics, MagTag

LINE_ITEM_TEMPL = "{bus_number}  {due_time}  {time_away} [{type}]"


class UI:
    def __init__(self, magtag: MagTag):
        self.magtag = magtag
        self.display = magtag.graphics.display
        self.magtag.splash.append(self.title_banner())
        # self.magtag.splash.append(self.current_time_banner())

    def title_banner(self) -> label.Label:
        return label.Label(
            terminalio.FONT,
            text="Live Times",
            scale=2,
            color=0x000000,
            anchor_point=(0, 0),
            anchored_position=(5, 5),
        )

    def current_time_banner(self) -> label.Label:
        current_minute = datetime.now().minute
        current_hour = datetime.now().hour
        current_time = f"{current_hour:0>2}:{current_minute:0>2}"
        return label.Label(
            terminalio.FONT,
            text=current_time,
            scale=2,
            color=0x000000,
            anchor_point=(0, 0),
            anchored_position=(self.display.width - 65, 5),
        )

    def add_bus_time_item(
        self, number, due_time, time_away_int, live_or_scheduled, index
    ):
        time_away = time_away_int // 60
        fixed_start_y = 40
        position_y = fixed_start_y + (index * 20)

        item = label.Label(
            terminalio.FONT,
            text=LINE_ITEM_TEMPL.format(
                bus_number=number,
                due_time=due_time,
                time_away=f"{time_away} min",
                type=live_or_scheduled,
            ),
            scale=1,
            color=0x000000,
            anchor_point=(0, 0),
            anchored_position=(5, position_y),
        )
        self.magtag.splash.append(item)

    def render(self):
        self.display.refresh()
