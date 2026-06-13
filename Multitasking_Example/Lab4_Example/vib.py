# vib.py
import digitalio

class VibrationSensor:
    def __init__(self, pin):
        """Initializes the vibration sensor on the specified pin."""
        self.sensor = digitalio.DigitalInOut(pin)
        self.sensor.direction = digitalio.Direction.INPUT
        # Active High requires an internal pull-down to stay LOW when idle
        self.sensor.pull = digitalio.Pull.DOWN

    def is_vibrating(self):
        """Returns True if vibration is detected (Active High logic)."""
        # Because it's active high, a True reading means it is triggered
        return self.sensor.value
