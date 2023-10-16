# Objet du script :
# Mise en œuvre du module Grove LCD 16x2 I2C
# Bibliothèques pour le LCD copiées et adaptées depuis ce site : 
# https://GitHub.com/Bucknalla/MicroPython-i2c-lcd

from time import sleep # pour temporiser
from machine import I2C # Pilote du bus I2C
from i2c_lcd import lcd # Pilote du module LCD 16x2

# On utilise l'I2C n°1 de la carte NUCLEO-WB55 pour communiquer avec le capteur
i2c = I2C(1) 
# Pause d'une seconde pour laisser à l'I2C le temps de s'initialiser
sleep(1)

# Liste des adresses I2C des périphériques présents
print("Adresses I2C utilisées : " + str(i2c.scan()))

# Instanciation de l'afficheur
display = lcd(i2c)

while True:

	# Positionne le curseur en colonne 1, ligne 1
	col = 1
	row = 1
	display.setCursor(col - 1, row - 1)

	# Affiche "Hello World"
	display.write('Hello World')

	# Positionne le curseur en colonne 1, ligne 2
	col = 1
	row = 2
	display.setCursor(col - 1, row - 1)

	# Affiche "Bonjour Monde"
	display.write('Bonjour Monde')

	# Attends cinq secondes
	sleep(5)

	# Efface l'afficheur
	display.clear()

	# Attends cinq secondes
	sleep(5)