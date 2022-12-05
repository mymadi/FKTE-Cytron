"""
Example for Pi Pico W. PIR Sensor Module

Additional Library:
    -simpleio.mpy
"""

import time
import board
import digitalio
import simpleio

# Define pin connected to piezo buzzer.
BUZZER_PIN = board.GP18

pir = digitalio.DigitalInOut(board.GP7)
pir.direction = digitalio.Direction.INPUT

def simpletone():
    for i in range (5):
        simpleio.tone(BUZZER_PIN, 261, duration=0.1)
        simpleio.tone(BUZZER_PIN, 392, duration=0.15)

def offtone():
    simpleio.tone(BUZZER_PIN, 0)

while True:
    if pir.value == True:
        simpletone()
    else:
        offtone()
        
    time.sleep(1)
