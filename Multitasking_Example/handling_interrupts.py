'''
Handling Interrupts

Additional Library:
    - asyncio
    - adafruit_ticks.mpy
    
Reference:

https://learn.adafruit.com/cooperative-multitasking-in-circuitpython-with-asyncio/handling-interrupts
'''

import asyncio
import board
import countio
import digitalio
import time

def blink(pin, interval, count):
    with digitalio.DigitalInOut(pin) as led:
        led.switch_to_output(value=False)
        for _ in range(count):
            led.value = True
            time.sleep(interval)
            led.value = False
            time.sleep(interval)   
    
async def catch_interrupt(pin):
    """Print a message when pin goes low."""
    with countio.Counter(pin) as interrupt:
        while True:
            if interrupt.count > 0:
                interrupt.count = 0
                print("interrupted!")
                blink(board.GP0, 0.25, 10)
            # Let another task run.
            blink(board.GP1, 0.5, 5)
            await asyncio.sleep(0)

async def main():
    interrupt_task = asyncio.create_task(catch_interrupt(board.GP21))
    await asyncio.gather(interrupt_task)

asyncio.run(main())
