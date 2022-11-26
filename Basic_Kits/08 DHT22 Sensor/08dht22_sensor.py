'''
DHT22 Sensor: Temperature and Humidity
Additional Library:
 - adafruit_dht.mpy
 '''

import time
import board
import adafruit_dht

dht22 = adafruit_dht.DHT22(board.GP7)

while True:
    try:
        temperature = dht22.temperature
        humidity = dht22.humidity
        
        print("Temperature: {:.2f} °C, Humidity: {:.2f} %RH ".format(temperature, humidity))

    except RuntimeError as error:
        print(error.args[0])
        time.sleep(2.0)
        continue
    except Exception as error:
        dht22.exit()
        raise error

    time.sleep(2.0)
