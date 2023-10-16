# Objet du script : Mise en œuvre d'un capteur/interrupteur tactile

from pyb import Pin
from time import  sleep_ms # Pour temporiser

p_in = Pin('D4', Pin.IN, Pin.PULL_UP)

while True :
	
	sleep_ms(500) # Temporisation de 500 millisecondes

	if p_in.value() == 1: # Si on touche le capteur
		print("ON")
	else: # Autrement
		print("OFF")