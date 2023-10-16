import ble_sensor
import struct
import bluetooth
from onewire import OneWire
from machine import Pin, I2C
from time import sleep_ms,time
from ds18x20 import DS18X20
import ssd1306
import sys

# Screen settings
width_oled_screen = 128
height_oled_screen = 64


bus = OneWire(Pin('D12'))
ds = DS18X20(bus)
capteur_temperature = ds.scan()
ble = bluetooth.BLE()
ble_device = ble_sensor.BLESensor(ble)
i2c = I2C(1)

oled = ssd1306.SSD1306_I2C(width_oled_screen, height_oled_screen, i2c)
   
while True:
    try:        
        ds.convert_temp()       
        sleep_ms(1000)
        temp_celsius = ds.read_temp(capteur_temperature[0])
        print("Température : ",temp_celsius )
        oled.fill(0)
        oled.text("temperature", 0, 0)
        oled.text(str(temp_celsius), 0, 20)
        oled.show()
        timestamp = time()        
        ble_device.set_data_temperature(timestamp, int(temp_celsius*10), notify=1) # envoi en BLE du timestamp et de la température en choisissant de notifier l'application
    except KeyboardInterrupt:
        print('Ctrl-C pressed...exiting')
        sys.exit()