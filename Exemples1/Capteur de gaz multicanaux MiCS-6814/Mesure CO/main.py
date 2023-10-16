# Objet du script :
# Mesure de la concentrations de monoxyde de carbone à l'aide du module Grove basé sur le capteur MEMS MiCS-6814.
# Fiche technique : https://www.sgxsensortech.com/content/uploads/2015/02/1143_Datasheet-MiCS-6814-rev-8.pdf

from machine import I2C # Pilote du bus I2C
from time import sleep # Pour temporiser

#Initialisation du bus I2C numéro 1 du STM32WB55 
i2c = I2C(1)

# Pause d'une seconde pour laisser à l'I2C le temps de s'initialiser
sleep(1)

from mics6814 import MICS6814

sensor = MICS6814(i2c)

# Seuils de détection pour le monoxyde de carbone en ppm
CO_LT = 1 # seuil bas, d'après la  fiche technique du MICS6814
CO_HT = 50 # seuil haut, seuil de risque sanitaire

# Offset (ambiant) fourni par le script de calibrage
Offset_CO = 4.0

# On démarre les résistances chaufffantes du capteur 
sensor.heater_on()
cnt_detected = 0

# On fait une série de mesures "à blanc" pour préchauffer le capteur

PREHEAT_ROUNDS = const(20)

print("Préchauffage pendant %d minutes" %(PREHEAT_ROUNDS * 10 // 60) )
for i in range(PREHEAT_ROUNDS):
	co = sensor.get_co()
	sleep(10)
print("Préchauffage terminé\n")

while True: # boucle ...

	# Pourt le moment, pas de mesure faite, donc potentiellement pas de CO détecté
	co_detected = False

	# Estime la concentration en CO, en déduisant l'offset ambiant
	co = sensor.get_co() - Offset_CO
	
	# Si le résultat est positif, vérifie qu'il est bien au-dessus du seuil de détection bas du capteur
	if co > CO_LT:
		co_detected = True
		cnt_detected += 1
		if co < CO_HT:
			print("%1d - Concentration CO : %.1f ppm" %(cnt_detected, co))
		else:
			# Si on dépasse le seuil d'alerte, signale le
			print("%1d - Alerte CO : %.1f > %.1f ppm : " %(cnt_detected, co, CO_HT))
	elif co < 0:
			# Si la concentration mesurée est négative, signale une erreur du capteur
			print("%1d - Monoxyde de carbone (CO) : Erreur de mesure !")
			# Quitte la boucle
			break

	if co_detected:
		print('')
		# Si du CO a été détecté, allume la LED du module pendant 10 secondes
		sensor.led_on()
		sleep(10)
		sensor.led_off()

