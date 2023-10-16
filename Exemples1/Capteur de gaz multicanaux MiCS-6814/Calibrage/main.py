# Objet du script : Calibrage du module Grove capteur de gaz basé sur le MEMS MiCS-6814
# Exécutez ce script dans un environnement aéré et non pollué.
# Ce programme réalise deux opérations :
# 1 - Il calibre les ADC des trois canaux de capture du MiCS-6814 pour le caclul des concentrations des différents gaz
# 2 - Il évalue le signal maximum du capteur concernant les différents gaz pour les déduire par la suites des mesures (offsets)

from array import array # Pour utiliser des tableaux
from machine import I2C # Pilote du bus I2C
from time import sleep_ms # Pour temporiser
from mics6814 import MICS6814 # Pilote du MICS6814

PRE_HEAT_ROUNDS = const(60) # Nombre d'itérations de chauffage
PRE_HEAT_TIME_TEMPO = const(60000) # Durée d'une itération de chauffage (en millisecondes)

#Initialisation du bus I2C numéro 1 du STM32WB55 
i2c = I2C(1)

# Pause d'une seconde pour laisser à l'I2C le temps de s'initialiser
sleep_ms(1000)

# Instanciation du capteur
sensor = MICS6814(i2c)

print("\nPréchauffage du capteur avant calibration : %d minutes" %((PRE_HEAT_ROUNDS * PRE_HEAT_TIME_TEMPO) // 60000))

# On démarre les résistances chauffantes des capteurs 
sensor.heater_on()

p = 0
for i in range(PRE_HEAT_ROUNDS):
	sleep_ms(PRE_HEAT_TIME_TEMPO)
	p += 1
	# On affiche l'avancement toutes les cinq minutes
	if p == 5: 
		print(" Avancement : %d minutes" %(i+1))
		p = 0

# Temporisation de 5 secondes
sleep_ms(5000)

print("\nCalibration démarrée")
sensor.do_calibrate()
print("\nCalibration terminée")

# On éteint les résistances chaufffantes des capteurs
sensor.heater_off()

# Affichage des aleurs mémorisées en EEPROM
sensor.display_eeprom()

# Mesures ambiantes / offsets pour les concentrations mesurées
sensor.flush_raw()