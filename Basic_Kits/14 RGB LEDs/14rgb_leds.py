"""
Example for Pico. Common Anode RGB LEDs
"""
import time
import board
import digitalio

ledR = digitalio.DigitalInOut(board.GP0)
ledG = digitalio.DigitalInOut(board.GP1)
ledB = digitalio.DigitalInOut(board.GP2)
ledR.direction = digitalio.Direction.OUTPUT
ledG.direction = digitalio.Direction.OUTPUT
ledB.direction = digitalio.Direction.OUTPUT

def clearRGB():
    ledR.value = True
    ledG.value = True
    ledB.value = True

def alternateRGB():
    clearRGB()
    ledR.value = False
    time.sleep(1)
    clearRGB()
    ledG.value = False
    time.sleep(1)
    clearRGB()
    ledB.value = False
    time.sleep(1)
    clearRGB()
    
def magenta():
    clearRGB()
    ledR.value = False
    ledB.value = False

def yellow():
    clearRGB()
    ledG.value = False
    ledR.value = False
    
def cyan():
    clearRGB()
    ledG.value = False
    ledB.value = False

def white():
    clearRGB()
    ledR.value = False
    ledG.value = False
    ledB.value = False
    
while True:
    alternateRGB()
    magenta()
    time.sleep(1)
    yellow()
    time.sleep(1)
    cyan()
    time.sleep(1)
    white()
    time.sleep(1)
