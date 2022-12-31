import time

from adafruit_magtag.magtag import MagTag

DEFAULT_SLEEP_TIME_MIN = 5


def go_to_sleep(magtag: MagTag, mins: int = DEFAULT_SLEEP_TIME_MIN):
    """Enter deep sleep for time needed."""
    print(f"Sleeping for {DEFAULT_SLEEP_TIME_MIN} mins")

    seconds_to_sleep = mins * 60
    magtag.exit_and_deep_sleep(seconds_to_sleep)
