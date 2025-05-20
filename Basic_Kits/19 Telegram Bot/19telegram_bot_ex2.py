"""
Telegram Bot using CircuitPython on Raspberry Pi Pico W
    - Monitors PIR Sensor and sends motion detection notifications
    - Responds to /temp command with internal temperature

Additional libraries
  https://circuitpython.org/libraries
  - adafruit_requests.mpy
"""

import os
import wifi
import socketpool
import time
import microcontroller
import board
import digitalio
import adafruit_requests
import ssl

# Configuration
WIFI_SSID = os.getenv("WIFI_SSID")
WIFI_PASSWORD = os.getenv("WIFI_PASSWORD")
TELEGRAM_TOKEN = os.getenv("botToken")
PIR_PIN = board.GP21  # PIR sensor pin
LED_PIN = board.GP0   # LED pin

API_URL = f"https://api.telegram.org/bot{TELEGRAM_TOKEN}"

# Hardware setup
led = digitalio.DigitalInOut(LED_PIN)
led.direction = digitalio.Direction.OUTPUT
pir = digitalio.DigitalInOut(PIR_PIN)
pir.direction = digitalio.Direction.INPUT

# State
chat_id = None
last_motion_state = pir.value
last_message_time = 0
COOLDOWN = 5  # Seconds between motion messages
update_offset = None  # For Telegram update tracking

def connect_wifi():
    print("Connecting to WiFi...")
    wifi.radio.connect(WIFI_SSID, WIFI_PASSWORD)
    print(f"Connected! IP: {wifi.radio.ipv4_address}")

def send_message(chat_id, text):
    try:
        requests.get(f"{API_URL}/sendMessage?chat_id={chat_id}&text={text}")
        print(f"Message sent: {text}")
    except Exception as e:
        print(f"Failed to send message: {e}")

def blink_led():
    led.value = True
    time.sleep(0.5)
    led.value = False

def read_temp():
    temp_c = microcontroller.cpu.temperature
    return f"Temperature: {temp_c:.1f}C"

def get_telegram_updates(offset=None):
    try:
        url = f"{API_URL}/getUpdates?timeout=5"
        if offset:
            url += f"&offset={offset}"
        response = requests.get(url)
        data = response.json()
        return data["result"]
    except Exception as e:
        print(f"Error getting updates: {e}")
        return []

# --- Main Code ---
connect_wifi()
pool = socketpool.SocketPool(wifi.radio)
requests = adafruit_requests.Session(pool, ssl.create_default_context())

print("Waiting for /start command...")
while chat_id is None:
    updates = get_telegram_updates(update_offset)
    for update in updates:
        if "message" in update and "text" in update["message"]:
            text = update["message"]["text"]
            if text == "/start":
                chat_id = update["message"]["chat"]["id"]
                send_message(chat_id, "Motion detection started. Use /temp to read temperature.")
            update_offset = update["update_id"] + 1
    time.sleep(2)

print("Bot ready! Monitoring motion and temperature...")

while True:
    # 1. Check for new Telegram messages
    updates = get_telegram_updates(update_offset)
    for update in updates:
        if "message" in update and "text" in update["message"]:
            text = update["message"]["text"]
            if text == "/temp":
                send_message(chat_id, read_temp())
            update_offset = update["update_id"] + 1

    # 2. Check PIR sensor for motion (with cooldown)
    motion_detected = (pir.value == True)  # Adjust if your sensor is active high
    current_time = time.monotonic()
    if motion_detected and not last_motion_state:
        if current_time - last_message_time > COOLDOWN:
            blink_led()
            send_message(chat_id, "Motion detected!")
            last_message_time = current_time
    last_motion_state = motion_detected

    time.sleep(1)
