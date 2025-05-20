"""
HTTP Server using CircuitPython on Raspberry Pi Pico W
    - Read DHT22 Sensor
    - Control LED
    - Monitor Vibration Sensor
    - Auto-refresh every 10 seconds

Additional libraries
  https://circuitpython.org/libraries
  - adafruit_dht.mpy
"""

import board
import digitalio
import adafruit_dht
import wifi
import socketpool
import time
import os

# Settings
WIFI_SSID = os.getenv("WIFI_SSID")
WIFI_PASSWORD = os.getenv("WIFI_PASSWORD")
DHT_PIN_NAME = "GP4"
LED_PIN_NAME = "GP0"
VIBRATION_PIN_NAME = "GP2"
SERVER_PORT = 80
AUTO_REFRESH_SECONDS = 10

# WiFi setup
wifi.radio.connect(WIFI_SSID, WIFI_PASSWORD)
print(f"Connected to WiFi! IP: {wifi.radio.ipv4_address}")

# Sensor setup
dht_pin = getattr(board, DHT_PIN_NAME)
dht_device = adafruit_dht.DHT22(dht_pin)
led_pin = getattr(board, LED_PIN_NAME)
led = digitalio.DigitalInOut(led_pin)
led.direction = digitalio.Direction.OUTPUT
led_state = False
vibration_pin = getattr(board, VIBRATION_PIN_NAME)
vibration_sensor = digitalio.DigitalInOut(vibration_pin)
vibration_sensor.direction = digitalio.Direction.INPUT

last_vibration_time = 0
vibration_detected = False
VIBRATION_TIMEOUT = 5

pool = socketpool.SocketPool(wifi.radio)
server = pool.socket(pool.AF_INET, pool.SOCK_STREAM)
server.bind(('0.0.0.0', SERVER_PORT))
server.listen(1)
print(f"Listening on http://{wifi.radio.ipv4_address}:{SERVER_PORT}")

def get_sensor_data():
    try:
        temperature = dht_device.temperature
        humidity = dht_device.humidity
        return temperature, humidity
    except Exception as e:
        print("Sensor error:", e)
        return None, None

def check_vibration():
    global last_vibration_time, vibration_detected
    current_vibration = vibration_sensor.value
    if current_vibration:
        last_vibration_time = time.monotonic()
        vibration_detected = True
        print("Vibration detected!")
    elif vibration_detected and (time.monotonic() - last_vibration_time > VIBRATION_TIMEOUT):
        vibration_detected = False
    return vibration_detected

def build_html(temp, hum, led_on, vibration):
    led_status = "ON" if led_on else "OFF"
    led_button_text = "Turn OFF" if led_on else "Turn ON"
    vibration_status = "DETECTED" if vibration else "None"
    vibration_class = "alert" if vibration else "normal"

    html = f"""<!DOCTYPE html>
<html>
<head>
    <title>Pico W Sensor Monitor</title>
    <meta name="viewport" content="width=device-width, initial-scale=1">
    <meta charset="UTF-8">
    <meta http-equiv="refresh" content="{AUTO_REFRESH_SECONDS}">
    <style>
        body {{ font-family: Arial, sans-serif; margin: 20px; text-align: center; }}
        .container {{ max-width: 600px; margin: 0 auto; }}
        .reading {{ font-size: 1.2em; margin: 10px 0; }}
        button {{ padding: 10px 15px; background-color: #4CAF50; color: white;
                border: none; border-radius: 4px; cursor: pointer; margin-right: 10px; }}
        button:hover {{ background-color: #45a049; }}
        .led-on {{ background-color: #4CAF50; }}
        .led-off {{ background-color: #f44336; }}
        .alert {{ color: #f44336; font-weight: bold; }}
        .normal {{ color: #333; }}
        .refresh-info {{ font-size: 0.8em; color: #666; margin-top: 20px; }}
    </style>
</head>
<body>
    <div class="container">
        <h1>Pico W Sensor Monitor</h1>
        <div class="reading">Temperature: <strong>{temp if temp is not None else 'Error'} &deg;C</strong></div>
        <div class="reading">Humidity: <strong>{hum if hum is not None else 'Error'} %</strong></div>
        <div class="reading">LED Status: <strong>{led_status}</strong></div>
        <div class="reading">Vibration: <strong class="{vibration_class}">{vibration_status}</strong></div>
        <form method="GET" action="/">
            <button type="submit" name="led" value="toggle" class="led-{'on' if led_on else 'off'}">{led_button_text}</button>
            <button type="submit">Refresh Now</button>
        </form>
        <div class="refresh-info">Page auto-refreshes every {AUTO_REFRESH_SECONDS} seconds</div>
    </div>
</body>
</html>"""
    return html

while True:
    client = None
    try:
        client, addr = server.accept()
        print("Client connected from", addr)
        client.settimeout(10.0)
        request = bytearray(1024)
        request_length = client.recv_into(request, 1024)
        request_text = request[:request_length].decode('utf-8')
        print("Request:", request_text)
        first_line = request_text.split('\r\n')[0]
        path = first_line.split(' ')[1] if len(first_line.split(' ')) > 1 else "/"
        led_toggled = False
        if "led=toggle" in path:
            led_state = not led_state
            led.value = led_state
            led_toggled = True
            print(f"LED toggled to: {'ON' if led_state else 'OFF'}")
        vibration_status = check_vibration()
        if led_toggled:
            response = ("HTTP/1.1 303 See Other\r\n"
                        "Location: /\r\n"
                        "Connection: close\r\n"
                        "\r\n")
        else:
            temp, hum = get_sensor_data()
            html = build_html(temp, hum, led_state, vibration_status)
            response = ("HTTP/1.1 200 OK\r\n"
                        "Content-Type: text/html; charset=utf-8\r\n"
                        "Connection: close\r\n"
                        "\r\n" + html)
        client.send(response.encode('utf-8'))
    except Exception as e:
        print("Error:", e)
        time.sleep(1)
    finally:
        if client:
            client.close()
