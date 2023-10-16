from machine import I2C
import LIS2DW12
import pyb
import time

i2c = I2C(1) # On utilise l'I2C n°1 de la carte NUCLEO-W55 pour communiquer avec le capteur LISDW12
accelerometre = LIS2DW12.LIS2DW12(i2c)

led_bleu = pyb.LED(1)
led_vert = pyb.LED(2)
led_rouge = pyb.LED(3)

while(1):
    time.sleep_ms(500)
    if abs(accelerometre.x()) > 700 : # Si la valeur absolue de l'accélération sur l'axe X est supérieur à 700 mG alors
        led_vert.on()
    else:
        led_vert.off() 
    if abs(accelerometre.y()) > 700 : # Si la valeur absolue de l'accélération sur l'axe Y est supérieur à 700 mG alors
        led_bleu.on()
    else:
        led_bleu.off() 
    if abs(accelerometre.z()) > 700 : # Si la valeur absolue de l'accélération sur l'axe Z est supérieur à 700 mG alors
        led_rouge.on()
    else:
        led_rouge.off() 
    
