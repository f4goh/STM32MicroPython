# Objet du script :
# Mise en œuvre d'un afficheur à matrices de LED 8x8 Max7219 sur bus SPI
# Texte défilant

import max7219 # Pilotes de l'afficheur
from machine import Pin, SPI # Pilotes des entrées-sorties et du bus SPI
from time import sleep_ms # Pour temporiser

# Nome de colonnes de LED sur l'afficheur
NB_COL = const(32)

# Nombre de lignes de LED sur l'afficheur
NB_ROW = const(8)

# Initialisation du bus SPI1
spi = SPI(1)
sleep_ms(1000)

# Instanciation de l'afficheur
display = max7219.Max7219(NB_COL, NB_ROW, spi, Pin('D9'))

inverted = False

def display_text_scroll(text, inv):
	# pour 4 blocs de LED

	# Calcul du décalage vers la gauche : len(text) * -8 - 1
	for p in range(NB_COL, len(text) * -8 - 1, -1):
		# Eteint toutes les LED
		display.fill(inv)
		# Affiche text décalé de p colonnes
		display.text(text, p, 0, not inv)
		display.show()
		# Temporisation de 50 millisecondes entre deux décalages
		sleep_ms(50)

# Programme principal

# Gestion d'erreurs pour ne pas laisser la matrice de LED écalirée
# en cas d'interruption du programme par CTRL+C
try :
	while True:
		display_text_scroll("STMicroelectronics", inverted)
		
# En cas d'interruption clavier avec CTRL+C
# Eteint la matrice
except KeyboardInterrupt:
		display.fill(0)
		display.show()
