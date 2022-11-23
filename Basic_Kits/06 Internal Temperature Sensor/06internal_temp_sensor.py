'''
The Raspberry Pi Pico W's CPU has a
temperature sensor built into it.
CircuitPython makes it super simple to read
this data from the sensor using the microcontroller module
'''

import time
import microcontroller

while True:
    data = microcontroller.cpu.temperature
    data = "{:.2f}".format(data)
    print("Temperature: ", data, "celcius")
    time.sleep(2)
