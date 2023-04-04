'''
Maker Line Following Robot

Reference:
    - https://my.cytron.io/p-maker-line-simplifying-line-sensor-for-beginner
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

# Sensors
S5 = digitalio.DigitalInOut(board.GP18)
S5.direction = digitalio.Direction.INPUT
S4 = digitalio.DigitalInOut(board.GP19)
S4.direction = digitalio.Direction.INPUT
S3 = digitalio.DigitalInOut(board.GP20)
S3.direction = digitalio.Direction.INPUT
S2 = digitalio.DigitalInOut(board.GP21)
S2.direction = digitalio.Direction.INPUT
S1 = digitalio.DigitalInOut(board.GP22)
S1.direction = digitalio.Direction.INPUT

def Robot_Movement(sL, sR):
    motorL.throttle = sL
    motorR.throttle = sR

while True:
    rs5 = S5.value
    rs4 = S4.value
    rs3 = S3.value
    rs2 = S2.value
    rs1 = S1.value

    if (rs1==0 and rs2==1 and rs3==1 and rs4==1 and rs5 == 0):
        Robot_Movement(0.5, 0.5)
    elif (rs1==0 and rs2==0 and rs3==1 and rs4==1 and rs5 == 0):
        Robot_Movement(0.5, 0.3)
    elif (rs1==0 and rs2==1 and rs3==1 and rs4==0 and rs5 == 0):
        Robot_Movement(0.3, 0.5)
    elif (rs1==0 and rs2==0 and rs3==0 and rs4==1 and rs5 == 1):
        Robot_Movement(0.6, 0.2)
    elif (rs1==1 and rs2==1 and rs3==0 and rs4==0 and rs5 == 0):
        Robot_Movement(0.2, 0.6)
    elif (rs1==0 and rs2==0 and rs3==0 and rs4==0 and rs5 == 1):
        Robot_Movement(0.6, 0)
    elif (rs1==1 and rs2==0 and rs3==0 and rs4==0 and rs5 == 0):
        Robot_Movement(0, 0.6)
    else:
         continue
