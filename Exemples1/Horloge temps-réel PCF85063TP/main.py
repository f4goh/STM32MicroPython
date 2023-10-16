# Objet du script :
# Démonstration de la mise en œuvre d'un module High Precision RTC utilisant un composant
# PCF85063TP de NXP (fiche technique : https://www.nxp.com/docs/en/data-sheet/PCF85063TP.pdf)

from pcf85063tp import RTC_HP # Pilote du PCF85063TP
from machine import I2C # Pilote du bus I2C
from time import sleep # Pour temporiser

# On utilise l'I2C n°1 de la carte NUCLEO-WB55 pour communiquer avec le capteur
i2c = I2C(1) 

# Pause d'une seconde pour laisser à l'I2C le temps de s'initialiser
sleep(1)

# On crée une instance de la RTC
rtc = RTC_HP(i2c)

# On fixe la date au 8 août 2021
rtc.fillByYMD(2021,8,10)

# On fixe l'heure à 8h 15 minutes et 22 secondes
rtc.fillByHMS(8,15,22)

# On fixe le jour de la semaine à "MARDI"
rtc.fillDayOfWeek('MAR')

# On démarre l'horlode du module RTC
rtc.startClock()

# On affiche pendant une minute, toutes les secondes, l'heure et la date
for i in range(60):
	print(rtc.readTime())
	sleep(1)

# On arrête l'horloge du module RTC
#rtc.stopClock()
