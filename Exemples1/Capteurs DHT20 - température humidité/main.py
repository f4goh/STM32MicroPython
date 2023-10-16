# Objet du script : Mise en œuvre du module Grove I2C capteur de pression,
# température et humidité basé sur le DHT22
# Source : https://github.com/flrrth/pico-dht20/tree/main

from time import sleep_ms
from machine import I2C
import dht20

# On utilise l'I2C n°1 de la carte NUCLEO-WB55 pour communiquer avec le capteur
i2c1 = I2C(1)

# Pause d'une seconde pour laisser à l'I2C le temps de s'initialiser
sleep_ms(1000)

# Liste des adresses I2C des périphériques présents
print("Adresses I2C utilisées : " + str(i2c1.scan()))

# Instanciation du capteur
dht = dht20.DHT20(i2c=i2c1)

while True:

	measurements = dht.measurements
	print(f"Température : {measurements['t']} °C, humidité : {measurements['rh']} %RH")
	sleep_ms(1000)