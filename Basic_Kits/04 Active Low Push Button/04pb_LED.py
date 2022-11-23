"""
Example for Pi Pico W. Blink An External LED (GP0)
Push the Button at pin GP20 (Active LOW)
"""

import time
import board
import digitalio

led = digitalio.DigitalInOut(board.GP0)
led.direction = digitalio.Direction.OUTPUT

switch = digitalio.DigitalInOut(board.GP20)
switch.direction = digitalio.Direction.INPUT

def blinkled():
    print("Blink LED GP0")
    led.value = True
    time.sleep(1)
    led.value = False
    time.sleep(1)
    led.value = True
    time.sleep(1)
    led.value = False
    time.sleep(1)

def ledoff():
    led.value = False
    print("Turn OFF LED GP0")

while True:
    if switch.value== True:
        ledoff()
    else:
        blinkled()
    time.sleep(1)
            
