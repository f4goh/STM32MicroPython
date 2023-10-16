# Objet du code : 
# Mise en œuvre du module Grove BME680 capteur de température, humidité, pression et qualité d'air.
# Ressource adaptée du site : https://RandomNerdTutorials.com/MicroPython-bme680-esp32-esp8266/

from machine import Pin, I2C # Gestion des broches et de l'I2C
from time import sleep # Gestion des temporisations	
import bme680 # Pilotes du module Grove BME680 

# On utilise l'I2C n°1 de la carte NUCLEO-WB55 pour communiquer avec le capteur
i2c = I2C(1)

# Pause d'une seconde pour laisser à l'I2C le temps de s'initialiser
sleep(1)

# Liste des adresses I2C des périphériques présents
print("Adresses I2C utilisées : " + str(i2c.scan()) + "\n")

# Instanciation du capteur
bme = bme680.BME680_I2C(i2c=i2c)

# Décompte du nombre de séries de mesures
nbmes = 0

while True:
	
	# Affiche la série de mesures
	nbmes = nbmes + 1
	print('Série de mesures numéro : ', nbmes)

	# Structure pour intercepter d'éventuelles erreurs
	try: # Essaies de faire tout ce qui suit...

		# Lecture du capteur
		temp = bme.temperature
		hum = bme.humidity
		pres = bme.pressure
		gas = bme.gas*0.001

		# Affichage des mesures sur le terminale série de l'USB User
		print('-' * 40)  # Imprime une ligne de séparation
		print('Température : %.1f °C' %temp)
		print('Humidité relative : %1d %%' %hum)
		print('Pression : %1d hPa' %pres)
		print('Résistance sensible aux COV : %1d kOhms' %gas)

	except OSError as e: # Si une erreur est survenue dans le bloc "try"...
		
		print('Erreur de lecture du capteur !')

	sleep(30) # Temporisation ; prochaine mesure dans 30 secondes.