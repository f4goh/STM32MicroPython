# Objet du script :
# Pilotage d'un module Grove barre de LED MY9221 avec un module Grove potentiomètre linéaire
# Lorsqu'on fait glisser la commande du potentiomètre, les LED s'allument (puo s'éteignent) progressivement.
# NB : Cet exemple fonctionnerait aussi parfaitement avec un potentiomètre rotatif

from my9221 import MY9221 # Pour piloter la barre de LED
from machine import Pin
from time import sleep_ms # Pour temporiser

# Potentiomètre sur A0
a0 = pyb.ADC('A0')

# Instanciation de la barre de LED
# Attention de bien modifier les références des broches si vous le connectez
# ailleurs sur le Grove Base Shield !
ledbar = MY9221(Pin('D4'), Pin('D5'))

# Nombre de LED sur la barre
_NB_LED = const(10)

# Fonction pour allumer les LED de la barre jusqu'à une LED donnée
# d'indice max_led.
#@micropython.native # Décorateur pour que le code soit optimisé pour STM32
def light_bar(max_led):

	# Construction du masque binaire pour allumer les LED
	
	mask = 0b0000000000
	
	# Pour toutes les LED (de 0 à _NB_LED-1)
	for i in range(_NB_LED):
		# Pour chaque bit jusqu'à celui de la dernière LED à éclairer
		if i < max_led+1:
			# Met à 1 le bit en question dans le masque
			mask = mask | (1<<i)
	
	# Applique le masque, allume les LED correspondantes
	ledbar.bits(mask)

# Fonction pour remapper un intervalle de valeurs dans un autre
#@micropython.native 
def map (value, from_min, from_max, to_min, to_max):
	return (value-from_min) * (to_max-to_min) / (from_max-from_min) + to_min

# Gestion d'erreurs pour ne pas laisser la barre de LED écalirée
# en cas d'interruption du programme par CTRL+C
try:

	while True:
	
		# Convertit la lecture analogique du potentiomètre en un indice entre 0 et 23
		max_led = int(map(a0.read(), 0, 4045, 0, _NB_LED-1))
	
		# Allume les LED jusqu'à l'indice déterminé ci-avant
		light_bar(max_led)
	
		# Temporise 20 millisecondes
		sleep_ms(20)
		
# En cas d'interruption clavier avec CTRL+C
# Eteint la barre
except KeyboardInterrupt:
	ledbar.bits(0b0000000000)