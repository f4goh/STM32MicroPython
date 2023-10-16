# Objet du script :
# Mesure de température toutes les secondes avec un module capteur de température Grove I2C MCP9808
# Allume ou éteint les LED de la carte selon les valeurs des températures, les affiche sur le port série
# Source : https://github.com/mchobby/esp8266-upy/blob/master/mcp9808/examples/

from machine import I2C # Pilote du contrôleur I2C
from mcp9808 import MCP9808 # Pilote du MCP9808
import pyb # Pour gérer les GPIO
from time import sleep_ms # Pour temporiser

# On utilise l'I2C n°1 de la carte NUCLEO-WB55 pour communiquer avec le capteur
i2c = I2C(1) 

# Pause d'une seconde pour laisser à l'I2C le temps de s'initialiser
sleep_ms(1000)

# Liste des adresses I2C des périphériques présents
print("Adresses I2C utilisées : " + str(i2c.scan()))

# Instanciation du MCP9808
sensor = MCP9808(i2c)

# Instanciation des LED
blue_led = pyb.LED(1)
green_led = pyb.LED(2)
red_led = pyb.LED(3)

while True:

	# Lecture de la température
	temp = sensor.get_temp

	# Gestion des LED et des attributs
	if temp > 25:
		red_led.on()
		attribute = "Chaud !"
	elif temp > 18 and temp <= 25:
		green_led.on()
		attribute = "Confortable"
	else:
		blue_led.on()
		attribute = "Froid !"

	red_led.off()
	green_led.off()
	blue_led.off()

	print("Température : %.1f °C (%s)" %(temp,attribute))

	# Temporisation de 5 secondes
	sleep_ms(5000)
