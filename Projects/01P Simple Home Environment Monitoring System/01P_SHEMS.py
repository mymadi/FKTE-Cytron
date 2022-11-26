'''
Simple Home Environment Monitoring System
- Serial LCD
- DHT22 Sensor
- LDR Sensor

References:
  [1] https://github.com/Guitarman9119/Raspberry-Pi-Pico-/tree/main/I2C%2016x2%20LCD%20Circuit%20Python

Additional Library:
- lcd.py from [1]
- i2c_pcf8574_interface.py from [1]
- adafruit_dht.mpy
'''
import board
import time
import busio
import digitalio
import analogio
# Needs these 3 libraries
# Upload it to the 'Lib'
import adafruit_dht
import lcd
import i2c_pcf8574_interface

# DHT22
dht22 = adafruit_dht.DHT22(board.GP7)
# LDR
ldr = analogio.AnalogIn(board.GP26)           
R = 10000                       # ohm resistance value
# Serial LCD
i2c = busio.I2C(scl=board.GP5, sda=board.GP4)
address = 0x3F
i2c = i2c_pcf8574_interface.I2CPCF8574Interface(i2c, address)
display = lcd.LCD(i2c, num_rows=2, num_cols=16)
display.set_backlight(True)
display.set_display_enabled(True)

def read_dht22():
    try:
        temperature = dht22.temperature
        humidity = dht22.humidity
        
        #print("Temperature: {:.2f} °C, Humidity: {:.2f} %RH ".format(temperature, humidity))

    except RuntimeError as error:
        print(error.args[0])
        time.sleep(2.0)
        display.clear()
        display.set_cursor_pos(0, 0)
        display.print("DHT Sensor Not  Found!")
    except Exception as error:
        dht22.exit()
        raise error
        display.clear()
        display.set_cursor_pos(0, 0)
        display.print("Error")
    
    return [temperature,humidity]

def get_voltage(raw):
    return (raw * 3.3) / 65536

def rtolux (rawval):
    vout = get_voltage(rawval)
    RLDR = (vout*R)/(3.3-vout)
    lux = 500/(RLDR/1000)       # Conversion resitance to lumen
    return lux

display.clear()
display.set_cursor_pos(0, 0)
display.print("  Project 1\n    SHEMS")
time.sleep(2)
    
while True:
    # Read the Sensors
    datadht22 = read_dht22()
    raw = ldr.value
    luxval = rtolux(raw)
    
    print("Temperature: {:.2f} °C, Humidity: {:.2f} %RH, Lux: {:.2f} lx".format(datadht22[0], datadht22[1], luxval))
   
    display.clear()
    display.set_cursor_pos(0, 0)
    display.print("Temp(C) = {:.2f}".format(datadht22[0]))
    display.set_cursor_pos(1, 0)
    display.print("Humi(%) = {:.2f}".format(datadht22[1]))
    time.sleep(2)
    display.clear()
    display.set_cursor_pos(0, 0)
    display.print("Lux(lx) = {:.2f}".format(luxval))
    time.sleep(2)