'''
Pi Pico W with Sd Card Example

Reference:
[1] https://learn.adafruit.com/adafruit-micro-sd-breakout-board-card-tutorial/circuitpython
'''

import time
import sdcardio
import board
import busio
import digitalio
import storage
import microcontroller

# Chip Select
SD_CS = board.GP5

# Connect to the card and mount the filesystem.
#                   CLK         MOSI        MISO
spi = busio.SPI(board.GP2, board.GP3, board.GP4)
#cs = digitalio.DigitalInOut(SD_CS)
sdcard = sdcardio.SDCard(spi, SD_CS)
vfs = storage.VfsFat(sdcard)
storage.mount(vfs, "/sd")

# Indicator LED
led = digitalio.DigitalInOut(board.GP0)
led.direction = digitalio.Direction.OUTPUT

print("Pi Pico W: Logging Internal Temperature to filesystem ^_^")
# append to the file!
while True:
    # open file for append
    with open("/sd/datalog01.txt", "a") as f:
        led.value = True  # turn on LED to indicate we're writing to the file
        temp = microcontroller.cpu.temperature
        print("Temperature: {:.2f} °C".format(temp))
        f.write('{:.2f}\n'.format(temp))
        led.value = False  # turn off LED to indicate we're done
    # file is saved
    time.sleep(5)
