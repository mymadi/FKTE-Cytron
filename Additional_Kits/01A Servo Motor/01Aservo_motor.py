"""
Servo Motor Movement (0 - 180 degrees)

Libraries required from bundle (https://circuitpython.org/libraries):
    - adafruit_motor

References:
    - https://learn.adafruit.com/circuitpython-essentials/circuitpython-servo

Where to buy?:
    - https://my.cytron.io/p-analog-micro-servo-9g-3v-6v (Operating Angle: 180 degrees)
    - https://my.cytron.io/p-micro-360-degree-continuous-rotation-servo (Operating Angle: 360 degrees)
"""
import time
import board
import pwmio
from adafruit_motor import servo

# create a PWMOut object on Pin A2.
pwm = pwmio.PWMOut(board.GP5, duty_cycle=2 ** 15, frequency=50)

# Create a servo object, my_servo.
my_servo = servo.Servo(pwm, min_pulse = 500, max_pulse = 2500)

while True:
    for angle in range(0, 180, 5):  # 0 - 180 degrees, 5 degrees at a time.
        my_servo.angle = angle
        time.sleep(0.1)
    for angle in range(180, 0, -5): # 180 - 0 degrees, 5 degrees at a time.
        my_servo.angle = angle
        time.sleep(0.1)
