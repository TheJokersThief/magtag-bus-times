#!/bin/python

# Uses CircuitPython - Adafruit MagTag
# .vscode/settings.json
# {
#   "circuitpython.board.version": null,
#   "circuitpython.board.vid": "0x239A",
#   "circuitpython.board.pid": "0x80E6",
# }

import ssl

import adafruit_requests
import socketpool
import wifi
from adafruit_magtag.magtag import MagTag

from magtag_bus_times.system import go_to_sleep
from magtag_bus_times.trips import Trip
from magtag_bus_times.ui import UI

# Get wifi details and more from a secrets.py file
try:
    from secrets import secrets
except ImportError:
    print("WiFi secrets are kept in secrets.py, please add them there!")
    raise

REQUESTS = None
MAX_TRIPS = 4
UPCOMING_ENDPOINT = "/upcoming.json"
WAIT_BETWEEN_RUNS = 300  # In seconds, 300s = 5m

MAGTAG = MagTag()


def connect_to_wifi() -> None:
    """Connect to the wifi"""
    print(f"Connecting to {secrets['ssid']}")
    wifi.radio.connect(secrets["ssid"], secrets["password"])
    print(f"Connected to {secrets['ssid']}!")


def init_request_pool() -> None:
    """Initialise a connection pool for making HTTP requests"""
    global REQUESTS
    pool = socketpool.SocketPool(wifi.radio)
    REQUESTS = adafruit_requests.Session(pool, ssl.create_default_context())


def run(ui: UI):
    """Run the main code inner loop"""
    try:
        print(f"Fetching text from {secrets['gtfs_url']}{UPCOMING_ENDPOINT}")
        response = REQUESTS.get(secrets["gtfs_url"] + UPCOMING_ENDPOINT)
        data = response.json()
        response.close()
        scheduled = [Trip(**trip) for trip in data["upcoming"]][:MAX_TRIPS]
        ui.current_time_banner(data["current_timestamp"])

        for index, item in enumerate(scheduled):
            ui.add_bus_time_item(
                item.route, item.dueTime, item.dueInSeconds, item.source, index
            )
        ui.render()
    except Exception as e:
        print("Error:\n", str(e))


def main():
    connect_to_wifi()
    init_request_pool()
    ui = UI(MAGTAG)
    run(ui)
    go_to_sleep(MAGTAG)
    #  entire code will run again after deep sleep cycle
    #  similar to hitting the reset button
