# Objet du script :
# Pilotage d'un module Grove anneau de LED RGB avec un module Grove potentiomètre
# Lorsqu'on tourne le potentiomètre, les LED s'allument progressivement.

import neopixel # Pilote pour l'anneau de LED RGB
from machine import Pin
from time import sleep_ms # Pour temporiser

# Potentiomètre sur A0
a0 = pyb.ADC('A0')

_NB_LED = const(24) # 24 LED sur l'anneau

# On initialise l'anneau de LED sur la broche D2
ring = neopixel.NeoPixel(Pin('D2'), _NB_LED)

# Fonction pour allumer les LED de l'anneau jusqu'à une LED donnée
# d'indice max_led.
#@micropython.native # Décorateur pour que le code soit optimisé pour STM32
def light_ring(max_led):

	# De 0 à _NB_LED - 1
	for i in range(_NB_LED):
		
		if i <= max_led: # Pour toutes les LED d'indice inférieur à max_led
			ring[i] = (10, 10, 10) # Les allumer en blanc avec une faible intensité
		else: Pour les autres LED
			ring[i] = (0, 0, 0) # Les éteindre 

	# Evnoyer les instruction à l'anneau
	ring.write()

# Fonction pour remapper un intervalle de valeurs dans un autre
#@micropython.native 
def map (value, from_min, from_max, to_min, to_max):
  return (value-from_min) * (to_max-to_min) / (from_max-from_min) + to_min


while True:
	
	# Convertit la lecture analogique du potentiomètre en un indice entre 0 et 23
	max_led = int(map(a0.read(), 0, 4045, 0, _NB_LED-1))
	
	# Allume les LED jusqu'à l'indice déterminé ci-avant
	light_ring(max_led)
	
	# Temporise 20 millisecondes
	sleep_ms(20)