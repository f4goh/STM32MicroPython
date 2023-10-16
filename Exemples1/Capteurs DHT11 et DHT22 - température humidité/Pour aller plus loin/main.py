# Exemple adapté de https://github.com/kurik/uPython-DHT22/blob/master/main.py
# Objet du script : Mise en œuvre du capteur de température et humidité DHT22
# Deuxième approche : utilisation d'une classe exploitant les interruption d'un timer

import dht22 # Pour gérer le DHT22
from time import sleep_ms # Pour temporiser

# Initialisation du pilote du DHT22.
# On a besoin du timer 2 pour celui-ci
dht22.init(timer_id = 2, data_pin = 'D2')

while True:

	# Pour gérer les exceptions
	try:
		# Recupération des mesures (2-uple)
		(hum, tem) = dht22.measure()
		
		# En cas de retour erroné sur les deux mesures simultanément
		if hum == 0 and tem == 0:
			raise ValueError("Erreur capteur")

		# Formattage (arrondis) des mesures
		temp = round(tem,1)
		humi = int(hum)

		# Affichage des mesures
		print('=' * 40) # Imprime une ligne de séparation
		print("Température : " + str(temp) + " °C")
		print("Humidité relative : " + str(humi) + " %")

	# Si une exception est survenue
	except Exception as e:
		print(str(e) + '\n')

	# Temporisation de deux secondes
	sleep_ms(2000)

