'''
Light Dependent Resistor (LDR)
Convert it into Lux
'''
import time
import board
import analogio

ldr = analogio.AnalogIn(board.GP26)           
R = 10000                       # ohm resistance value

def get_voltage(raw):
    return (raw * 3.3) / 65536

def rtolux (rawval):
    vout = get_voltage(rawval)
    RLDR = (vout*R)/(3.3-vout)
    lux = 500/(RLDR/1000)       # Conversion resitance to lumen
    return lux
    
while True:
    raw = ldr.value
    volts = get_voltage(raw)
    luxval = rtolux(raw)
    print("raw = {:5d} volts = {:.2f} light = {:.2f}".format(raw, volts, luxval))
    time.sleep(1)