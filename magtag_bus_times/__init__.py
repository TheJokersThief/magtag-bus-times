# Uses CircuitPython - Adafruit MagTag
# .vscode/settings.json
# {
#   "circuitpython.board.version": null,
#   "circuitpython.board.vid": "0x239A",
#   "circuitpython.board.pid": "0x80E6",
# }

import os
import ssl
import time

import adafruit_requests
import microcontroller
import socketpool
import wifi

from magtag_bus_times.system import CustomMagTag
from magtag_bus_times.trips import Trip
from magtag_bus_times.ui import UI

REQUESTS = None
MAX_TRIPS = 2
UPCOMING_ENDPOINT = "/upcoming.json"
WAIT_BETWEEN_RUNS = 300  # In seconds, 300s = 5m

MAGTAG = CustomMagTag()


def connect_to_wifi() -> None:
    """Connect to the wifi"""
    print(f"Connecting to {os.getenv('SSID')}")
    wifi.radio.connect(os.getenv("SSID"), os.getenv("PASSWORD"))
    print(f"Connected to {os.getenv('SSID')}!")


def init_request_pool() -> None:
    """Initialise a connection pool for making HTTP requests"""
    global REQUESTS
    pool = socketpool.SocketPool(wifi.radio)
    REQUESTS = adafruit_requests.Session(pool, ssl.create_default_context())


def run(ui: UI):
    """Run the main code inner loop"""
    try:
        print(f"Fetching text from {os.getenv('GTFS_URL')}{UPCOMING_ENDPOINT}")
        response = REQUESTS.get(os.getenv("GTFS_URL") + UPCOMING_ENDPOINT)
        response.close()

        data = response.json()
        scheduled = [Trip(**trip) for trip in data["upcoming"]][:MAX_TRIPS]
    except Exception as e:
        print("Error:\n", str(e))


def main():
    connect_to_wifi()
    init_request_pool()
    ui = UI(MAGTAG)
    run(ui)
    MAGTAG.go_to_sleep()
    #  entire code will run again after deep sleep cycle
    #  similar to hitting the reset button
