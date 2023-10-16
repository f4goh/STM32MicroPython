# Objet du script :
# Mise en œuvre d'un afficheur à matrices de LED 8x8 Max7219 sur bus SPI
# Texte statique

import max7219 # Pilote de l'afficheur
from machine import Pin, SPI # Pour piloter le bus SPI
from time import sleep # Pour temporiser

# Nome de colonnes de LED sur l'afficheur
NB_COL = const(32)

# Nombre de lignes de LED sur l'afficheur
NB_ROW = const(8)

# Paramètre d'affichage (voir plus bas)
RIGHT_SHIFT = const(0)
BOTTOM_SHIFT = const(1)
inverted = False

# La broche "Chip Select" du bus SPI sera "D9" 
CHIP_SELECT = 'D9'

# Initialisation du bus SPI 1
spi = SPI(1)
sleep(1)

# Instanciation du pilote de la matrice de LED
display = max7219.Max7219(NB_COL, NB_ROW, spi, Pin(CHIP_SELECT))

# La luminosité des LED sera 8 (valeur comprise entre 0 et 15)
display.brightness(8)

# Le fond du texte sera constitué de LED éteintes
display.fill(inverted)

# Le texte affiché sera "1234"
# Il sera décalé vers la droite de RIGHT_SHIFT colonnes de LED
# Il sera décalé vers le bas de BOTTOM_SHIFT lignes de LED
# Le texte sera constitué de LED allumées
display.text('1234', RIGHT_SHIFT, BOTTOM_SHIFT, not inverted)

# Gestion d'erreurs pour ne pas laisser la matrice de LED écalirée
# en cas d'interruption du programme par CTRL+C
try :
	# Affiche le texte
	display.show()
	while True:
		pass
		
# En cas d'interruption clavier avec CTRL+C
# Eteint la matrice
except KeyboardInterrupt:
	display.fill(0)
	display.show()