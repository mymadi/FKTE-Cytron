"""
Example for Pi Pico W. Running & Blink Light
"""
import time
import board
import digitalio

# LEDs Pinout             
L = [0,0,0,0,0,0,0,0]

# To Declare the LEDs as PORT
LEDS = (board.GP0, board.GP1, board.GP2, board.GP3, board.GP4, board.GP5, board.GP6, board.GP7)

for i in range(8):
    L[i] = digitalio.DigitalInOut(LEDS[i])
    L[i].direction = digitalio.Direction.OUTPUT

# Running Light
def running_light():
    for j in range(8):
        L[j].value = True
        time.sleep(0.05)
    
    for j in range(8):
        L[j].value = False
        
    for j in reversed(range(8)):
        L[j].value = True
        time.sleep(0.05)
        
    for j in range(8):
        L[j].value = False

# Blink Light
def blink_light():
    for j in range(8):
        L[j].value = True
    time.sleep(0.5)
    for j in range(8):
        L[j].value = False
    time.sleep(0.5)

# OFF the Light
def off_light():
    for j in range(8):
        L[j].value = False
    
while True:
    for rl in range(3):
        running_light()    # Running Light
    time.sleep(1)
    off_light()            # OFF Light
    
    for bl in range(5):
        blink_light()      # Blink Light
    time.sleep(1)
    off_light()            # OFF Light
    time.sleep(1)
