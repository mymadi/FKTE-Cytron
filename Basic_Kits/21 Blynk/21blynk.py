"""
Blynk IoT
  - Tested with CircuitPython 8.0.0-beta.6

Additional libraries
  https://circuitpython.org/libraries
  - adafruit_requests.mpy
  - simpleio.mpy

Reference:
[1] https://peppe8o.com/personal-iot-with-blynk-on-raspberry-pi/
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

# Get wifi and blynk token details from a settings.toml file
print(os.getenv("test_env_file"))
ssid = os.getenv("WIFI_SSID")
password = os.getenv("WIFI_PASSWORD")
blynkToken = os.getenv("blynk_auth_token")

# Buzzer
NOTE_G4 = 392
NOTE_C5 = 523
buzzer = board.GP18

# Initialize LED and button.
led = digitalio.DigitalInOut(board.GP0)
led.direction = digitalio.Direction.OUTPUT

# Active LOW Push Button
pb = digitalio.DigitalInOut(board.GP20)
pb.direction = digitalio.Direction.INPUT

# Write API
def write(token,pin,value):
        api_url = "https://blynk.cloud/external/api/update?token="+token+"&"+pin+"="+value
        response = requests.get(api_url)
        if "200" in str(response):
                print("Value successfully updated")
        else:
                print("Could not find the device token or wrong pin format")
# Read API
def read(token,pin):
        api_url = "https://blynk.cloud/external/api/get?token="+token+"&"+pin
        response = requests.get(api_url)
        return response.content.decode()
    
# Connect to Wi-Fi AP
print(f"Initializing...")
wifi.radio.connect(ssid, password)
print("connected!\n")
pool = socketpool.SocketPool(wifi.radio)
print("IP Address: {}".format(wifi.radio.ipv4_address))
print("Connecting to WiFi '{}' ...\n".format(ssid), end="")
requests = adafruit_requests.Session(pool, ssl.create_default_context())

simpleio.tone(buzzer, NOTE_C5, duration=0.1)

while True:
    try:
        while not wifi.radio.ipv4_address or "0.0.0.0" in repr(wifi.radio.ipv4_address):
            print(f"Reconnecting to WiFi...")
            wifi.radio.connect(ssid, password)
            
        # Write Blynk virtual pin V1
        # V1 can be assigned to Virtual Pin Widget on Blynk App
        # Set as Double for floating number
        valV1 = str(round(random.uniform(0,250),2))
        write(blynkToken,"V1",valV1)
        
        # Read Blynk virtual pin V0
        # V0 can be assigned to Button Widget on Blynk App
        button = read(blynkToken,"V0")
        print(button)
        if (button == "1"):
            led.value = True
        else:
            led.value = False
        
        # Write Blynk virtual pin V4
        # V4 can be assigned to LED Widget on Blynk App
        # Set as Integer
        if (pb.value == False):
            write(blynkToken,"V4","1")
            print("LED Turn ON")
        else:
            write(blynkToken,"V4","0")
            print("LED Turn OFF")
        
        time.sleep(5)
        simpleio.tone(buzzer, NOTE_G4, duration=0.1)
        
    except OSError as e:
        print("Failed!\n", e)
        microcontroller.reset()
