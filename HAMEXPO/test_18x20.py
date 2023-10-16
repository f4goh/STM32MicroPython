# DS18x20 temperature sensor driver for MicroPython.
# MIT license; Copyright (c) 2016 Damien P. George

from onewire import OneWire
from machine import Pin, I2C
from time import sleep_ms
from ds18x20 import DS18X20
import sys


bus = OneWire(Pin('D12'))
ds = DS18X20(bus)
capteur_temperature = ds.scan()
    
while True:
    try:        
        ds.convert_temp()       
        sleep_ms(750)
        temp_celsius = ds.read_temp(capteur_temperature[0])
        print("Température : ",temp_celsius )
    except KeyboardInterrupt:
        print('Ctrl-C pressed...exiting')
        sys.exit()
        
