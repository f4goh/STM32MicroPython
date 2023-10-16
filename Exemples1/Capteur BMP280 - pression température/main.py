# Objet du script : Mise en œuvre du module Grove I2C capteur de pression,
# et température basé sur le BMP280.
# Une estimation de la température est également donnée.
# Le driver provient de cette source :
# Author David Stenwall (david at stenwall.io)
# https://github.com/dafvid/micropython-bmp280

from time import sleep_ms
from machine import I2C
from bmp280 import *

# Pression normalisée au niveau de la mer, pour le calcul de l'atitude.
# Attention, cette valeur change localement avec la météo !
# Pour la France, vous trouverez une valeur mesurée à proximité de 
# chez vous sur ce site :
# https://www.meteociel.fr/observations-meteo/pression.php

SEE_LEVEL_PRESSURE = 1013.25

# On utilise l'I2C n°1 de la carte NUCLEO-WB55 pour communiquer avec le capteur
i2c1 = I2C(1)

# Pause d'une seconde pour laisser à l'I2C le temps de s'initialiser
sleep_ms(1000)

# Liste des adresses I2C des périphériques présents
print("Adresses I2C utilisées : " + str(i2c1.scan()))

# Instanciation du capteur
bmp = BMP280(i2c1, addr = 0x77 )

# Mise en sommeil du capteur
bmp.sleep()

while True:

	# Temporisation d'une seconde
	sleep_ms(1000)
	
	# Reveil du capteur
	bmp.normal_measure()
	
	# Lecture de la température
	temperature = bmp.temperature
	
	# Lecture de la pression
	pressure = bmp.pressure
	
	# Estimation de l'altitude
	altitude = 44330*(1-(pressure/SEE_LEVEL_PRESSURE)**(1/5.255))

	# Affichage des mesures
	print('=' * 40) # Imprime une ligne de séparation
	print("Température : %.1f °C" %temperature)
	print("Pression : %1d hPa" %pressure)
	print("Altitude : %1d m" %altitude) 
	
	# Mise en sommeil du capteur
	bmp.sleep()