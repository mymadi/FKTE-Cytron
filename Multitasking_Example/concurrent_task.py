'''
Concurrent Tasks

Additional Library:
    - asyncio
    - adafruit_ticks.mpy
    
Reference:

https://learn.adafruit.com/cooperative-multitasking-in-circuitpython-with-asyncio/overview
'''
import asyncio
import board
import digitalio


async def blink(pin, interval, count):
    with digitalio.DigitalInOut(pin) as led:
        led.switch_to_output(value=False)
        for _ in range(count):
            led.value = True
            await asyncio.sleep(interval)  # Don't forget the "await"!
            led.value = False
            await asyncio.sleep(interval)  # Don't forget the "await"!


async def main():
    led1_task = asyncio.create_task(blink(board.GP0, 0.5, 10))
    led2_task = asyncio.create_task(blink(board.GP1, 0.1, 20))

    await asyncio.gather(led1_task, led2_task)  # Don't forget "await"!
    print("done")


asyncio.run(main())
