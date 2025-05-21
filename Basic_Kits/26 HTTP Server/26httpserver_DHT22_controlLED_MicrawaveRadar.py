"""
HTTP Server using CircuitPython on Raspberry Pi Pico W
    - Read DHT22 Sensor
    - Control LED
    - Monitor Human Motion Sensor (Microwave Radar)
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
MOTION_SENSOR_PIN_NAME = "GP2" 
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

# Human Motion Sensor setup (Microwave Radar)
motion_sensor_pin = getattr(board, MOTION_SENSOR_PIN_NAME)
motion_sensor = digitalio.DigitalInOut(motion_sensor_pin)
motion_sensor.direction = digitalio.Direction.INPUT
motion_detected = False

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

def check_motion():
    global motion_detected
    current_motion = motion_sensor.value
    if current_motion:
        motion_detected = True
        print("Motion detected!")
    else:
        motion_detected = False
    return motion_detected

def build_html(temp, hum, led_on, motion):
    led_status = "ON" if led_on else "OFF"
    led_button_text = "Turn OFF" if led_on else "Turn ON"
    motion_status = "DETECTED" if motion else "None"
    motion_class = "alert" if motion else "normal"

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
        <div class="reading">Motion: <strong class="{motion_class}">{motion_status}</strong></div>
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

        motion_status = check_motion()

        if led_toggled:
            response = ("HTTP/1.1 303 See Other\r\n"
                        "Location: /\r\n"
                        "Connection: close\r\n"
                        "\r\n")
        else:
            temp, hum = get_sensor_data()
            html = build_html(temp, hum, led_state, motion_status)
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
