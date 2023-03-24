'''
Basic Robot Movement using Maker Drive and CircuitPython on Pi Pico W
Libraries required from bundle (https://circuitpython.org/libraries):
  - adafruit_motor
  
References:
  - https://learn.adafruit.com/circuitpython-essentials/circuitpython-pwm
  - https://my.cytron.io/tutorial/control-dc-motor-using-maker-drive-and-circuitpython-on-rp2040
  
'''

import time
import board
import digitalio
import pwmio
from adafruit_motor import motor

# Right Motor
PWM_M1A = board.GP14
PWM_M1B = board.GP15
# Left Motor
PWM_M2A = board.GP17
PWM_M2B = board.GP16

# DC motor setup
# DC Motors generate electrical noise when running that can reset the microcontroller in extreme
# cases. A capacitor can be used to help prevent this.
pwm_1a = pwmio.PWMOut(PWM_M1A, frequency=10000)
pwm_1b = pwmio.PWMOut(PWM_M1B, frequency=10000)
motorR = motor.DCMotor(pwm_1a, pwm_1b)
pwm_2a = pwmio.PWMOut(PWM_M2A, frequency=10000)
pwm_2b = pwmio.PWMOut(PWM_M2B, frequency=10000)
motorL = motor.DCMotor(pwm_2a, pwm_2b)

def Robot_Stop():
    motorL.throttle = 0
    motorR.throttle = 0

def Robot_Forward(sL, sR):
    motorL.throttle = sL
    motorR.throttle = sR
    
def Robot_Backward(sL, sR):
    motorL.throttle = sL
    motorR.throttle = sR

def Robot_TLeft(sL, sR):
    motorL.throttle = sL
    motorR.throttle = sR

def Robot_TRight(sL, sR):
    motorL.throttle = sL
    motorR.throttle = sR
    
while True:
    Robot_Stop()
    time.sleep(2)
    Robot_Forward(0.5, 0.5)
    time.sleep(3)
    Robot_Backward(-0.5, -0.5)
    time.sleep(3)
    Robot_TLeft(0.1, 0.5)
    time.sleep(3)
    Robot_TRight(0.5, 0.1)
    time.sleep(3)
