"""
HTTP Server using CircuitPython on Raspberry Pi Pico W
    - Smart Home Monitoring System
    
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

# Default settings
DHT_PIN_NAME = "GP4"
LED_PIN_NAME = "GP0"  # Built-in LED on Pico W
VIBRATION_PIN_NAME = "GP2"  # Vibration sensor pin
SERVER_PORT = 80
AUTO_REFRESH_SECONDS = 10  # Auto-refresh interval

# Temperature and Humidity ranges
MIN_TEMP = -40  # Minimum temperature for gauge
MAX_TEMP = 80   # Maximum temperature for gauge
MIN_HUM = 0     # Minimum humidity for gauge
MAX_HUM = 100   # Maximum humidity for gauge

# Temperature ranges and colors
TEMP_RANGES = [
    (-40, 0, "#0077BE"),    # Very Cold: Deep Blue
    (0, 15, "#4682B4"),     # Cold: Steel Blue
    (15, 25, "#2E8B57"),    # Moderate: Sea Green
    (25, 35, "#FFC107"),    # Warm: Amber
    (35, 50, "#FF8C00"),    # Hot: Dark Orange
    (50, 80, "#D32F2F")     # Very Hot: Red
]

# Humidity ranges and colors
HUM_RANGES = [
    (0, 20, "#D32F2F"),     # Very Dry: Red
    (20, 40, "#FF8C00"),    # Dry: Dark Orange
    (40, 60, "#FFC107"),    # Moderate: Amber
    (60, 80, "#2E8B57"),    # Humid: Sea Green
    (80, 100, "#0077BE")    # Very Humid: Deep Blue
]

# WiFi credentials
WIFI_SSID = os.getenv("WIFI_SSID")
WIFI_PASSWORD = os.getenv("WIFI_PASSWORD")

# WiFi setup
print(f"Connecting to WiFi: {WIFI_SSID}")
try:
    wifi.radio.connect(WIFI_SSID, WIFI_PASSWORD)
    print(f"Connected to WiFi! IP: {wifi.radio.ipv4_address}")
except Exception as e:
    print(f"WiFi connection error: {e}")
    time.sleep(5)
    raise

# DHT22 setup
dht_pin = getattr(board, DHT_PIN_NAME)
dht_device = adafruit_dht.DHT22(dht_pin)

# LED setup
led_pin = getattr(board, LED_PIN_NAME)
led = digitalio.DigitalInOut(led_pin)
led.direction = digitalio.Direction.OUTPUT
led_state = False  # Initial state: OFF

# Vibration sensor setup
vibration_pin = getattr(board, VIBRATION_PIN_NAME)
vibration_sensor = digitalio.DigitalInOut(vibration_pin)
vibration_sensor.direction = digitalio.Direction.INPUT

# Variables to track vibration
last_vibration_time = 0
vibration_detected = False
VIBRATION_TIMEOUT = 5  # Seconds to show "Vibration Detected" after event

# HTTP server setup
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

    # If vibration is detected, update the timestamp
    if current_vibration:
        last_vibration_time = time.monotonic()
        vibration_detected = True
        print("Vibration detected!")

    # Check if we're still within the display timeout period
    elif vibration_detected and (time.monotonic() - last_vibration_time > VIBRATION_TIMEOUT):
        vibration_detected = False

    return vibration_detected

def get_color_from_range(value, ranges):
    for low, high, color in ranges:
        if low <= value <= high:
            return color
    return "#333"  # Default color

def build_html(temp, hum, led_on, vibration):
    led_status = "ON" if led_on else "OFF"
    led_button_text = "Turn OFF" if led_on else "Turn ON"
    vibration_status = "DETECTED" if vibration else "None"
    vibration_class = "alert" if vibration else "normal"

    # Calculate temperature gauge
    if temp is not None:
        temp_percent = max(0, min(100, (temp - MIN_TEMP) / (MAX_TEMP - MIN_TEMP) * 100))
        temp_color = get_color_from_range(temp, TEMP_RANGES)
    else:
        temp_percent = 0
        temp_color = "#333"

    # Calculate humidity gauge
    if hum is not None:
        hum_percent = max(0, min(100, (hum - MIN_HUM) / (MAX_HUM - MIN_HUM) * 100))
        hum_color = get_color_from_range(hum, HUM_RANGES)
    else:
        hum_percent = 0
        hum_color = "#333"

    html = f"""<!DOCTYPE html>
<html>
<head>
    <title>Smart Home Monitoring System</title>
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

        /* Gauge styles */
        .gauge-label {{
            font-weight: bold;
            margin-bottom: 5px;
        }}
        .bar-gauge-container {{
            width: 100%;
            max-width: 300px;
            height: 20px;
            background-color: #eee;
            border-radius: 5px;
            margin: 5px auto 20px auto;
            overflow: hidden;
            position: relative;
            display: inline-block; /* Center the gauge */
        }}
        .bar-gauge-fill {{
            height: 100%;
            transition: width 0.3s ease;
            position: absolute;
            left: 0;
            top: 0;
        }}
        .bar-gauge-text {{
            position: absolute;
            top: 50%;
            left: 5px;
            transform: translateY(-50%);
            color: #333;
            font-size: 0.8em;
            z-index: 1;
        }}
        .temp-fill {{ background-color: {temp_color}; width: {temp_percent}%; }}
        .hum-fill {{ background-color: {hum_color}; width: {hum_percent}%; }}

        /* Range indicators */
        .range-indicators {{
            display: flex;
            justify-content: space-between;
            max-width: 300px;
            margin: 0 auto 10px auto;
            font-size: 0.7em;
            color: #666;
        }}
    </style>
</head>
<body>
    <div class="container">
        <h1>Smart Home Monitoring System</h1>

        <div class="gauge-label">Temperature</div>
        <div class="range-indicators">
            <span>{MIN_TEMP}°C</span>
            <span>{MAX_TEMP}°C</span>
        </div>
        <div class="bar-gauge-container">
            <div class="bar-gauge-fill temp-fill"></div>
            <div class="bar-gauge-text">{temp if temp is not None else 'Error'} &deg;C</div>
        </div>

        <div class="gauge-label">Humidity</div>
        <div class="range-indicators">
            <span>{MIN_HUM}%</span>
            <span>{MAX_HUM}%</span>
        </div>
        <div class="bar-gauge-container">
            <div class="bar-gauge-fill hum-fill"></div>
            <div class="bar-gauge-text">{hum if hum is not None else 'Error'} %</div>
        </div>

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

        # Set a timeout to prevent indefinite blocking
        client.settimeout(10.0)

        # Use recv_into instead of recv
        request = bytearray(1024)
        request_length = client.recv_into(request, 1024)
        request_text = request[:request_length].decode('utf-8')
        print("Request:", request_text)

        # Parse the first line of the HTTP request
        first_line = request_text.split('\r\n')[0]
        path = first_line.split(' ')[1] if len(first_line.split(' ')) > 1 else "/"
        led_toggled = False

        if "led=toggle" in path:
            led_state = not led_state
            led.value = led_state
            led_toggled = True
            print(f"LED toggled to: {'ON' if led_state else 'OFF'}")

        # Check vibration sensor
        vibration_status = check_vibration()

        if led_toggled:
            # Redirect to home page after toggling
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
