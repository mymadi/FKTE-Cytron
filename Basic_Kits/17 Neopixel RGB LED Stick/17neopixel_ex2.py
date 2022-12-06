'''
Example Pi Pico W using Neopixel RGB LED Stick

Buy Here:
https://my.cytron.io/p-neopixel-rgb-led-stick-by-cytron

Additional Library:
    - neopixel.mpy
'''

import time
import board
import neopixel
import random

# Configure the setup
PIXEL_PIN = board.GP7  # pin that the NeoPixel is connected to
ORDER = neopixel.GRB  # pixel color channel order
COLORB = (0, 0, 255)  # color to blink (Red, Green, Blue)
COLORR = (255, 0, 0)  # color to blink (Red, Green, Blue)
COLORG = (0, 255, 0)  # color to blink (Red, Green, Blue)
CLEAR = (0, 0, 0)  # clear (or second color)
DELAY = 0.05  # blink rate in seconds
num_pixel = 8

# Create the NeoPixel object
pixel = neopixel.NeoPixel(PIXEL_PIN, num_pixel, brightness=0.5, pixel_order=ORDER)

while True:
    # Blue Color
    for i in range (num_pixel):
        pixel[i] = COLORB
        time.sleep(DELAY)
        pixel[i] = CLEAR
        time.sleep(DELAY)
    # Red Color
    for j in reversed(range(num_pixel)):
        pixel[j] = COLORR
        time.sleep(DELAY)
        pixel[j] = CLEAR
        time.sleep(DELAY)
   # Green Color
    for k in range (num_pixel):
        pixel[k] = COLORG
        time.sleep(DELAY)
        pixel[k] = CLEAR
        time.sleep(DELAY)
        
    time.sleep(1)
    # Random Pixel with Random Color
    for i in range (8):
        COLORRn = (random.randint(0, 255), random.randint(0, 255), random.randint(0, 255))
        k = random.randint(0, 7)
        pixel[k] = COLORRn
        time.sleep(DELAY*2)
        pixel[k] = CLEAR
        time.sleep(DELAY*2)
      
    time.sleep(1)
    # Random Color
    for i in range (num_pixel):
        COLORRn2 = (random.randint(0, 255), random.randint(0, 255), random.randint(0, 255))
        pixel[i] = COLORRn2
        time.sleep(DELAY)
        #pixel[i] = CLEAR
        time.sleep(DELAY)
    
    time.sleep(1)
    # Clear the Pixels
    pixel.fill((0, 0, 0))
    
    # Random Color for ALL Pixels
    for i in range (100):
        pixel.fill((random.randint(0, 255), random.randint(0, 255), random.randint(0, 255)))
        pixel.show()
        time.sleep(DELAY)
    
    time.sleep(1)
    # Clear the Pixels
    pixel.fill((0, 0, 0))
