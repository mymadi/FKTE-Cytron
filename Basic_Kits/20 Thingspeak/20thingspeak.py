"""
Thingspaek IoT using CircuitPython on Raspberry Pi Pico W
  - Tested with CircuitPython 8.0.0-beta.6

Additional libraries
  https://circuitpython.org/libraries
  - adafruit_requests.mpy
  - simpleio.mpy

Reference:
[1] https://github.com/CytronTechnologies/MAKER-PI-PICO/blob/main/Example%20Code/CircuitPython/IoT/thingspeak.py
"""

import os
import ipaddress
import wifi
import socketpool
import time
import microcontroller
import board
import digitalio
import simpleio
import adafruit_requests
import ssl
import random

# Get wifi and thingspeak write API details from a settings.toml file
print(os.getenv("test_env_file"))
ssid = os.getenv("WIFI_SSID")
password = os.getenv("WIFI_PASSWORD")
tswriteAPI = os.getenv("thingspeak_write_api_key")

# Thingspeak API url.
API_URL = "http://api.thingspeak.com"

# Buzzer
NOTE_G4 = 392
NOTE_C5 = 523
buzzer = board.GP18

# Connect to Wi-Fi AP
print(f"Initializing...")
wifi.radio.connect(ssid, password)
print("connected!\n")
pool = socketpool.SocketPool(wifi.radio)
print("IP Address: {}".format(wifi.radio.ipv4_address))
print("Connecting to WiFi '{}' ... ".format(ssid), end="")
requests = adafruit_requests.Session(pool, ssl.create_default_context())

simpleio.tone(buzzer, NOTE_C5, duration=0.1)

while True:
    try:
        while not wifi.radio.ipv4_address or "0.0.0.0" in repr(wifi.radio.ipv4_address):
            print(f"Reconnecting to WiFi...")
            wifi.radio.connect(ssid, password)
        
        # Dummy Value
        value1 = round(random.uniform(25,35),2)
        value2 = round(random.uniform(75,90),2)
        value3 = round(random.uniform(8,300),2)
        
        # Updating Thingspeak
        print("\nUpdating Thingspeak...")
        get_url = API_URL + "/update?api_key=" + tswriteAPI + "&field1=" + str(value1) + "&field2=" + str(value2) + "&field3=" + str(value3)
        r = requests.get(get_url)
        print("Value 1:", value1)
        print("Value 2:", value2)
        print("Value 3:", value3)
        print("Data Count:", r.text)
        print("OK")
    
        time.sleep(20)  # Free version of Thingspeak only allows one update every 20 seconds.
        simpleio.tone(buzzer, NOTE_G4, duration=0.1)
        simpleio.tone(buzzer, NOTE_C5, duration=0.15)
        
    except OSError as e:
        print("Failed!\n", e)
        microcontroller.reset()
