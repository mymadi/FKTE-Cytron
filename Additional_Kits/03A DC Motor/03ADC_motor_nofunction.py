import time
import board
import digitalio
import pwmio

# 1. Setup Direction Pins
in1 = digitalio.DigitalInOut(board.GP14)
in1.direction = digitalio.Direction.OUTPUT
in2 = digitalio.DigitalInOut(board.GP15)
in2.direction = digitalio.Direction.OUTPUT

# 2. Setup Speed Pin (ENA) - Set to 100% (65535)
ena = pwmio.PWMOut(board.GP2, frequency=1000)
ena.duty_cycle = 65535 

# --- CLOCKWISE ---
print("Spinning Clockwise...")
in1.value = True
in2.value = False
time.sleep(3)

# --- STOP ---
print("Stopping...")
in1.value = False
in2.value = False
time.sleep(1)

# --- COUNTER-CLOCKWISE ---
print("Spinning Counter-Clockwise...")
in1.value = False
in2.value = True
time.sleep(3)

# --- FINAL STOP ---
in1.value = False
in2.value = False
print("Done.")
