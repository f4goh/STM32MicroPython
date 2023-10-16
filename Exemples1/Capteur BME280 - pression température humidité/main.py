# Exemple adapté de https://GitHub.com/catdog2/mpy_bme280_esp8266
# Objet du script : Mise en œuvre du module Grove I2C capteur de pression,
# température et humidité basé sur le BME280

from time import sleep_ms # Pout temporiser
from machine import I2C # Pilote du bus I2C
import bme280 # Pilote du capteur 

# On utilise l'I2C n°1 de la carte NUCLEO-WB55 pour communiquer avec le capteur
i2c1 = I2C(1)

# Pause d'une seconde pour laisser à l'I2C le temps de s'initialiser
sleep_ms(1000)

# Liste des adresses I2C des périphériques présents
print("Adresses I2C utilisées : " + str(i2c1.scan()))

# Instanciation du capteur
sensor = bme280.BME280(i2c=i2c1)

while True:
	
	# Lecture des valeurs mesurées
	bme280data = sensor.values

	# Séparation des mesures
	temp = bme280data[0]
	press = bme280data[1]
	humi = bme280data[2]

	# Affichage des mesures
	print('=' * 40)  # Imprime une ligne de séparation
	print("Température : %.1f °C" %temp)
	print("Pression : %d hPa" %press)
	print("Humidité relative : %d %%" %humi)

	# Temporisation d'une seconde
	sleep_ms(1000)