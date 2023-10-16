# Lecture et numérisation du signal d'un capteur de niveau d'eau (water sensor)
# Attention : le capteur doit être alimenté en 5V pour donner une réponse entre 0 et 4095.

from pyb import ADC, Pin 		# Convertisseur analogique-numérique et GPIO
from time import sleep 			# Pour les temporisations

# Instanciation et démarrage du convertisseur analogique-numérique
adc = ADC(Pin('A0'))

# Seuil pour la détection d'eau (sans unités)
THRESHOLD = const(800)

while True:

	# Numérise la valeur lue, produit un résultat variable dans le temps dans l'intervalle [0 ; 4095]
	measure = adc.read()
	
	# Si le signal dépasse un seuil donné
	if measure > THRESHOLD:
		print("Eau détectée : %d " %(measure))
	else:
		print("Sec : %d " %(measure))
	sleep(1) # Temporisation d'une seconde