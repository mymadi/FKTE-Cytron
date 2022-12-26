"""
Telegram Bot using CircuitPython on Raspberry Pi Pico W
  - Tested with CircuitPython 8.0.0-beta.6

Additional libraries
  https://circuitpython.org/libraries
  - adafruit_requests.mpy
  - simpleio.mpy
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

# Get wifi details from a settings.toml file
print(os.getenv("test_env_file"))
ssid = os.getenv("WIFI_SSID")
password = os.getenv("WIFI_PASSWORD")
telegrambot = os.getenv("botToken")

# Telegram API url.
API_URL = "https://api.telegram.org/bot" + telegrambot

# Buzzer
NOTE_G4 = 392
NOTE_C5 = 523
buzzer = board.GP18

# Input-Output Initialization
led = digitalio.DigitalInOut(board.LED)
led.direction = digitalio.Direction.OUTPUT

led0 = digitalio.DigitalInOut(board.GP0)
led0.direction = digitalio.Direction.OUTPUT

pb = digitalio.DigitalInOut(board.GP20)
pb.direction = digitalio.Direction.INPUT

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

def blinkGP0():
    led0.value = True
    time.sleep(0.5)
    led0.value = False
    time.sleep(0.5)
    led0.value = True
    time.sleep(0.5)
    led0.value = False

def readIntTemp():
    data = microcontroller.cpu.temperature
    data = "Temperature: {:.2f} °C".format(data)
    return data

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
            send_message(chat_id,"Welcome to Telegram Bot!")
            send_message(chat_id,"Choose from one of the following options:")
            send_message(chat_id,"1) Built-in LED ON:  /LED_ON")
            send_message(chat_id,"2) Built-in LED OFF: /LED_OFF")
            send_message(chat_id,"3) Read Internal Temperature: /Temp")
            send_message(chat_id,"4) Check Push Button Status: /PB")
        elif message_in == "/LED_ON":
            led.value = True
            send_message(chat_id, "LED turn on.")
        elif message_in == "/LED_OFF":
            led.value = False
            send_message(chat_id, "LED turn off.")
        elif message_in == "/LED0_BLK":
            blinkGP0()
            send_message(chat_id, "Blink LED GP0")
        elif message_in == "/Temp":
            temp = readIntTemp()
            send_message(chat_id, temp)
            blinkGP0()
        elif message_in == "/PB":
            if (pb.value == False):
                send_message(chat_id, "Push Button Pressed")
            else:
                send_message(chat_id, "Push Button X Pressed")            
        else:
            send_message(chat_id, "Command is not available.")
        
        
    except OSError as e:
        print("Failed!\n", e)
        microcontroller.reset()
