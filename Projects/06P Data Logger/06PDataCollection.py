'''
Pi Pico W: Data Collection

Components:
    - DHT22 Module
    - LDR Module
    - SD Card Module
    - RTC ds1370 Module
    - Buzzer

Additional libraries
  - simpleio.mpy
  - adafruit_dht.mpy
  - adafruit_ds1307.mpy
'''

import time
import sdcardio
import board
import busio
import digitalio
import storage
import microcontroller
import adafruit_dht
import analogio
import simpleio
import adafruit_ds1307

# RTC ds1307
i2c = busio.I2C(scl=board.GP1, sda=board.GP0)
rtc = adafruit_ds1307.DS1307(i2c)
# Lookup table for names of days (nicer printing).
days = ("Monday", "Tuesday", "Wednesday", "Thursday", "Friday", "Saturday", "Sunday")

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
led = digitalio.DigitalInOut(board.GP9)
led.direction = digitalio.Direction.OUTPUT

# Buzzer
NOTE_G4 = 392
NOTE_C5 = 523
buzzer = board.GP18

# DHT22
dht22 = adafruit_dht.DHT22(board.GP7)

# LDR
ldr = analogio.AnalogIn(board.GP26)           
R = 10000                       # ohm resistance value

# Read DHT22 Sensor
def readDHT22():
    temperature = dht22.temperature
    humidity = dht22.humidity
    return temperature, humidity

# Read LDR Sensor
def rtolux():
    raw = ldr.value
    vout = (raw * 3.3) / 65536
    RLDR = (vout*R)/(3.3-vout)
    lux = 500/(RLDR/1000)       # Conversion resitance to lumen
    return lux

print("Pi Pico W: Data Collection ^_^")
# append to the file!
while True:
    try:
    # open file for append
        with open("/sd/data02.txt", "a") as f:
            t = rtc.datetime
            led.value = True  # turn on LED to indicate we're writing to the file
            # Read the Sensors
            dhtval = readDHT22()
            luxval = rtolux()
            temp = round(dhtval[0],2)
            humi = round(dhtval[1],2)
            lux = round(luxval,2)
            
            f.write("{}:{:02}:{:02},{:.2f},{:.2f},{:.2f}\n".format(t.tm_hour,t.tm_min,t.tm_sec,temp,humi,lux))
            led.value = False  # turn off LED to indicate we're done
            simpleio.tone(buzzer, NOTE_G4, duration=0.15)
            
            # Print the Data
            print(
            "The date is {} {}/{}/{}".format(
                days[int(t.tm_wday)], t.tm_mday, t.tm_mon, t.tm_year
                )
            )
            print("The time is {}:{:02}:{:02}".format(t.tm_hour, t.tm_min, t.tm_sec))
            print("Temperature: {:.2f} °C, Humidity: {:.2f} %RH, Lux: {:.2f} lx ".format(temp, humi,lux))
            #print(t)
            # file is saved
            time.sleep(10)
            
    except OSError as e:  # Typically when the filesystem isn't writeable...
        delay = 0.5  # ...blink the LED every half second.
        if e.args[0] == 28:  # If the filesystem is full...
            delay = 0.25  # ...blink the LED faster!
        while True:
            led.value = not led.value
            time.sleep(delay)
