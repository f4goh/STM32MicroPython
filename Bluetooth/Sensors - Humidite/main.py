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
        humidity = (random.randint(0, 1000)) # valeur aléatoire entre 0 et 100,0 °C 
        ble_device.set_data_humidity(timestamp, humidity, notify=1) # envoi en BLE du timestamp et de l'humidité en choisissant de notifier l'application
        time.sleep_ms(1000)

if __name__ == '__main__':
    demo()