'''
Adafruit IO using CircuitPython on Raspberry Pi Pico W
  - Tested with CircuitPython 8.0.0-beta.6

Additional libraries
  https://circuitpython.org/libraries
    - adafruit_requests.mpy
    - simpleio.mpy
    - adafruit_io
    - adafruit_minimqtt
    - adafruit_register
    - simpleio.mpy

References:
[1] https://learn.adafruit.com/pico-w-wifi-with-circuitpython/pico-w-with-adafruit-io
'''

import os
import time
import ssl
import wifi
import socketpool
import microcontroller
import board
import busio
import adafruit_requests
import analogio
import simpleio
import random
from adafruit_io.adafruit_io import IO_HTTP, AdafruitIO_RequestError

# Get wifi details from a settings.toml file
print(os.getenv("test_env_file"))
ssid = os.getenv("WIFI_SSID")
password = os.getenv("WIFI_PASSWORD")
aio_username = os.getenv("aio_username")
aio_key = os.getenv("aio_key")

# Buzzer
NOTE_G4 = 392
NOTE_C5 = 523
buzzer = board.GP18

# WiFi Connection
wifi.radio.connect(ssid,password)
pool = socketpool.SocketPool(wifi.radio)
requests = adafruit_requests.Session(pool, ssl.create_default_context())
simpleio.tone(buzzer, NOTE_C5, duration=0.1)

# Initialize an Adafruit IO HTTP API object
io = IO_HTTP(aio_username, aio_key, requests)
print("connected to io")

# Create feed. Please make sure same as at adafruit IO.
picowData1_feed = io.get_feed("picow.data1")
picowData2_feed = io.get_feed("picow.data2")

#  pack feed names into an array for the loop
feed_names = [picowData1_feed, picowData2_feed]
print("feeds created")

clock = 300

while True:
    try:
        while not wifi.radio.ipv4_address or "0.0.0.0" in repr(wifi.radio.ipv4_address):
            print(f"Reconnecting to WiFi...")
            wifi.radio.connect(ssid, password)
        #  when the clock runs out..
        if clock > 300:
            # Dummy Value
            data1 = round(random.uniform(25,35),2)
            data2 = round(random.uniform(75,90),2)
            print("\nUpdating Adafruit IO...")
            
            #  send data to respective feeds
            data = [data1, data2]
            for z in range(len(data)):
                io.send_data(feed_names[z]["key"], data[z])
                print("sent %0.1f" % data[z])
                time.sleep(1)
            #  print sensor data to the REPL
            print("Data 1 = {:.2f}".format(data1))
            print("Data 2 = {:.2f}".format(data2))
            print()
            time.sleep(1)
            #  reset clock
            clock = 0
        else:
            clock += 1
    # pylint: disable=broad-except
    #  any errors, reset Pico W
    except Exception as e:
        print("Error:\n", str(e))
        print("Resetting microcontroller in 10 seconds")
        time.sleep(10)
        microcontroller.reset()
    #  delay
    time.sleep(1)
    print(clock)
