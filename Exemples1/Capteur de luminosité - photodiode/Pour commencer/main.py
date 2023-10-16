# Lecture et numérisation du signal d'un capteur Grove de luminosité (LS06-S phototransistor)
# Attention : le capteur doit être alimenté en 5V pour donner une réponse entre 0 et 4095.

from pyb import ADC, Pin # Convertisseur analogique-numérique et GPIO
from time import sleep # Pour les temporisations

# Instanciation et démarrage du convertisseur analogique-numérique
adc = ADC(Pin('A1'))

while True:
	# Numérise la valeur lue, produit un résultat variable dans le temps 
	# dans l'intervalle [0 ; 4095]
	sampled = adc.read()
	print("Luminosité %d (sans unités)" %sampled)
	sleep(1) # Temporisation d'une seconde