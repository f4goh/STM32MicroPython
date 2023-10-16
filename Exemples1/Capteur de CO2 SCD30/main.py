# Objet du script : Mise en œuvre du module I2C Grove SCD30.
# Source : https://pypi.org/project/micropython-scd30/

from time import sleep_ms
from machine import I2C, Pin
from scd30 import SCD30

# On utilise l'I2C n°1 de la carte NUCLEO-W55 pour communiquer avec le capteur
i2c = I2C(1)

# Pause d'une seconde pour laisser à l'I2C le temps de s'initialiser
sleep_ms(1000)

# Liste des adresses I2C des périphériques présents
print("Adresses I2C utilisées : " + str(i2c.scan()))

# Instanciation du capteur
I2C_ADDRESS = const(0x61)
scd30 = SCD30(i2c, addr = I2C_ADDRESS)

# Corrige la pression grâce à l'altitude du lieu (en m)
altitude = 0

while True:

	# Attend que le capteur renvoie des valeurs (par défaut toutes les 2 secondes)
	while scd30.get_status_ready() != 1:
		sleep_ms(200)

	# Lecture des valeurs mesurées
	scd30data = scd30.read_measurement() 

	# Séparation et formattage (arrondis) des mesures
	conco2 = int(scd30data[0])
	temp = round(scd30data[1],1)
	humi = int(scd30data[2])

	# Affichage des mesures
	# Syntaxe utilisant la conversion en chaines de caractères plutôt que
	# les instructions de formattage de Python
	print('=' * 40) # Imprime une ligne de séparation
	print("Concentration en CO2 : " + str(conco2) + " ppm")
	print("Température : " + str(temp) + " °C")
	print("Humidité relative : " + str(humi) + " %")
