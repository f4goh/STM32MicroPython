from machine import I2C
import LPS22
from pyb import Timer

i2c = I2C(1)
lps = LPS22.LPS22(i2c)

def tim_irq(t):
    print(lps.get_irq())

tim = Timer(1, freq = 1)
tim.callback(tim_irq)
