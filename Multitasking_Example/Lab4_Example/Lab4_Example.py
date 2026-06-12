'''
======================================================================
Laboratory 4: Monitoring System based on Real-Time Operating 
              System (RTOS) & Object-Oriented Programming
======================================================================
Board:   Raspberry Pi Pico W
Date:    June 12, 2026

Description:
This script demonstrates cooperative multitasking using the pyRTOS 
library alongside inter-task communication via global variables. 
It features three concurrent tasks:
1) Monitoring a vibration sensor (via a custom OOP module on GP22), 
   toggling an LED (GP0), and updating a global status variable.
2) Polling the internal microcontroller CPU temperature and printing
   a combined status dashboard (Temp, Vibration, Button) every 2 seconds.
3) Monitoring a push button (GP21), toggling an LED (GP1), and 
   updating a global status variable.

Libraries:
- pyRTOS (Rybec/pyRTOS)
- Custom OOP Module (vib.py)
======================================================================
'''

import board
import digitalio
import pyRTOS
import microcontroller
from vib import VibrationSensor

# ==========================================
# --- Global Variables for Inter-Task Comm ---
# ==========================================
vib_status = False  # Stores the current state of the vibration sensor
btn_status = False  # Stores the current state of the push button

# ==========================================
# --- Hardware Initialization ---
# ==========================================
# 1) Vibration Setup
led_gp0 = digitalio.DigitalInOut(board.GP0)
led_gp0.direction = digitalio.Direction.OUTPUT
led_gp0.value = False

vib_sensor = VibrationSensor(board.GP22)

# 2) Button Setup
led_gp1 = digitalio.DigitalInOut(board.GP1)
led_gp1.direction = digitalio.Direction.OUTPUT
led_gp1.value = False

# ==========================================
# --- pyRTOS Task Definitions ---
# ==========================================

def vibration_task(self):
    """Task 1: Monitors vibration, updates global status, controls LED."""
    global vib_status # Declare intent to modify the global variable
    yield 

    while True:
        # Update the global variable
        vib_status = vib_sensor.is_vibrating()
        
        # Instantly toggle the LED based on the status
        if vib_status:
            led_gp0.value = True
        else:
            led_gp0.value = False
            
        yield [pyRTOS.timeout(0.05)] # 50ms polling

def button_task(self):
    """Task 3: Monitors button, updates global status, controls LED."""
    global btn_status # Declare intent to modify the global variable
    
    btn_gp21 = digitalio.DigitalInOut(board.GP21)
    btn_gp21.direction = digitalio.Direction.INPUT
    btn_gp21.pull = digitalio.Pull.UP 
    yield 

    while True:
        # Update the global variable (Active Low logic)
        btn_status = not btn_gp21.value 
        
        # Instantly toggle the LED based on the status
        if btn_status:
            led_gp1.value = True      
        else:
            led_gp1.value = False     
            
        yield [pyRTOS.timeout(0.15)] # 150ms polling

def temp_task(self):
    """Task 2: Prints internal temperature alongside button and vibration status."""
    yield 

    while True:
        # Fetch the internal temperature
        temp_c = microcontroller.cpu.temperature
        
        # Format the global statuses into readable text
        v_text = "DETECTED" if vib_status else "Clear"
        b_text = "PRESSED" if btn_status else "Released"
        
        # Print everything cleanly on a single line
        print(f"Temp: {temp_c:.2f} °C | Vibration: {v_text} | Button: {b_text}")
        
        yield [pyRTOS.timeout(2.0)] # Print every 2 seconds


# ==========================================
# --- pyRTOS Setup and Execution ---
# ==========================================
print("Adding tasks to pyRTOS scheduler...")

pyRTOS.add_task(pyRTOS.Task(vibration_task, name="Vibration_Monitor", priority=1))
pyRTOS.add_task(pyRTOS.Task(temp_task, name="Temperature_Monitor", priority=2))
pyRTOS.add_task(pyRTOS.Task(button_task, name="Button_Monitor", priority=3))

print("Starting pyRTOS scheduler...")
pyRTOS.start()
