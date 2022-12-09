"""
Telegram Bot using CircuitPython on Raspberry Pi Pico W
  - Tested with CircuitPython 8.0.0-beta.4

Additional libraries
  https://circuitpython.org/libraries
  - adafruit_requests.mpy
  - simpleio.mpy

https://getemoji.com/
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

# Get wifi and telegram token details from a .env file
print(os.getenv('test_env_file'))
ssid = os.getenv('WIFI_SSID')
password = os.getenv('WIFI_PASSWORD')
telegrambot = os.getenv('botToken')

# Telegram API url.
API_URL = "https://api.telegram.org/bot" + telegrambot

# Buzzer
NOTE_G4 = 392
NOTE_C5 = 523
NOTE_F4 = 349
NOTE_C2 = 262

buzzer = board.GP18

# Input-Output Initialization
rly = digitalio.DigitalInOut(board.GP0)
rly.direction = digitalio.Direction.OUTPUT

pb = digitalio.DigitalInOut(board.GP20)
pb.direction = digitalio.Direction.INPUT

# DHT22
dht22 = adafruit_dht.DHT22(board.GP7)

# LDR
ldr = analogio.AnalogIn(board.GP26)           
R = 10000                       # ohm resistance value

def init_bot():
    get_url = API_URL
    get_url += "/getMe"
    r = requests.get(get_url)
    return r.json()['ok']

first_read = True
update_id = 0

def read_message():
    global first_read
    global update_id
    
    get_url = API_URL
    get_url += "/getUpdates?limit=1&allowed_updates=[\"message\",\"callback_query\"]"
    if first_read == False:
        get_url += "&offset={}".format(update_id)

    r = requests.get(get_url)
    #print(r.json())
    
    try:
        update_id = r.json()['result'][0]['update_id']
        message = r.json()['result'][0]['message']['text']
        chat_id = r.json()['result'][0]['message']['chat']['id']

        #print("Update ID: {}".format(update_id))
        print("Chat ID: {}\tMessage: {}".format(chat_id, message))

        first_read = False
        update_id += 1
        simpleio.tone(buzzer, NOTE_G4, duration=0.1)
        simpleio.tone(buzzer, NOTE_C5, duration=0.1)
        
        return chat_id, message

    except (IndexError) as e:
        #print("No new message")
        return False, False

def send_message(chat_id, message):
    get_url = API_URL
    get_url += "/sendMessage?chat_id={}&text={}".format(chat_id, message)
    r = requests.get(get_url)
    #print(r.json())

def readDHT22():
    temperature = dht22.temperature
    humidity = dht22.humidity
    temperature = "Temperature: {:.2f} °C".format(temperature)
    humidity = "Humidity: {:.2f} °C".format(humidity)
    return temperature, humidity

def rtolux ():
    raw = ldr.value
    vout = (raw * 3.3) / 65536
    RLDR = (vout*R)/(3.3-vout)
    lux = 500/(RLDR/1000)       # Conversion resitance to lumen
    lux = "Lux: {:.2f} lx".format(lux)
    return lux

#  Connect to Wi-Fi AP
print(f"Initializing...")
wifi.radio.connect(ssid, password)
print("connected!\n")
pool = socketpool.SocketPool(wifi.radio)
print("IP Address: {}".format(wifi.radio.ipv4_address))
print("Connecting to WiFi '{}' ... ".format(ssid), end="")
requests = adafruit_requests.Session(pool, ssl.create_default_context())

if init_bot() == False:
    print("\nTelegram bot failed.")
else:
    print("\nTelegram bot ready!\n")
    simpleio.tone(buzzer, NOTE_C5, duration=0.1)

while True:
    try:
        while not wifi.radio.ipv4_address or "0.0.0.0" in repr(wifi.radio.ipv4_address):
            print(f"Reconnecting to WiFi...")
            wifi.radio.connect(ssid, password)
            
        chat_id, message_in = read_message()
        if message_in == "/start":
            send_message(chat_id,">> Welcome to My Smart Home! 🏡 <<")
            send_message(chat_id,"Choose from one of the following options:")
            send_message(chat_id,"1) Turn ON Light💡:  /Light_ON")
            send_message(chat_id,"2) Turn OFF Light💡: /Light_OFF")
            send_message(chat_id,"3) Read Sensor Data 🌡: /RED")
        elif message_in == "/Light_ON":
            rly.value = True
            send_message(chat_id, "Light Turn ON 💡")
        elif message_in == "/Light_OFF":
            rly.value = False
            send_message(chat_id, "Light Turn OFF 💡")
        elif message_in == "/RED":
            dht22val = readDHT22()
            luxval = rtolux()
            send_message(chat_id, dht22val[0])
            send_message(chat_id, dht22val[1])
            send_message(chat_id, luxval)           
        else:
            send_message(chat_id, "Command is not available 👻")
        
        
    except OSError as e:
        print("Failed!\n", e)
        microcontroller.reset()
