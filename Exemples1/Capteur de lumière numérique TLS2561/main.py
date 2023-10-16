# Objet du script :
# Mise en œuvre du module Grove I2C Capteur de lumière numérique (TLS2561)
# Sources : https://github.com/mchobby/esp8266-upy/tree/master/tsl2561

from tsl2561 import * # Pilote du module
from machine import I2C # Pilote du bus I2C
from time import sleep # pour temporiser

# On utilise l'I2C n°1 de la carte NUCLEO-WB55 pour communiquer avec le capteur
i2c = I2C(1) 

# Pause d'une seconde pour laisser à l'I2C le temps de s'initialiser
sleep(1)

# Instanciation du capteur
tsl = TSL2561( i2c )

while True:
	# Lecture d'une valeur
	
	#   Cela activera automatiquement le senseur (ce qui prend du temps)
	#   puis effectue la lecture ensuite désactive le senseur.
	#   Retourne une valeur en lux (ex: 6.815804 Lux)
	#print( tsl.read() )

	# Note: vous pouvez activer/désactiver manuellement le senseur avec
	# active(True/False).

	# Vous pouvez changer manuellement le gain et temps d'intégration
	# * Le gain peut être 1 ou 16
	# * Le temps d'intégration : 0 ou 13 ou 101 ou 402 (0=manuel)
	#tsl.gain( 16 )
	#tsl.integration_time( 402 )
	#print( tsl.read() )

	# Vous pouvez également utiliser une sélection automatique du gain (AutoGain)
	# (uniquement si vous n'utilisez pas d'intégration manuelle)
	tsl.integration_time( 402 )
	print( "Eclairement : %.1f lx" % tsl.read(autogain=True))

	# Temporisation d'une seconde
	sleep(1)