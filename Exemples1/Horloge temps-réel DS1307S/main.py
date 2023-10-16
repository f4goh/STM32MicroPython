# Objet du script :
# Démonstration de la mise en œuvre d'un module RTC utilisant un composant
# DS1307 de Maxim Integrated (fiche technique : https://datasheets.maximintegrated.com/en/ds/DS1307.pdf)
# Pilote adapté à partir de la source à l'adresse suivante :
# https://github.com/mcauser/micropython-tinyrtc-i2c/blob/master/ds1307.py
# ATTENTION, pour fonctionner correctement ce module doit être alimenté en 5V


from ds1307 import DS1307 # Pilote du ds1307
from machine import I2C # Pilote du bus I2C
from time import sleep # Pour temporiser

# On utilise l'I2C n°1 de la carte NUCLEO-WB55 pour communiquer avec le capteur
i2c = I2C(1) 

# Pause d'une seconde pour laisser à l'I2C le temps de s'initialiser
sleep(1)

# On crée une instance de la RTC
ds = DS1307(i2c)

# On fixe la date au 26 aout 2021 (4eme jour de la semaine)
# On fixe l'heure à 23heures 59min 0sec
ds.setDateTime([2021, 8, 26, 4, 23, 59, 58, 0])

# On affiche pendant une minute, toutes les secondes, l'heure et la date
for i in range(60):
	print(ds.readDateTime())
	sleep(1)

# On arrète l'horloge 
ds.halt(True)