'''
Project: Concurrent Task Management with pyRTOS

Description:
This script demonstrates the power of the pyRTOS library
for cooperative multitasking on the Raspberry Pi Pico W. It sets up
multiple independent tasks that run concurrently:
- 16 individual LEDs blinking at different rates.
- A push button monitoring task (sw17) that toggles an LED (GP16)
  and updates a global boolean variable (swT).
- A random data generation task (RD18) that updates a global float variable (RData).
- The status of swT is printed by LED1 Task (GP0).
- The value of RData is printed by LED2 Task (GP1).

Library Used:
    - pyRTOS: https://github.com/Rybec/pyRTOS

Installation Note:
    Download the pyRTOS library from the link above.
    Copy the entire 'pyRTOS' folder (containing __init__.py, scheduler.py, etc.)
    into the 'lib' directory on your CircuitPython device's CIRCUITPY drive:
    e.g., CIRCUITPY/lib/pyRTOS/

References:
1) RTOS Basics: Getting Started with Microcontrollers: https://www.seeedstudio.com/blog/2021/04/26/rtos-basics-getting-started-with-microcontrollers/
2) Real-time Multitasking on Maker Pi Pico Using pyRTOS: https://my.cytron.io/tutorial/real-time-multitasking-on-maker-pi-pico-using-pyrtos
3) Real-time IoT Room Monitoring on Maker Pi Pico Using pyRTOS: https://my.cytron.io/tutorial/real-time-iot-room-monitoring-on-maker-pi-pico-using-pyrtos
'''

import board
import digitalio
import time
import pyRTOS # Import the pyRTOS library (Rybec/pyRTOS)
import random

# --- Global Variables for Inter-Task Communication ---
# These variables allow tasks to share data, but be mindful of race conditions
# in more complex scenarios (pyRTOS's Message system is generally safer).
swT = False   # Global status for the button (True/False)
RData = 0.0   # Global variable to store random data

# --- Task Definitions ---
# Each task is a generator function that takes 'self' as its first argument.

def led1(self):
    """Controls LED on GP0, blinks and prints swT status."""
    ledpin1 = digitalio.DigitalInOut(board.GP0)
    ledpin1.direction = digitalio.Direction.OUTPUT
    ledpin1.value = False # Ensure LED is off initially
    yield # Initial yield to allow setup to complete before loop

    while True:
        ledpin1.value = not ledpin1.value # Toggle LED state
        print(f"LED1 Task (GP0): swT status = {swT}") # Access global swT
        yield [pyRTOS.timeout(1)] # Yield control for 1 second

def led2(self):
    """Controls LED on GP1, blinks and prints RData value."""
    ledpin2 = digitalio.DigitalInOut(board.GP1)
    ledpin2.direction = digitalio.Direction.OUTPUT
    ledpin2.value = False
    yield

    while True:
        ledpin2.value = not ledpin2.value
        print(f"LED2 Task (GP1): Random Data = {RData:.2f}") # Access global RData
        yield [pyRTOS.timeout(0.95)]

def led3(self):
    """Controls LED on GP2, blinks at 0.90s."""
    ledpin3 = digitalio.DigitalInOut(board.GP2)
    ledpin3.direction = digitalio.Direction.OUTPUT
    ledpin3.value = False
    yield

    while True:
        ledpin3.value = not ledpin3.value
        yield [pyRTOS.timeout(0.90)]

def led4(self):
    """Controls LED on GP3, blinks at 0.85s."""
    ledpin4 = digitalio.DigitalInOut(board.GP3)
    ledpin4.direction = digitalio.Direction.OUTPUT
    ledpin4.value = False
    yield

    while True:
        ledpin4.value = not ledpin4.value
        yield [pyRTOS.timeout(0.85)]

