'''
Example for Pi Pico W: Buzzer
using simpleio.tone

Additional Library:
    -simpleio.mpy
'''

import board
import time
import simpleio
import math

# Define pin connected to piezo buzzer.
BUZZER_PIN = board.GP18

# Define a list of tones/music notes to play.
TONE_FREQ = [ 262,  # C4
              294,  # D4
              330,  # E4
              349,  # F4
              392,  # G4
              440,  # A4
              494,  # B4
              523 ] # C5

def playtones():
    for i in range(len(TONE_FREQ)):
        simpleio.tone(BUZZER_PIN, TONE_FREQ[i], duration=0.5)
    for i in range(len(TONE_FREQ)-1, -1, -1):
        simpleio.tone(BUZZER_PIN, TONE_FREQ[i], duration=0.5)

def testtones():
    for f in (262, 294, 330, 349, 392, 440, 494, 523):
        simpleio.tone(BUZZER_PIN, f, 0.25)
    time.sleep(1)

def sintones():
    y = 180
    w = 1000
    z = 100
    for x in range(y):
        sinVal = (math.sin(x*(3.1412/y)))
        f = z+(sinVal*w)
        print(f)
        simpleio.tone(BUZZER_PIN, f,0.015)
        
def simpletone():
    simpleio.tone(BUZZER_PIN, 261, duration=0.1)
    simpleio.tone(BUZZER_PIN, 392, duration=0.15)

while True:
    sintones()
    time.sleep(1)
    testtones()
    time.sleep(1)
    playtones()
    time.sleep(1)
    simpletone()
    time.sleep(1)
