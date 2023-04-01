'''
Simple Light Searching Robot using only ONE Light Dependent Resistor (LDR)
'''
import time
import board
import analogio
import digitalio
import pwmio
from adafruit_motor import motor

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

ldr = analogio.AnalogIn(board.GP27)

def Robot_Movement(sL, sR):
    motorL.throttle = sL
    motorR.throttle = sR

while True:
    raw = ldr.value
    print("raw = {:5d}".format(raw))
    time.sleep(0.1)
    if (raw > 20000):            # << Please changed HERE
        Robot_Movement(0.5, 0.5) # Forward
        print("Move Forward")
    else:
        Robot_Movement(0.1, 0.3) # Turn Left
        print("Turn Left")
