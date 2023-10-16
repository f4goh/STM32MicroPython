# Objet du script :
# Mise en œuvre d'un capteur/interrupteur tactile

from pyb import Pin
from time import sleep_ms # Pour temporiser

i1 = Pin('D4', Pin.IN, Pin.PULL_UP)
i2 = Pin('D5', Pin.IN, Pin.PULL_UP)

while True :
	
	sleep_ms(500) # Temporisation de 500 millisecondes

	if i1.value() == 1: # Si on touche le premier interrupteur
		print("Interrupteur 1 : ON")
	else: # Autrement
		print("Interrupteur 1 : OFF")

	if i2.value() == 1: # Si on touche le second interrupteur
		print("Interrupteur 2 : ON")
	else: # Autrement
		print("Interrupteur 2 : OFF")
