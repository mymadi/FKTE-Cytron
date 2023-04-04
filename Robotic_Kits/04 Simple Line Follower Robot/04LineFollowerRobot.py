'''
Simple Line Following Robot (2 Sensors).

Libraries required from bundle (https://circuitpython.org/libraries):
  - adafruit_motor
'''

import time
import board
import digitalio
import pwmio
from adafruit_motor import motor

# Sensors
SenL = digitalio.DigitalInOut(board.GP18)
SenL.direction = digitalio.Direction.INPUT

SenR = digitalio.DigitalInOut(board.GP13)
SenR.direction = digitalio.Direction.INPUT

# Left Motor
PWM_M1A = board.GP16
PWM_M1B = board.GP17
# Right Motor
PWM_M2A = board.GP14
PWM_M2B = board.GP15

# DC motor setup
# DC Motors generate electrical noise when running that can reset the microcontroller in extreme
# cases. A capacitor can be used to help prevent this.
pwm_1a = pwmio.PWMOut(PWM_M1A, frequency=10000)
pwm_1b = pwmio.PWMOut(PWM_M1B, frequency=10000)
motorL = motor.DCMotor(pwm_1a, pwm_1b)
pwm_2a = pwmio.PWMOut(PWM_M2A, frequency=10000)
pwm_2b = pwmio.PWMOut(PWM_M2B, frequency=10000)
motorR = motor.DCMotor(pwm_2a, pwm_2b)

def Robot_Movement(sL, sR):
    motorL.throttle = sL
    motorR.throttle = sR

while True:
    if (SenL.value == 0) and (SenR.value == 1):
        Robot_Movement(0.5, 0.1)
    elif (SenL.value == 1) and (SenR.value == 0):
        Robot_Movement(0.1, 0.5)
    else:
        Robot_Movement(0.5, 0.5)
