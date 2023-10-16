#SCL D15, SDA D14
from machine import Pin, I2C
import ssd1306
from time import sleep

#Init I2C1
i2c = I2C(1)

print('Scan i2c bus...')
devices = i2c.scan()

if len(devices) == 0:
    print("No i2c device !")
else:
    print('i2c devices found:',len(devices))

for device in devices:  
    print("Decimal address: ",device," | Hexa address: ",hex(device))
    