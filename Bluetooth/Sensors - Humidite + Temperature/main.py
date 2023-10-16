import ble_sensor
import struct
import bluetooth
import time
import random

def demo():
    ble = bluetooth.BLE()
    ble_device = ble_sensor.BLESensor(ble)
    
    while True:
        timestamp = time.time()

        humidity = random.randint(0, 1000) # valeur aléatoire entre 0 et 100,0%
        temperature = random.randint(250, 350) # valeur aléatoire entre 25 et 35°C

        ble_device.set_data_ht(timestamp, humidity, temperature, True) 

        time.sleep_ms(1000)

if __name__ == '__main__':
    demo()