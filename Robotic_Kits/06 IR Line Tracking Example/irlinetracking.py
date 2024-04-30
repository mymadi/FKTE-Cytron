"""
Example for Pi Pico W. For IR Line Tracking Module
IR Line Tracking Module at pin GP20 (Active LOW)

Link:
https://my.cytron.io/c-photoelectric-line-sensor/p-ir-line-tracking-module

Note:
1) Will output logic LOW when object is detection
2) Obstacle detection range: 5mm to 10mm from the sensor
3) Adjustable sensitivity with an onboard potentiometer, this translates to an adjustable detection range
"""

import time
import board
import digitalio

IRs = digitalio.DigitalInOut(board.GP20)
IRs.direction = digitalio.Direction.INPUT

while True:
    if IRs.value== True:
        print("Black Line")
    else:
        print("White Line")
    time.sleep(1)
