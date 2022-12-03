"""
Example for Pico. Common Anode RGB LEDs

Additional Library:
    - adafruit_rgbled.mpy
    
References:
[1] https://www.rapidtables.com/web/color/RGB_Color.html
"""

import board
import time
import adafruit_rgbled

RED_LED = board.GP0
GREEN_LED = board.GP1
BLUE_LED = board.GP2

# Create a RGB LED object
# invert_pwm=True = for Common Anode
# invert_pwm=False = for Common Cathode
led = adafruit_rgbled.RGBLED(RED_LED, GREEN_LED, BLUE_LED, invert_pwm=True)

# Using a 24-bit integer (hex syntax)
# led.color = 0xFF00FF # Red Color
# Using RGB Tuple (Red, Green, Blue)
# led.color = (238, 75, 43)

while True:
    # Using a 24-bit integer (hex syntax)
    led.color = 0xFF0000 # Red Color
    time.sleep(1)
    led.color = 0x00FF00 # Green Color
    time.sleep(1)
    led.color = 0x0000FF # Blue Color
    time.sleep(1)
    # Using RGB Tuple (Red, Green, Blue)
    led.color = (255, 255, 0) # Yellow
    time.sleep(1)
    led.color = (128, 0, 128) # Purple
    time.sleep(1)
    led.color = (135,206,235) # Sky Blue
    time.sleep(1)