def led5(self):
    """Controls LED on GP4, blinks at 0.80s."""
    ledpin5 = digitalio.DigitalInOut(board.GP4)
    ledpin5.direction = digitalio.Direction.OUTPUT
    ledpin5.value = False
    yield

    while True:
        ledpin5.value = not ledpin5.value
        yield [pyRTOS.timeout(0.80)]

def led6(self):
    """Controls LED on GP5, blinks at 0.75s."""
    ledpin6 = digitalio.DigitalInOut(board.GP5)
    ledpin6.direction = digitalio.Direction.OUTPUT
    ledpin6.value = False
    yield

    while True:
        ledpin6.value = not ledpin6.value
        yield [pyRTOS.timeout(0.75)]

def led7(self):
    """Controls LED on GP6, blinks at 0.70s."""
    ledpin7 = digitalio.DigitalInOut(board.GP6)
    ledpin7.direction = digitalio.Direction.OUTPUT
    ledpin7.value = False
    yield

    while True:
        ledpin7.value = not ledpin7.value
        yield [pyRTOS.timeout(0.70)]

def led8(self):
    """Controls LED on GP7, blinks at 0.65s."""
    ledpin8 = digitalio.DigitalInOut(board.GP7)
    ledpin8.direction = digitalio.Direction.OUTPUT
    ledpin8.value = False
    yield

    while True:
        ledpin8.value = not ledpin8.value
        yield [pyRTOS.timeout(0.65)]

def led9(self):
    """Controls LED on GP8, blinks at 0.60s."""
    ledpin9 = digitalio.DigitalInOut(board.GP8)
    ledpin9.direction = digitalio.Direction.OUTPUT
    ledpin9.value = False
    yield

    while True:
        ledpin9.value = not ledpin9.value
        yield [pyRTOS.timeout(0.60)]

def led10(self):
    """Controls LED on GP9, blinks at 0.55s."""
    ledpin10 = digitalio.DigitalInOut(board.GP9)
    ledpin10.direction = digitalio.Direction.OUTPUT
    ledpin10.value = False
    yield

    while True:
        ledpin10.value = not ledpin10.value
        yield [pyRTOS.timeout(0.55)]

def led11(self):
    """Controls LED on GP10, blinks at 0.50s."""
    ledpin11 = digitalio.DigitalInOut(board.GP10)
    ledpin11.direction = digitalio.Direction.OUTPUT
    ledpin11.value = False
    yield

    while True:
        ledpin11.value = not ledpin11.value
        yield [pyRTOS.timeout(0.50)]

def led12(self):
    """Controls LED on GP11, blinks at 0.45s."""
    ledpin12 = digitalio.DigitalInOut(board.GP11)
    ledpin12.direction = digitalio.Direction.OUTPUT
    ledpin12.value = False
    yield

    while True:
        ledpin12.value = not ledpin12.value
        yield [pyRTOS.timeout(0.45)]

def led13(self):
    """Controls LED on GP12, blinks at 0.40s."""
    ledpin13 = digitalio.DigitalInOut(board.GP12)
    ledpin13.direction = digitalio.Direction.OUTPUT
    ledpin13.value = False
    yield

    while True:
        ledpin13.value = not ledpin13.value
        yield [pyRTOS.timeout(0.40)]

def led14(self):
    """Controls LED on GP13, blinks at 0.35s."""
    ledpin14 = digitalio.DigitalInOut(board.GP13)
    ledpin14.direction = digitalio.Direction.OUTPUT
    ledpin14.value = False
    yield

    while True:
        ledpin14.value = not ledpin14.value
        yield [pyRTOS.timeout(0.35)]

def led15(self):
    """Controls LED on GP14, blinks at 0.30s."""
    ledpin15 = digitalio.DigitalInOut(board.GP14)
    ledpin15.direction = digitalio.Direction.OUTPUT
    ledpin15.value = False
    yield

    while True:
        ledpin15.value = not ledpin15.value
        yield [pyRTOS.timeout(0.30)]

