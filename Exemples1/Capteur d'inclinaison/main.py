# Objet : mise en œuvre d'un interrupteur à bille / capteur d'inclinaison

from time import sleep_ms # Pour la temporisation
from pyb import Pin

p_in = Pin('D4', Pin.IN, Pin.PULL_UP)

while True :

	sleep_ms(500) # Temporisation de 500 millisecondes

	etat = p_in.value() # Lecture du capteur, 0 si horizontal et 1 si incliné

	if etat:
		print("Incliné")
	else:
		print("Horizontal")