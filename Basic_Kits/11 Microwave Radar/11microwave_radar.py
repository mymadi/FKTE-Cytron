"""
Example for Pi Pico W. Blink An External LED (GP0) if:
Microwave Radar Sensor detected Human Body Motion

Reference:
[1] https://my.cytron.io/p-microwave-radar-human-motion-sensor
[2] https://create.arduino.cc/projecthub/remnis/coolest-motion-detection-sensor-ever-d2d688
[3] https://github.com/jdesbonnet/RCWL-0516
"""

import time
import board
import digitalio

led = digitalio.DigitalInOut(board.GP0)
led.direction = digitalio.Direction.OUTPUT

rcwl = digitalio.DigitalInOut(board.GP2)
rcwl.direction = digitalio.Direction.INPUT

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
    if rcwl.value== True:
        blinkled()
    else:
        ledoff()
    
    time.sleep(1)
