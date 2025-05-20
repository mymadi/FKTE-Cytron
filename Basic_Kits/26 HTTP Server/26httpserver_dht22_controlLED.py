"""
HTTP Server using CircuitPython on Raspberry Pi Pico W
    - Read DHT22 Sensor
    - Need to toggle REFRESH button for new data
    - Control LED (Toggle Button)
    
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
SERVER_PORT = 80

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

def build_html(temp, hum, led_on):
    led_status = "ON" if led_on else "OFF"
    led_button_text = "Turn OFF" if led_on else "Turn ON"

    html = f"""<!DOCTYPE html>
<html>
<head>
    <title>Pico W DHT22 Monitor</title>
    <meta name="viewport" content="width=device-width, initial-scale=1">
    <style>
        body {{ font-family: Arial, sans-serif; margin: 20px; }}
        .container {{ max-width: 600px; margin: 0 auto; }}
        .reading {{ font-size: 1.2em; margin: 10px 0; }}
        button {{ padding: 10px 15px; background-color: #4CAF50; color: white;
                 border: none; border-radius: 4px; cursor: pointer; margin-right: 10px; }}
        button:hover {{ background-color: #45a049; }}
        .led-on {{ background-color: #4CAF50; }}
        .led-off {{ background-color: #f44336; }}
    </style>
</head>
<body>
<center>
    <div class="container">
        <h1>Pico W DHT22 Sensor</h1>
        <div class="reading">Temperature: <strong>{temp if temp is not None else 'Error'} &deg;C</strong></div>
        <div class="reading">Humidity: <strong>{hum if hum is not None else 'Error'} %</strong></div>
        <div class="reading">LED Status: <strong>{led_status}</strong></div>
        <form method="GET" style="margin-top: 20px;">
            <button type="submit" name="led" value="toggle" class="led-{'on' if led_on else 'off'}">{led_button_text}</button>
            <button type="submit">Refresh Data</button>
        </form>
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

        temp, hum = get_sensor_data()
        html = build_html(temp, hum, led_state)
        response = "HTTP/1.1 200 OK\r\nContent-Type: text/html\r\n\r\n" + html

        client.send(response.encode('utf-8'))

    except Exception as e:
        print("Error:", e)
        time.sleep(1)
    finally:
        if client:
            client.close()
