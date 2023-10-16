# Objet du script : Mettre en œuvre un module suiveur de ligne
# Source : https://github.com/DexterInd/GrovePi/blob/master/Software/Python/grove_line_finder.py

from time import sleep_ms # Pour temporiser
from machine import Pin # Gestion de la broche du suiveur de ligne 

line_finder = Pin('D7', Pin.IN) # Broche du détecteur de ligne

while True:
	# Renvoie 1 lorsque la ligne noire est détectée, 0 si du blanc se trouve sous les diodes
	if line_finder.value(): # Equivalent à  line_finder.value() != 0:, on supprime un test
		print ("Ligne noire détectée !")
	else:
		print ("Surface blanche détectée")

	sleep_ms(100) # On temporise un dixième de seconde
