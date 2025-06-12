'''
RTOS Module
Exercise 4: Two Blinking LEDs using 'pyRTOS'
'''
import board
import digitalio
import time
import pyRTOS

# --- Task Definitions ---
def onboard_led_task(self):
    """
    Task to control the onboard LED, blinking at a 0.5-second interval.
    """
    led_onboard = digitalio.DigitalInOut(board.LED)
    led_onboard.direction = digitalio.Direction.OUTPUT
    led_onboard.value = False # Ensure LED starts off
    print("Onboard LED Task Initialized.")
    yield # Initial yield to allow setup to complete before loop
    
    onboard_interval = 0.5 # seconds
    while True:
        led_onboard.value = not led_onboard.value # Toggle LED state
        print(f"Onboard LED: {'ON' if led_onboard.value else 'OFF'}")
        # Yield control for the specified interval.
        # pyRTOS will resume this task after the timeout, allowing other tasks to run.
        yield [pyRTOS.timeout(onboard_interval)]

def external_led_task(self):
    """
    Task to control an external LED on GP0, blinking at a 0.2-second interval.
    """
    # Set up an external LED on GP0 (replace with your desired pin if different)
    led_external_pin = board.GP0
    led_external = digitalio.DigitalInOut(led_external_pin)
    led_external.direction = digitalio.Direction.OUTPUT
    led_external.value = False # Ensure LED starts off
    print(f"External LED Task (GP0) Initialized.")
    yield # Initial yield
    
    external_interval = 0.2 # seconds
    while True:
        led_external.value = not led_external.value # Toggle LED state
        print(f"External LED (GP0): {'ON' if led_external.value else 'OFF'}")
        # Yield control for the specified interval.
        yield [pyRTOS.timeout(external_interval)]

# --- RTOS Setup ---
print("Preparing to add tasks to pyRTOS scheduler...")

# 1. Create Task instances for each of our defined tasks.
task_onboard_led = pyRTOS.Task(onboard_led_task, name="OnboardLED", priority=1)
task_external_led = pyRTOS.Task(external_led_task, name="ExternalLED_GP0", priority=2)

# 2. Add each task instance to the pyRTOS scheduler.
pyRTOS.add_task(task_onboard_led)
pyRTOS.add_task(task_external_led)

print("Starting pyRTOS scheduler...")
# 3. Start the pyRTOS scheduler.
pyRTOS.start()

print("Scheduler stopped. (This message implies all tasks have terminated, which is unlikely for this code)")