def led16(self):
    """Controls LED on GP15, blinks at 0.25s."""
    ledpin16 = digitalio.DigitalInOut(board.GP15)
    ledpin16.direction = digitalio.Direction.OUTPUT
    ledpin16.value = False
    yield

    while True:
        ledpin16.value = not ledpin16.value
        yield [pyRTOS.timeout(0.25)]

def sw17(self):
    """Monitors push button (GP21) and updates global swT status, controls LED on GP16."""
    global swT # Declare intent to modify the global variable
    swpin17 = digitalio.DigitalInOut(board.GP21)
    swpin17.direction = digitalio.Direction.INPUT
    # Assuming internal pull-up/down is managed by Maker Pi Pico board or external resistor
    # If not, add swpin17.pull = digitalio.Pull.UP or DOWN if needed.

    ledpin17 = digitalio.DigitalInOut(board.GP16)
    ledpin17.direction = digitalio.Direction.OUTPUT
    ledpin17.value = False # LED off initially
    yield

    while True:
        # Check if button is pressed (assuming active low, i.e., False when pressed)
        if swpin17.value == False:
            ledpin17.value = not ledpin17.value # Toggle LED on GP16
            swT = not swT # Toggle global switch status
        yield [pyRTOS.timeout(0.15)] # Check button every 0.15 seconds (debounce)

def RD18(self):
    """Generates random data and updates global RData variable."""
    global RData # Declare intent to modify the global variable
    yield # Initial yield

    while True:
        RData = random.uniform(0, 250) # Generate a random float between 0 and 250
        yield [pyRTOS.timeout(1)] # Update random data every 1 second

# --- RTOS Setup ---
print("Adding tasks to pyRTOS scheduler...")

# Create Task instances and add them to the scheduler
# pyRTOS.Task(task_function, name=None, priority=0, mailbox=False)
pyRTOS.add_task(pyRTOS.Task(led1, name="LED_GP0", priority=1))
pyRTOS.add_task(pyRTOS.Task(led2, name="LED_GP1", priority=2))
pyRTOS.add_task(pyRTOS.Task(led3, name="LED_GP2", priority=3))
pyRTOS.add_task(pyRTOS.Task(led4, name="LED_GP3", priority=4))
pyRTOS.add_task(pyRTOS.Task(led5, name="LED_GP4", priority=5))
pyRTOS.add_task(pyRTOS.Task(led6, name="LED_GP5", priority=6))
pyRTOS.add_task(pyRTOS.Task(led7, name="LED_GP6", priority=7))
pyRTOS.add_task(pyRTOS.Task(led8, name="LED_GP7", priority=8))
pyRTOS.add_task(pyRTOS.Task(led9, name="LED_GP8", priority=9))
pyRTOS.add_task(pyRTOS.Task(led10, name="LED_GP9", priority=10))
pyRTOS.add_task(pyRTOS.Task(led11, name="LED_GP10", priority=11))
pyRTOS.add_task(pyRTOS.Task(led12, name="LED_GP11", priority=12))
pyRTOS.add_task(pyRTOS.Task(led13, name="LED_GP12", priority=13))
pyRTOS.add_task(pyRTOS.Task(led14, name="LED_GP13", priority=14))
pyRTOS.add_task(pyRTOS.Task(led15, name="LED_GP14", priority=15))
pyRTOS.add_task(pyRTOS.Task(led16, name="LED_GP15", priority=16))
pyRTOS.add_task(pyRTOS.Task(sw17, name="Button_GP21", priority=17)) # Button task
pyRTOS.add_task(pyRTOS.Task(RD18, name="Random_Data", priority=18)) # Random data task

print("Starting pyRTOS scheduler...")
# Start the RTOS scheduler. For Rybec/pyRTOS, no arguments are passed here.
pyRTOS.start()

# This line will generally not be reached, as the RTOS scheduler runs indefinitely.
print("Scheduler stopped. (This message implies all tasks have terminated, which is unlikely for this code)")
