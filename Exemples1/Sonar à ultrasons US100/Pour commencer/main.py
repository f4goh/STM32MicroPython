# Objet du script :
# Mesurer une distance avec le module UART sonar à ultrasons de Grove

from us100 import US100 # Pilote du sonar
from time import sleep # Pour temporiser

sonar = US100()

while True:
	print('Distance : %.1f cm ' % (sonar.distance_mm()/10), end="\r")
	sleep(0.1)	#Attente 100 milliseconde