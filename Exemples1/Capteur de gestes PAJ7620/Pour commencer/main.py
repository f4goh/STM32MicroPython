# Objet du script :
# Test d'un module Grove capteur de gestes
# Code adapté de :
# https://github.com/itechnofrance/micropython/blob/master/librairies/paj7620/use_paj7620.py

import paj7620 # Pilotes pour l'anneau de LED RGB et le capteur de gestes
from time import sleep_ms # Pour temporiser et mesurer le temps écoulé
from machine import I2C # Pour gérer le bus I2C

# On utilise l'I2C n°1 de la carte NUCLEO-WB55 pour communiquer avec le capteur de gestes
i2c = I2C(1) 

# Pause d'une seconde pour laisser à l'I2C le temps de s'initialiser
sleep_ms(1000)

# Liste des adresses I2C des périphériques présents
print("Adresses I2C utilisées : " + str(i2c.scan()))

# Adresse du capteur sur le bus I2C : 0x73 
PAJ7620U2_ADR = const(0x73)

# Instanciation du capteur de gestes
g = paj7620.PAJ7620(i2c = i2c)

# Liste des gestes
gestures = [ "Aucun geste", "Avant", "Arrière", "Droite", "Gauche", "Haut", "Bas", "Sens horaire", "Sens anti-horaire", "Vague"]

while True:

	# Lecture du geste
	index = g.gesture()

	# Extrait le geste de la liste
	if index > 0 and index < 10:
		print(gestures[index])
	
	# Temporisation de 10 millisecondes
	sleep_ms(10)
