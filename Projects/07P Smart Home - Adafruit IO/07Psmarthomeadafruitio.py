'''
Smart Home - Adafruit IO
  - Tested with CircuitPython 8.0.0-beta.6

Additional libraries
  https://circuitpython.org/libraries
    - adafruit_requests.mpy
    - simpleio.mpy
    - adafruit_dht.mpy
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
import adafruit_dht
import analogio
import simpleio
import digitalio
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
print("Connected to Adafruit IO✅")

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

# Create feed. Please make sure same as at adafruit IO.
picowTemp_feed = io.get_feed("smarthome.temp")
picowHumi_feed = io.get_feed("smarthome.humi")
picowLux_feed = io.get_feed("smarthome.lux")
picowLig_feed = io.get_feed("smarthome.light")

#  pack feed names into an array for the loop
feed_names = [picowTemp_feed, picowHumi_feed, picowLux_feed, picowLig_feed]
print("Feeds Created✅")

clock = 10

while True:
    try:
        while not wifi.radio.ipv4_address or "0.0.0.0" in repr(wifi.radio.ipv4_address):
            print(f"Reconnecting to WiFi...")
            wifi.radio.connect(ssid, password)
        #  when the clock runs out..
        if clock > 10:
            # Read the Sensors
            dhtval = readDHT22()
            luxval = rtolux()
            temp = round(dhtval[0],2)
            humi = round(dhtval[1],2)
            lux = round(luxval,2)
        
            # Decision Making to Turn ON the Light
            if (lux < 10):
                rly.value = True
                light = 1
                print("Light Turn ON")
            else:
                rly.value = False
                light = 0
                print("Light Turn OFF")
            
            print("\nUpdating Adafruit IO...✅")
            simpleio.tone(buzzer, NOTE_G4, duration=0.2)
            #  send sensor data to respective feeds
            data = [temp, humi, lux, light]
            for z in range(len(data)):
                io.send_data(feed_names[z]["key"], data[z])
                print("sent %0.1f" % data[z])
                time.sleep(1)
            #  print sensor data to the REPL
            print("Temperature = {:.2f} °C".format(temp))
            print("Humidity = {:.2f} %".format(humi))
            print("Lux = {:.2f} lx".format(lux))
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
