# vib.py
import digitalio

class VibrationSensor:
    def __init__(self, pin):
        """Initializes the vibration sensor on the specified pin."""
        self.sensor = digitalio.DigitalInOut(pin)
        self.sensor.direction = digitalio.Direction.INPUT
        # Assuming Active Low requires an internal pull-up to stay HIGH when idle
        self.sensor.pull = digitalio.Pull.UP

    def is_vibrating(self):
        """Returns True if vibration is detected (Active Low logic)."""
        # Because it's active low, a False reading means it is triggered
        return not self.sensor.value