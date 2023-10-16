# Objet du script : Mise en œuvre du module Grove - Laser PM2.5 Sensor (HM3301)
# Fiche technique : 
# https://files.seeedstudio.com/wiki/Grove-Laser_PM2.5_Sensor-HM3301/res/HM-3300%263600_V2.1.pdf
# Ce module donne une estimation de la masse moyenne des particules présentes dans un mètre-cube 
# d'air selon leur diamètre approximatif : 1 µm, 2.5 µm ou 10 µm.

from time import sleep_ms # Pour gérer les temporisations
from machine import I2C # Pour gérer l'I2C
import hm3301 # Pour gérer le capteur 

# On utilise l'I2C n°1 de la carte NUCLEO-WB55 pour communiquer avec le capteur
i2c1 = I2C(1)

# Pause d'une seconde pour laisser à l'I2C le temps de s'initialiser
sleep_ms(1000)

# Liste des adresses I2C des périphériques présents
print("Adresses I2C utilisées : " + str(i2c1.scan()))

# Instanciation du capteur
sensor = hm3301.HM3301(i2c=i2c1)

while True :
	
	# Concentration massique des particules de taille 1 µm
	std_PM1 = sensor.getData(0)
	# Concentration massique des particules de taille 2.5 µm
	std_PM2_5 = sensor.getData(1)
	# Concentration massique des particules de taille 10 µm
	std_PM10 = sensor.getData(2)
	
	# Affichage
	print("Concentration des particules : ")
	print(" - De taille 1 µm : %d µg/m^3" % std_PM1)
	print(" - De taille 2,5 µm : %d µg/m^3" % std_PM2_5)
	print(" - De taille 10 µm : %d µg/m^3\n" % std_PM10)
	
	# Temporisation de 5 secondes
	sleep_ms(5000)