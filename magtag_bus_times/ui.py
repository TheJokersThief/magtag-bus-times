import time

import displayio
import terminalio
from adafruit_display_text import label

from magtag_bus_times.system import CustomMagTag

DAYS = ("Monday", "Tuesday", "Wednesday", "Thursday", "Friday", "Saturday", "Sunday")
MONTHS = (
    "January",
    "February",
    "March",
    "April",
    "May",
    "June",
    "July",
    "August",
    "September",
    "October",
    "November",
    "December",
)


def make_banner(x=0, y=0):
    """Make a single future forecast info banner group."""
    day_of_week = label.Label(terminalio.FONT, text="DAY", color=0x000000)
    day_of_week.anchor_point = (0, 0.5)
    day_of_week.anchored_position = (0, 10)

    # icon = displayio.TileGrid(
    #     icons_small_bmp,
    #     pixel_shader=icons_small_pal,
    #     x=25,
    #     y=0,
    #     width=1,
    #     height=1,
    #     tile_width=20,
    #     tile_height=20,
    # )

    day_temp = label.Label(terminalio.FONT, text="+100F", color=0x000000)
    day_temp.anchor_point = (0, 0.5)
    day_temp.anchored_position = (50, 10)

    group = displayio.Group(x=x, y=y)
    group.append(day_of_week)
    # group.append(icon)
    group.append(day_temp)

    return group


class UI:
    def __init__(self, magtag: CustomMagTag):
        # Placeholder
        city = "Cork"

        self.today_date = label.Label(terminalio.FONT, text="?" * 30, color=0x000000)
        self.today_date.anchor_point = (0, 0)
        self.today_date.anchored_position = (15, 13)

        self.city_name = label.Label(terminalio.FONT, text=city, color=0x000000)
        self.city_name.anchor_point = (0, 0)
        self.city_name.anchored_position = (15, 24)

        self.today_morn_temp = label.Label(
            terminalio.FONT, text="+100F", color=0x000000
        )
        self.today_morn_temp.anchor_point = (0.5, 0)
        self.today_morn_temp.anchored_position = (118, 59)

        self.today_day_temp = label.Label(terminalio.FONT, text="+100F", color=0x000000)
        self.today_day_temp.anchor_point = (0.5, 0)
        self.today_day_temp.anchored_position = (149, 59)

        self.today_night_temp = label.Label(
            terminalio.FONT, text="+100F", color=0x000000
        )
        self.today_night_temp.anchor_point = (0.5, 0)
        self.today_night_temp.anchored_position = (180, 59)

        self.today_humidity = label.Label(terminalio.FONT, text="100%", color=0x000000)
        self.today_humidity.anchor_point = (0, 0.5)
        self.today_humidity.anchored_position = (105, 95)

        self.today_wind = label.Label(terminalio.FONT, text="99m/s", color=0x000000)
        self.today_wind.anchor_point = (0, 0.5)
        self.today_wind.anchored_position = (155, 95)

        self.today_sunrise = label.Label(
            terminalio.FONT, text="12:12 PM", color=0x000000
        )
        self.today_sunrise.anchor_point = (0, 0.5)
        self.today_sunrise.anchored_position = (45, 117)

        self.today_sunset = label.Label(
            terminalio.FONT, text="12:12 PM", color=0x000000
        )
        self.today_sunset.anchor_point = (0, 0.5)
        self.today_sunset.anchored_position = (130, 117)

        self.today_banner = displayio.Group()
        self.today_banner.append(self.today_date)
        self.today_banner.append(self.city_name)
        # self.today_banner.append(self.today_icon)
        self.today_banner.append(self.today_morn_temp)
        self.today_banner.append(self.today_day_temp)
        self.today_banner.append(self.today_night_temp)
        self.today_banner.append(self.today_humidity)
        self.today_banner.append(self.today_wind)
        self.today_banner.append(self.today_sunrise)
        self.today_banner.append(self.today_sunset)

        future_banners = [
            make_banner(x=210, y=18),
            make_banner(x=210, y=39),
            make_banner(x=210, y=60),
            make_banner(x=210, y=81),
            make_banner(x=210, y=102),
        ]

        magtag.splash.append(self.today_banner)
        for future_banner in future_banners:
            magtag.splash.append(future_banner)

    def temperature_text(self, tempK):
        return "{:3.0f}C".format(tempK - 273.15)

    def wind_text(self, speedms):
        return "{:3.0f}m/s".format(speedms)

    def update_banner(self, banner, data):
        """Update supplied forecast banner with supplied data."""
        banner[0].text = DAYS[time.localtime(data["dt"]).tm_wday][:3].upper()
        # banner[1][0] = ICON_MAP.index(data["weather"][0]["icon"][:2])
        banner[2].text = self.temperature_text(data["temp"]["day"])

    def update_today(self, data, tz_offset=0):
        """Update today info banner."""
        date = time.localtime(data["dt"])
        sunrise = time.localtime(data["sunrise"] + tz_offset)
        sunset = time.localtime(data["sunset"] + tz_offset)

        self.today_date.text = "{} {} {}, {}".format(
            DAYS[date.tm_wday].upper(),
            MONTHS[date.tm_mon - 1].upper(),
            date.tm_mday,
            date.tm_year,
        )
        # self.today_icon[0] = ICON_MAP.index(data["weather"][0]["icon"][:2])
        self.today_morn_temp.text = self.temperature_text(data["temp"]["morn"])
        self.today_day_temp.text = self.temperature_text(data["temp"]["day"])
        self.today_night_temp.text = self.temperature_text(data["temp"]["night"])
        self.today_humidity.text = "{:3d}%".format(data["humidity"])
        self.today_wind.text = self.wind_text(data["wind_speed"])
        self.today_sunrise.text = "{:2d}:{:02d} AM".format(
            sunrise.tm_hour, sunrise.tm_min
        )
        self.today_sunset.text = "{:2d}:{:02d} PM".format(
            sunset.tm_hour - 12, sunset.tm_min
        )
