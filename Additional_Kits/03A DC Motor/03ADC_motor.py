import board
import pwmio
import digitalio
import time

# --- Configuration ---
# Set up GPIO pins for direction control
in1 = digitalio.DigitalInOut(board.GP14)
in2 = digitalio.DigitalInOut(board.GP15)
in1.direction = digitalio.Direction.OUTPUT
in2.direction = digitalio.Direction.OUTPUT

# Set up PWM pin for speed control (ENA)
# Duty cycle 0-65535
ena = pwmio.PWMOut(board.GP13, frequency=1000, duty_cycle=0)

# --- Functions ---
def forward(speed):
    in1.value = True
    in2.value = False
    ena.duty_cycle = speed  # speed is 0 to 65535

def backward(speed):
    in1.value = False
    in2.value = True
    ena.duty_cycle = speed

def stop():
    in1.value = False
    in2.value = False
    ena.duty_cycle = 0

# --- Main Loop ---
while True:
    print("Forward")
    forward(40000) # Approx 60% speed
    time.sleep(2)
    
    print("Stop")
    stop()
    time.sleep(1)
    
    print("Backward")
    backward(30000) # Approx 45% speed
    time.sleep(2)
    
    print("Stop")
    stop()
    time.sleep(1)
