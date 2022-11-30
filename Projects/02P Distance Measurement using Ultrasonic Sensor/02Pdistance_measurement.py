'''
Example Pi Pico W. 3V-5.5V SR04P Ultrasonic Ranging Module.
References:
  [1] https://github.com/Guitarman9119/Raspberry-Pi-Pico-/tree/main/I2C%2016x2%20LCD%20Circuit%20Python

Additional Library:
    - lcd.py from [1]
    - i2c_pcf8574_interface.py from [1]
    - adafruit_hcsr04.mpy   
'''

import time
import board
import adafruit_hcsr04
import busio
import digitalio
# Needs these 2 libraries from Guitarman9119 Github
# Upload it to the 'Lib'
import lcd
import i2c_pcf8574_interface

# Ultrasonic
sonar = adafruit_hcsr04.HCSR04(trigger_pin=board.GP7, echo_pin=board.GP6)
# Serial LCD
i2c = busio.I2C(scl=board.GP5, sda=board.GP4)
address = 0x3F
i2c = i2c_pcf8574_interface.I2CPCF8574Interface(i2c, address)
display = lcd.LCD(i2c, num_rows=2, num_cols=16)
display.set_backlight(True)
display.set_display_enabled(True)

# Display Message
display.clear()
display.print("Ultrasonic Dist\nMeasurement")
time.sleep(2)
    
while True:
    # Read and Check Sensor
    try:
        ultra = sonar.distance
        #print(sonar.distance)
    except RuntimeError:
        print("Retrying!")
        pass
    
    # Display
    display.clear()
    display.set_cursor_pos(0, 0)
    display.print("Dist(cm): {:0.2f}".format(ultra))
    time.sleep(2)
