# Exemple adapté de https://github.com/blaa/th02-sensor/blob/master/
# Objet du script : Mise en œuvre du module grove I2C capteur de température 
# et humidité basé sur le capteur TH02

from time import sleep_ms
from machine import I2C, Pin
from th02 import TH02

# On utilise l'I2C n°1 de la carte NUCLEO-WB55 pour communiquer avec le capteur
i2c = I2C(1)

# Pause d'une seconde pour laisser à l'I2C le temps de s'initialiser
sleep_ms(1000)

# Liste des adresses I2C des périphériques présents
print("Adresses I2C utilisées : " + str(i2c.scan()))

# Instanciation du capteur
th = TH02(i2c=i2c)

while True:

	# Temporisation d'une seconde
	sleep_ms(1000)
	
	# Lecture des valeurs mesurées
	humi = th.get_humidity()
	temp = th.get_temperature()

	# Affichage formatté des mesures
	print('=' * 40) # Imprime une ligne de séparation
	
	# Affiche la température en degrés Celsius.
	print("Température : %.1f °C" %temp)
	
	# Affiche l'humidité en pourcents. 
	# Attention, le caractère '%' à la fin est dédoublé pour ne pas être interprété
	# comme une instruction de formattage !
	print("Humidité relative : %.1f %%" %humi)
