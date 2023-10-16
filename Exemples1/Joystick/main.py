# Objet du script : Mise en œuvre du Joystick Grove.

from time import sleep_ms # Pour temporiser
from pyb import Pin

vertical = ADC(PIN('A0')) #en branchant le joystick sur A0,l'axe Y sera lu par A0 et l'axe X par A1
horizontal= ADC(PIN('A1')) #sur A1, Y sera lu par A1 et X par A2; sur A2, Y sera lu par A2 et X par A3..

while True :

	sleep_ms(500)
	
	x = vertical.read()
	y = horizontal.read()

	if x <= 780 and x >= 750 :
		print("Haut")
	if x <= 280 and x >= 240 :
		print("Bas")
	if y <= 780 and y >= 750 :
		print("Gauche")
	if y <= 280 and y >= 240 :
		print("Droite")
	if x >= 1000: # En appuyant sur le joystick, la sortie de l'axe X se met à 1024, le maximum.
		print("Appuyé")
