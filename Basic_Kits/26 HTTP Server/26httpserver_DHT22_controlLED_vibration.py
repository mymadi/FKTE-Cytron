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

# Default settings
WIFI_SSID = "YOUR_WIFI_SSID"
WIFI_PASSWORD = "YOUR_WIFI_PASSWORD"
DHT_PIN_NAME = "GP4"
LED_PIN_NAME = "GP0"  # Built-in LED on Pico W
VIBRATION_PIN_NAME = "GP2"  # Vibration sensor pin
SERVER_PORT = 80
AUTO_REFRESH_SECONDS = 10  # Auto-refresh interval

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
# vibration_sensor.pull = digitalio.Pull.UP  # Use pull-up if sensor gives LOW when vibration detected
# For sensors that give HIGH on vibration, use: vibration_sensor.pull = digitalio.Pull.DOWN

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
    <meta http-equiv="refresh" content="{AUTO_REFRESH_SECONDS}">
    <style>
        body {{ font-family: Arial, sans-serif; margin: 20px; }}
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
<center>
    <div class="container">
        <h1>Pico W Sensor Monitor</h1>
        <div class="reading">Temperature: <strong>{temp if temp is not None else 'Error'} &deg;C</strong></div>
        <div class="reading">Humidity: <strong>{hum if hum is not None else 'Error'} %</strong></div>
        <div class="reading">LED Status: <strong>{led_status}</strong></div>
        <div class="reading">Vibration: <strong class="{vibration_class}">{vibration_status}</strong></div>
        <form method="GET" style="margin-top: 20px;">
            <button type="submit" name="led" value="toggle" class="led-{'on' if led_on else 'off'}">{led_button_text}</button>
            <button type="submit">Refresh Now</button>
        </form>
        <div class="refresh-info">Page auto-refreshes every {AUTO_REFRESH_SECONDS} seconds</div>
    </div>
</center>
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

        # Check if LED toggle was requested
        if "GET /?led=toggle" in request_text:
            led_state = not led_state
            led.value = led_state
            print(f"LED toggled to: {'ON' if led_state else 'OFF'}")

        # Check vibration sensor
        vibration_status = check_vibration()

        temp, hum = get_sensor_data()
        html = build_html(temp, hum, led_state, vibration_status)
        response = "HTTP/1.1 200 OK\r\nContent-Type: text/html\r\n\r\n" + html

        client.send(response.encode('utf-8'))

    except Exception as e:
        print("Error:", e)
        time.sleep(1)
    finally:
        if client:
            client.close()
