# Uses CircuitPython - Adafruit MagTag
# .vscode/settings.json
# {
#   "circuitpython.board.version": null,
#   "circuitpython.board.vid": "0x239A",
#   "circuitpython.board.pid": "0x80E6",
# }

import ssl
import time

import adafruit_requests
import microcontroller
import socketpool
import wifi

# pylint: disable=no-name-in-module,wrong-import-order
try:
    from secrets import secrets
except ImportError:
    print("WiFi secrets are kept in secrets.py, please add them there!")
    raise

requests = None


def connect_to_wifi() -> None:
    """Connect to the wifi"""
    print(f"Connecting to {secrets['ssid']}")
    wifi.radio.connect(secrets["ssid"], secrets["password"])
    print(f"Connected to {secrets['ssid']}!")

def init_request_pool() -> None:
    """Initialise a connection pool for making HTTP requests"""
    global requests
    pool = socketpool.SocketPool(wifi.radio)
    requests = adafruit_requests.Session(pool, ssl.create_default_context())

def run():
    """Run the main code inner loop"""
    global requests
    while True:
        try:
            print(f"Fetching text from {secrets['gtfs_url']}")
            response = requests.get(secrets["gtfs_url"]).json()
            response.close()
            time.sleep(60)
        except Exception as e:
            print("Error:\n", str(e))
            print("Resetting microcontroller in 10 seconds")
            time.sleep(10)
            microcontroller.reset()
        time.sleep(5)

def main():
    connect_to_wifi()
    requests = init_request_pool()
    run()

main()
