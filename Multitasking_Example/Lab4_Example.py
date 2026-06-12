# code.py
import board
import digitalio
import pyRTOS
import microcontroller
from vib import VibrationSensor

# --- Hardware Initialization ---

# 1) Vibration Setup: LED on GP0, Sensor on GP22
led_gp0 = digitalio.DigitalInOut(board.GP0)
led_gp0.direction = digitalio.Direction.OUTPUT
led_gp0.value = False

vib_sensor = VibrationSensor(board.GP22)

# 2) Button Setup: LED on GP1
led_gp1 = digitalio.DigitalInOut(board.GP1)
led_gp1.direction = digitalio.Direction.OUTPUT
led_gp1.value = False

# --- pyRTOS Task Definitions ---

def vibration_task(self):
    """Task 1: Monitors the vibration sensor and controls LED on GP0."""
    yield # Initial yield to allow setup to complete

    while True:
        if vib_sensor.is_vibrating():
            led_gp0.value = True
            print("Vibration detected! LED (GP0) ON.")
        else:
            led_gp0.value = False
            
        yield [pyRTOS.timeout(0.05)] # Fast polling rate (50ms) to catch quick vibrations

def temp_task(self):
    """Task 2: Reads and prints the internal Pico temperature."""
    yield

    while True:
        # Fetch internal CPU temperature
        temp_c = microcontroller.cpu.temperature
        print(f"Internal Temperature: {temp_c:.2f} °C")
        
        yield [pyRTOS.timeout(2.0)] # Read temperature every 2 seconds

def button_task(self):
    """Task 3: Monitors push button (GP21) and controls LED (GP1)."""
    # Initialize the button on GP21
    btn_gp21 = digitalio.DigitalInOut(board.GP21)
    btn_gp21.direction = digitalio.Direction.INPUT
    btn_gp21.pull = digitalio.Pull.UP # Pull-up resistor for Active Low button
    yield

    while True:
        # Active low logic (False = pressed)
        if not btn_gp21.value: 
            led_gp1.value = True
            print("Push Button (GP21) pressed! LED (GP1) ON.")
        else:
            led_gp1.value = False
            
        yield [pyRTOS.timeout(0.15)] # Poll every 150ms for basic debounce

# --- pyRTOS Setup and Execution ---
print("Adding tasks to pyRTOS scheduler...")

# Register the 3 parts to the scheduler
pyRTOS.add_task(pyRTOS.Task(vibration_task, name="Vibration_Monitor", priority=1))
pyRTOS.add_task(pyRTOS.Task(temp_task, name="Temperature_Monitor", priority=2))
pyRTOS.add_task(pyRTOS.Task(button_task, name="Button_Monitor", priority=3))

print("Starting pyRTOS scheduler...")
pyRTOS.start()