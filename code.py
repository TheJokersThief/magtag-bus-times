# Uses CircuitPython - Adafruit MagTag
# .vscode/settings.json
# {
#   "circuitpython.board.version": null,
#   "circuitpython.board.vid": "0x239A",
#   "circuitpython.board.pid": "0x80E6",
# }

import time
import ssl
import socketpool
import wifi
import adafruit_minimqtt.adafruit_minimqtt as MQTT

# Add a secrets.py to your filesystem that has a dictionary called secrets with "ssid" and
# "password" keys with your WiFi credentials. DO NOT share that file or commit it into Git or other
# source control.
# pylint: disable=no-name-in-module,wrong-import-order
try:
    from secrets import secrets
except ImportError:
    print("WiFi secrets are kept in secrets.py, please add them there!")
    raise


print("Connecting to %s" % secrets["ssid"])
wifi.radio.connect(secrets["ssid"], secrets["password"])
print("Connected to %s!" % secrets["ssid"])

while True:
    print("Loop...")
    time.sleep(5)
