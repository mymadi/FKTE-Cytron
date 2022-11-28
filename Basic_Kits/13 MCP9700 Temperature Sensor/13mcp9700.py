'''
MCP9700 Temperature Sensor

References:
[1] Datasheet, https://drive.google.com/file/d/1RkvPfGPVTxeZoKctQkr2t4XRbr2ieJT6/view
[2] https://startingelectronics.org/beginners/start-electronics-now/tut15-arduino-serial-thermometer/
'''
import time
import board
import analogio

# create an ADC object acting on a pin
mcp = analogio.AnalogIn(board.GP26)   

def get_voltage(raw):
    return (raw * 3.3) / 65536

def mcp9700(val):
    # Calibrating to 0°C – the difference between voltage read from the sensor
    # and 500 mV is linearily dependent on temperature.
    temperature = (val*3.3/65535)-0.5
    # This difference is divided by 10mV/step and now we have temperature
    temperature = temperature / 0.01;
    #temperature = ((val*3.3/65535)-0.5)/(10/1000)
    return temperature

while True:
    # Reading value from analog input
    raw = mcp.value
    volts = get_voltage(raw)
    temp = mcp9700(raw)
    
    print("raw = {:5d} volts = {:.3f} Temperature = {:.2f}".format(raw, volts, temp))
    time.sleep(1)
