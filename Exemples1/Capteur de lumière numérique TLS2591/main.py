# Objet du script :
# Mise en œuvre du module Adafruit I2C Capteur de lumière numérique (TLS2591)
# Source : https://github.com/mchobby/esp8266-upy/tree/master/tsl2591

from tsl2591 import * # Pilote du module
from machine import I2C # Pilote du bus I2C
from time import sleep # pour temporiser

# On utilise l'I2C n°1 de la carte NUCLEO-WB55 pour communiquer avec le capteur
i2c = I2C(1) 

# Pause d'une seconde pour laisser à l'I2C le temps de s'initialiser
sleep(1)

# Instanciation du capteur
tsl = TSL2591( i2c )

# Attention: manipuler le gain et le temps d'intégration de façon
# inappropriée peut conduire à des résultats totalement erronés.

# GAIN_LOW (1x gain)
# GAIN_MED (25x gain, default)
# GAIN_HIGH (428x gain)
# GAIN_MAX (9876x gain)
# tsl.gain = GAIN_LOW # x25

# INTEGRATIONTIME_100MS (100ms, default)
# INTEGRATIONTIME_200MS
# INTEGRATIONTIME_300MS
# INTEGRATIONTIME_400MS
# INTEGRATIONTIME_500MS
# INTEGRATIONTIME_600MS
# tsl.integration_time = INTEGRATIONTIME_400MS

while True:

	# Lecture d'une valeur

	print( "Eclairement : %.1f lx" % tsl.lux )

	# Valeur entière proportionelle à l'éclairement infrarouge
	ir = tsl.infrared

	# Valeur entière proportionelle à l'éclairement visible
	vi = tsl.visible
	
	# Somme des deux ...
	total = ir + vi
	
	if total !=0:
		inv_total = 100 / total

		print("Infrarouge : %.1f %%" %(ir*inv_total))
		print("Lumière visible : %1.f %%" %(vi*inv_total))

	print("")

	# Temporisation de 5 secondes
	sleep(5)