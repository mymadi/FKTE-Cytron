"""
Favoriot using CircuitPython on Raspberry Pi Pico W (Publish)
    - https://www.favoriot.com/
    - Free version limit to 2 widgets and 500 samples per day.

Additional libraries
  https://circuitpython.org/libraries
  - adafruit_minimqtt
  - adafruit_dht.mpy
"""

import time
import os
import board
import analogio
import adafruit_dht
import wifi
import socketpool
import adafruit_minimqtt.adafruit_minimqtt as MQTT
import json
import microcontroller


# WiFi credentials
WIFI_SSID = os.getenv("WIFI_SSID")
WIFI_PASSWORD = os.getenv("WIFI_PASSWORD")
MQTT_DEVICE_DEVELOPER_ID = os.getenv("MQTT_DEVICE_DEVELOPER_ID")
MQTT_DEVICE_ACCESS_TOKEN = os.getenv("MQTT_DEVICE_ACCESS_TOKEN")  # device access token
MQTT_CLIENTID = os.getenv("MQTT_CLIENTID")
MQTT_HOST = "mqtt.favoriot.com"
MQTT_PORT = 1883  # Typically 1883 for non-SSL, 8883 for SSL
MQTT_PUBLISH_TOPIC = "/v2/streams"
MQTT_STATUS_TOPIC = "/v2/streams/status"


pool = socketpool.SocketPool(wifi.radio)# Initialize socket pool
# Initialize MQTT client with a keep-alive interval of 60 seconds and loop timeout of 10 seconds
mqtt_client = MQTT.MQTT(
    broker=MQTT_HOST,
    port=MQTT_PORT,
    username=MQTT_DEVICE_ACCESS_TOKEN,
    password=MQTT_DEVICE_ACCESS_TOKEN,
    socket_pool=pool,
    keep_alive=60
)

"""DHT"""
dht = adafruit_dht.DHT22(board.GP4) # Temperature,Humidity sensors
# Global variable for publish interval
publish_interval = 5 

# Function to connect to WiFi
def connect_to_wifi():
    wifi.radio.connect(WIFI_SSID, WIFI_PASSWORD)
    print("Connected to WiFi!")
    print("IP address:", wifi.radio.ipv4_address)

# Define callback methods for MQTT events
def got_connected(client, userdata, flags, rc):
    print("Connected to MQTT broker!")
    print("Subscribing to topic...")
    client.subscribe(f"{MQTT_DEVICE_ACCESS_TOKEN}{MQTT_STATUS_TOPIC}")
    print(f"Subscribed to {MQTT_DEVICE_ACCESS_TOKEN}{MQTT_STATUS_TOPIC}")

def got_disconnected(client, userdata, rc):
    print("Disconnected from MQTT broker!")
    try_reconnect()

# Function to reconnect to WiFi and MQTT broker
def try_reconnect():
    try:
        if not wifi.radio.ipv4_address:
            connect_to_wifi()
        if not mqtt_client.is_connected():
            print("Reconnecting to MQTT broker...")
            mqtt_client.reconnect()
            print("Reconnected to MQTT broker")
    except Exception as e:
        print("Error during reconnection:", e)

def done_publish(client, userdata, topic, pid):
    print(f"Published to {topic} with PID {pid}")

def getData(client, topic, msg):
    print("======================================")
    print(f"New message on topic {topic}: {msg}")
    print("======================================")

def sendStreams():
    # Create JSON payload for Favoriot
    data = {
         "device_developer_id": MQTT_DEVICE_DEVELOPER_ID,  # Replace 'YOUR_DEVICE_ID' with your actual device ID
         "data":{
                "temperature": temperature,
                "humidity": humidity,                
                }
           }
            # Publish data to Favoriot MQTT broker with QoS 2
    mqtt_client.publish((f"{MQTT_DEVICE_ACCESS_TOKEN}{MQTT_PUBLISH_TOPIC}"), json.dumps(data))

# Connect to WiFi
print("Connecting to WiFi...")
connect_to_wifi()

# Set up MQTT event handlers
mqtt_client.on_connect = got_connected
mqtt_client.on_disconnect = got_disconnected
mqtt_client.on_publish = done_publish
mqtt_client.on_message = getData

# Connect to the MQTT broker
print("Connecting to MQTT broker...")
mqtt_client.connect()

# Variable to track the last publish time
last_publish_time = time.monotonic()

while True:
    try:
        current_time = time.monotonic()
        if current_time - last_publish_time >= publish_interval:
            temperature = dht.temperature
            humidity = dht.humidity
            
            sendStreams()
            last_publish_time = current_time
    except RuntimeError as error:
        # Errors happen fairly often with DHT sensors, just keep going
        print(error.args[0])
    except Exception as e:
        print("Error:", e)

    # Check connection status and reconnect if necessary
    try_reconnect()
    # Process any incoming messages
    mqtt_client.loop(1)
