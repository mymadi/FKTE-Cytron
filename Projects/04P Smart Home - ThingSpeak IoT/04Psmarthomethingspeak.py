"""
Smart Home - ThingSpeak IoT
  - Tested with CircuitPython 8.0.0-beta.4

Additional libraries
  https://circuitpython.org/libraries
  - adafruit_requests.mpy
  - simpleio.mpy
  - adafruit_dht.mpy

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
import adafruit_dht
import analogio
import random

# Get wifi and thingspeak write API details from a .env file
print(os.getenv('test_env_file'))
ssid = os.getenv('WIFI_SSID')
password = os.getenv('WIFI_PASSWORD')
tswriteAPI = os.getenv('thingspeak_write_api_key')

# Thingspeak API url.
API_URL = "http://api.thingspeak.com"

# Buzzer
NOTE_G4 = 392
NOTE_C5 = 523
buzzer = board.GP18

# Input-Output Initialization
rly = digitalio.DigitalInOut(board.GP0)
rly.direction = digitalio.Direction.OUTPUT

# DHT22
dht22 = adafruit_dht.DHT22(board.GP7)

# LDR
ldr = analogio.AnalogIn(board.GP26)           
R = 10000                       # ohm resistance value


def readDHT22():
    temperature = dht22.temperature
    humidity = dht22.humidity
    return temperature, humidity

def rtolux():
    raw = ldr.value
    vout = (raw * 3.3) / 65536
    RLDR = (vout*R)/(3.3-vout)
    lux = 500/(RLDR/1000)       # Conversion resitance to lumen
    return lux

#  Connect to Wi-Fi AP
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
        # Read the Sensors
        dhtval = readDHT22()
        luxval = rtolux()
        temp = round(dhtval[0],2)
        humi = round(dhtval[1],2)
        lux = round(luxval,2)
        
        # Decision Making to Turn ON the Light
        if (lux < 100):
            rly.value = True
            light = 1
        else:
            rly.value = False
            light = 0
            
        print("\nUpdating Thingspeak...")
        get_url = API_URL + "/update?api_key=" + tswriteAPI + "&field1=" + str(temp) + "&field2=" + str(humi) + "&field3=" + str(lux) + "&field4=" + str(light)
        r = requests.get(get_url)
        print("Temperature (°C):", temp)
        print("Humidity (%):", humi)
        print("Lux (lx):", lux)
        if (light == 1):
            print("Light ON")
        else:
            print("Light OFF")
        print("Data Count:", r.text)
        print("\nOK")
    
        time.sleep(20)  # Free version of Thingspeak only allows one update every 20 seconds.
        simpleio.tone(buzzer, NOTE_C5, duration=0.1)
        simpleio.tone(buzzer, NOTE_G4, duration=0.15)
        
    except OSError as e:
        print("Failed!\n", e)
        microcontroller.reset()
