import time

from adafruit_magtag.magtag import MagTag

DEFAULT_SLEEP_TIME_MIN = 5


class CustomMagTag(MagTag):
    def go_to_sleep(self, mins: int = DEFAULT_SLEEP_TIME_MIN):
        """Enter deep sleep for time needed."""
        print(f"Sleeping for {DEFAULT_SLEEP_TIME_MIN} mins")

        seconds_to_sleep = mins * 60
        self.exit_and_deep_sleep(seconds_to_sleep)
