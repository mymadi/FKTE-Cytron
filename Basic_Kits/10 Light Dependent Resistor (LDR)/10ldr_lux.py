'''
- A Light Dependent Resistor (LDR) at the Bottom
- Convert it into Lux

Link:
1) Module: https://my.cytron.io/p-light-sensor-module
2) Schematic: https://static.cytron.io/download/usr_attachment/LDR%20Sensor%20Module.pdf
3) https://github.com/mymadi/FKTE-Cytron/blob/main/Basic_Kits/10%20Light%20Dependent%20Resistor%20(LDR)/A%20Light%20Dependent%20Resistor%20at%20Bottom.png
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
    lux = 500/(RLDR/1000)       # Conversion resistance to lumen
    return lux
    
while True:
    raw = ldr.value
    volts = get_voltage(raw)
    luxval = rtolux(raw)
    print("raw = {:5d} volts = {:.2f} light = {:.2f}".format(raw, volts, luxval))
    time.sleep(1)
