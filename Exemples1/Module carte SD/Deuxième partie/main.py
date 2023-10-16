# Objet du script : Mise en œuvre du module grove I2C capteur de pression,
# température et humidité basé sur le capteur BME280
# Enregistre les mesures dans un fichier sur une carte SD 

import os,pyb,time,sdcard,bme280	# Pilotes pour lire-écrire des fichiers, pour temporiser, 
									# du module carte SD et du capteur bme280.
from machine import I2C, Pin # Pilotes du contrôleur de bus I2C et des entrées-sorties
from pyb import SPI # Pilote du contrôleur de bus SPI

# On utilise l'I2C n°1 de la carte NUCLEO-W55 pour communiquer avec le capteur
i2c = I2C(1)

# Pause d'une seconde pour laisser à l'I2C le temps de s'initialiser
time.sleep_ms(1000)

# Liste des adresses I2C des périphériques présents
print("Adresses I2C utilisées : " + str(i2c.scan()))

# Instanciation du capteur
bme = bme280.BME280(i2c=i2c)

spi = SPI(1, SPI.MASTER, baudrate=100000, polarity=1, phase=0) # Instance du bus SPI
sd = sdcard.SDCard(spi, machine.Pin('D9')) # Broche de sélection du module carte SD

vfs = os.VfsFat(sd) # Déclaration d'un système de fichier FAT
os.mount(vfs, "/fc") # Montage du volume logique associé au module carte SD

fname = "/fc/log.csv"

with open(fname, "w") as log: # Ouverture du fichier "log.csv" en écriture
	
	n = log.write("Temps,Temp,Pres,Humi" + '\n')
	
	while True:

		# Temporisation d'une seconde
		time.sleep_ms(1000)
	
		# Lecture des valeurs mesurées
		bme280data = bme.values
	
		# Séparation et formattage (arrondis) des mesures
		temp = round(bme280data[0],1)
		press = int(bme280data[1])
		humi = int(bme280data[2])

		# Affichage des mesures
		print('=' * 40)  # Imprime une ligne de séparation
		print("Température : " + str(temp) + " °C")
		print("Pression : " + str(press) + " hPa")
		print("Humidité relative : " + str(humi) + " %")
	
		# Ecriture dans un fichier "log.csv" de la carte SD
		t = time.ticks_ms() # Etiquette de temps 
		# écriture dans le fichier
		#n = log.write(str(t) + "," + str(temp) + "," + str(press) + "," + str(humi) + '\n')
		n = log.write("{},{},{},{}\n".format(t, temp, press, humi))
		print(n, "octets écrits")
