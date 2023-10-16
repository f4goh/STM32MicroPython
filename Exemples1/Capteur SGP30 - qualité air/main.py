# Exemple adapté de https://github.com/safuya/micropython-sgp30/blob/master/
# Objet du script : Mise en œuvre du module grove I2C capteur de gas COV et CO2
# basé sur le capteur SGP30

from time import sleep_ms
from machine import I2C, Pin
from sgp30 import SGP30

# On utilise l'I2C n°1 de la carte NUCLEO-WB55 pour communiquer avec le capteur
i2c = I2C(1)

# Pause d'une seconde pour laisser à l'I2C le temps de s'initialiser
sleep_ms(1000)

# Liste des adresses I2C des périphériques présents
print("Adresses I2C utilisées : " + str(i2c.scan()))

# Instanciation du capteur
sgp = SGP30(i2c)

while True:

	# Temporisation d'une seconde
	sleep_ms(1000)

	# Lecture des valeurs mesurées
	co2eq, tvoc = sgp.indoor_air_quality

	# Affichage formatté des valeurs mesurées
	print("CO2eq = %d ppm \t TVOC = %d ppb" % (co2eq, tvoc))
