"""
Stepper Motor Movement using L298N Motor Driver

Libraries required from bundle (https://circuitpython.org/libraries):
    - adafruit_motor

References:
    - https://my.cytron.io/tutorial/controlling-stepper-motor-using-maker-drive-raspberry-pi

Where to buy?:
    - https://my.cytron.io/p-stepper-motor
    - https://my.cytron.io/p-2amp-7v-30v-l298n-motor-driver-stepper-driver-2-channels
"""

import time
import board
import digitalio
from adafruit_motor import stepper

DELAY = 0.01
STEPS = 48

# You can use any available GPIO pin on a microcontroller.
# The following pins are simply a suggestion. If you use different pins, update
# the following code to use your chosen pins.

# To use with CircuitPython and a microcontroller:
coils = (
    digitalio.DigitalInOut(board.GP14),  # A1
    digitalio.DigitalInOut(board.GP15),  # A2
    digitalio.DigitalInOut(board.GP16),  # B1
    digitalio.DigitalInOut(board.GP17),  # B2
)

for coil in coils:
    coil.direction = digitalio.Direction.OUTPUT

motor = stepper.StepperMotor(coils[0], coils[1], coils[2], coils[3], microsteps=None)

for step in range(STEPS):
    motor.onestep()
    time.sleep(DELAY)

for step in range(STEPS):
    motor.onestep(direction=stepper.BACKWARD)
    time.sleep(DELAY)

for step in range(STEPS):
    motor.onestep(style=stepper.DOUBLE)
    time.sleep(DELAY)

for step in range(STEPS):
    motor.onestep(direction=stepper.BACKWARD, style=stepper.DOUBLE)
    time.sleep(DELAY)

for step in range(STEPS):
    motor.onestep(style=stepper.INTERLEAVE)
    time.sleep(DELAY)

for step in range(STEPS):
    motor.onestep(direction=stepper.BACKWARD, style=stepper.INTERLEAVE)
    time.sleep(DELAY)

motor.release()
