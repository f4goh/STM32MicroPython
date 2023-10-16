# Exemple adapté de https://github.com/neliogodoi/MicroPython-SI1145
# Objet du script : Mise en œuvre du module grove I2C capteur de lumière solaire,
# basé sur le capteur SI1145 pour mesurer l'indice UV.

from time import sleep_ms # Pour gérer les temporisations
from machine import I2C # Pour gérer l'I2C
import si1145 # Pour gérer le capteur 

# On utilise l'I2C n°1 de la carte NUCLEO-WB55 pour communiquer avec le capteur
i2c1 = I2C(1)

# Pause d'une seconde pour laisser à l'I2C le temps de s'initialiser
sleep_ms(1000)

# Liste des adresses I2C des périphériques présents
print("Adresses I2C utilisées : " + str(i2c1.scan()))

# Instanciation du capteur
sensor = si1145.SI1145(i2c=i2c1)

while True :
	# Indice UV
	uv_index = sensor.read_uv
	
	# Valeur caractéristique de l'intensité du rayonnement infrarouge
	ir_analog = sensor.read_ir
	
	# Valeur caractéristique de l'intensité du rayonnement visible
	visible_analog = sensor.read_visible
	
	# Affichage
	print(" Indice UV: %d\n IR: %d (AU)\n Visible: %d (AU)\n" % (uv_index, ir_analog, visible_analog))
	
	# Temporisation de 5 secondes
	sleep_ms(5000)