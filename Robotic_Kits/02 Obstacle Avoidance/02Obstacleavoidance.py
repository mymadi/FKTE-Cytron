'''
Obstcle Avoidance Robot using 3V-5.5V SR04P Ultrasonic Ranging Module.

Additional Library:
    - adafruit_hcsr04.mpy
    - adafruit_motor
'''

import time
import board
import digitalio
import pwmio
from adafruit_motor import motor
import adafruit_hcsr04

sonar = adafruit_hcsr04.HCSR04(trigger_pin=board.GP13, echo_pin=board.GP12)

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
    
def Read_Ultrasonic():
    time.sleep(0.1)
    return sonar.distance

while True:
    Distance = Read_Ultrasonic()
    print(Distance)
    if (Distance < 10):
        Robot_TLeft(0.1, 0.5)
        print("Turn Left")
        time.sleep(3)
    else:
        Robot_Forward(0.5, 0.5)