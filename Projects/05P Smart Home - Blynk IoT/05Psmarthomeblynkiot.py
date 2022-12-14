"""
Smart Home - Blynk IoT
  - Tested with CircuitPython 8.0.0-beta.5

Additional libraries
  https://circuitpython.org/libraries
  - adafruit_requests.mpy
  - simpleio.mpy
  - adafruit_dht.mpy

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
import adafruit_dht
import analogio

# Get wifi and blynk token details from a .env file
print(os.getenv('test_env_file'))
ssid = os.getenv('WIFI_SSID')
password = os.getenv('WIFI_PASSWORD')
blynkToken = os.getenv('blynk_auth_tokenSH')

# Buzzer
NOTE_G4 = 392
NOTE_C5 = 523
buzzer = board.GP18

# Input-Output Initialization
rly = digitalio.DigitalInOut(board.GP0)
rly.direction = digitalio.Direction.OUTPUT

# Microwave Radar
rcwl = digitalio.DigitalInOut(board.GP4)
rcwl.direction = digitalio.Direction.INPUT

# DHT22
dht22 = adafruit_dht.DHT22(board.GP7)

# LDR
ldr = analogio.AnalogIn(board.GP26)           
R = 10000                       # ohm resistance value

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

# Batch Write
# Virtual Pin Blynk
pin = ["V0","V1","V2"]
def BatchWrite(token,pin,value):
    batchstr = []
    datalength = len(value)
    print(datalength)
    for i in range(datalength):
        batchs = str(pin[i]+"="+value[i])
        batchstr.append(batchs)
    batchnew = ("&".join(map(str,batchstr)))
    batchnew = str("&"+batchnew)
    print(batchnew)
    api_url = "https://blynk.cloud/external/api/batch/update?token="+token+batchnew    
    #api_url = "https://blynk.cloud/external/api/batch/update?token="+token+"&"+pin[0]+"="+value[0]+"&"+pin[1]+"="+value[1]+"&"+pin[2]+"="+value[2]+"&"+pin[3]+"="+value[3]
    response = requests.get(api_url)
    if "200" in str(response):
            print("Batch: Value successfully updated")
    else:
            print("Could not find the device token or wrong pin format")

# Read DHT22 Sensor
def readDHT22():
    temperature = dht22.temperature
    humidity = dht22.humidity
    return temperature, humidity

# Read LDR Sensor
def rtolux():
    raw = ldr.value
    vout = (raw * 3.3) / 65536
    RLDR = (vout*R)/(3.3-vout)
    lux = 500/(RLDR/1000)       # Conversion resitance to lumen
    return lux

# # Hardware Connected
# def HWstatus(token):
#     api_url = "https://blynk.cloud/external/api/isHardwareConnected?token="+token
#     response = requests.get(api_url)
#     return response.content.decode()

# Connect to Wi-Fi AP
print(f"Initializing...")
wifi.radio.connect(ssid, password)
print("connected!\n")
pool = socketpool.SocketPool(wifi.radio)
print("IP Address: {}".format(wifi.radio.ipv4_address))
print("Connecting to WiFi '{}' ...\n".format(ssid), end="")
requests = adafruit_requests.Session(pool, ssl.create_default_context())

# statusHW = HWstatus(blynkToken)
# print(statusHW)

simpleio.tone(buzzer, NOTE_C5, duration=0.1)

while True:
    try:
        while not wifi.radio.ipv4_address or "0.0.0.0" in repr(wifi.radio.ipv4_address):
            print(f"Reconnecting to WiFi...")
            wifi.radio.connect(ssid, password)
        
        # Read the Sensors
        dhtval = readDHT22()
        luxval = rtolux()
        temp = str(round(dhtval[0],2))
        humi = str(round(dhtval[1],2))
        lux = str(round(luxval,2))
        
        # Batch Write Blynk virtual pin V0-V2
        value = [temp,humi,lux]
        BatchWrite(blynkToken,pin,value)
              
        # Read Blynk virtual pin V3
        # V3 can be assigned to Button Widget on Blynk App
        button = read(blynkToken,"V3")
        print(button)
        if (button == "1"):
            rly.value = True
            print("Light Turn ON")
        else:
            rly.value = False
            print("Light Turn OFF")
        
        # Write Blynk virtual pin V4
        # V4 can be assigned to LED Widget on Blynk App
        # Set as Integer
        if (rcwl.value == True):
            write(blynkToken,"V4","1")
            print("Motion Detected!")
        else:
            write(blynkToken,"V4","0")
            print("No Motion Detected")
        
        time.sleep(5)
        simpleio.tone(buzzer, NOTE_G4, duration=0.1)
        
    except OSError as e:
        print("Failed!\n", e)
        microcontroller.reset()
