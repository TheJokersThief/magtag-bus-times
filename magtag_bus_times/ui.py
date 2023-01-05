import displayio
import terminalio
from adafruit_datetime import datetime
from adafruit_display_shapes.roundrect import RoundRect
from adafruit_display_text import label
from adafruit_magtag import Graphics, MagTag

LINE_ITEM_TEMPL = "{bus_number}  {due_time}  {time_away} [{type}]"


class UI:
    def __init__(self, magtag: MagTag):
        self.magtag = magtag
        self.display = magtag.graphics.display
        self.magtag.splash.append(self.setup())

    def setup(self) -> label.Label:
        setup = displayio.Group()
        setup.append(
            label.Label(
                terminalio.FONT,
                text="Upcoming",
                scale=2,
                color=0x000000,
                anchor_point=(0, 0),
                anchored_position=(185, 5),
            )
        )
        setup.append(RoundRect(175, 5, 115, 120, r=5, outline=0x000000, stroke=2))
        return setup

    def current_time_banner(self, timestamp) -> label.Label:
        dtobj = datetime.fromtimestamp(timestamp)
        current_minute = dtobj.minute
        current_hour = dtobj.hour
        current_time = f"{current_hour:0>2}:{current_minute:0>2}"

        time_group = displayio.Group()
        time_group.append(
            label.Label(
                terminalio.FONT,
                text=current_time,
                scale=1,
                color=0x000000,
                anchor_point=(0, 0),
                anchored_position=(6, 109),
            )
        )
        time_group.append(RoundRect(1, 107, 40, 20, r=5, outline=0x000000, stroke=2))
        self.magtag.splash.append(time_group)

    def add_bus_time_item(
        self, number, due_time, time_away_int, live_or_scheduled, index
    ):
        time_away = time_away_int // 60
        due_time = due_time[:-3]
        right_sidebar = 40

        if index == 0:
            self._add_main_item(number, due_time, time_away, live_or_scheduled)
        else:
            fixed_start_y = 10
            position_y = fixed_start_y + (index * 25)
            aux_item = displayio.Group()
            time = label.Label(
                terminalio.FONT,
                text=due_time,
                scale=2,
                color=0x000000,
                anchor_point=(0, 0),
                anchored_position=(205, position_y),
            )

            aux_item.append(time)
            self.magtag.splash.append(aux_item)

    def render(self):
        self.display.refresh()

    def _add_main_item(self, number, due_time, time_away, live_or_scheduled):
        main_item = displayio.Group()
        next_title = label.Label(
            terminalio.FONT,
            text="NEXT",
            scale=1,
            color=0x000000,
            anchor_point=(0, 0),
            anchored_position=(85, 25),
        )

        time = label.Label(
            terminalio.FONT,
            text=due_time,
            scale=4,
            color=0x000000,
            anchor_point=(0, 0),
            anchored_position=(38, 24),
        )

        distance = label.Label(
            terminalio.FONT,
            text=f"{str(time_away)[:-2]} min".center(15),
            scale=2,
            color=0x000000,
            anchor_point=(0, 0),
            anchored_position=(15, 74),
        )

        item_type = label.Label(
            terminalio.FONT,
            text=f"[{live_or_scheduled}]".center(15),
            scale=1,
            color=0x000000,
            anchor_point=(0, 0),
            anchored_position=(56, 100),
        )
        main_item.append(next_title)
        main_item.append(time)
        main_item.append(distance)
        main_item.append(item_type)
        self.magtag.splash.append(main_item)
