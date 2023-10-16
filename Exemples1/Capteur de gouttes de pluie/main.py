# Attention : le capteur doit être alimenté en 5V pour donner une réponse entre 0 et 4095.

from pyb import ADC, Pin # Convertisseur analogique-numérique et GPIO
from time import sleep # Pour les temporisations

# Instanciation et démarrage du convertisseur analogique-numérique
adc = ADC(Pin('A0'))

while True:

	# Numérise la valeur lue, produit un résultat variable dans le temps dans l'intervalle [0 ; 4095]
	measure = adc.read()

	# Si une goutte tombe sur le capteur alors on averti l'utilisateur. 
	# Pour changer le niveau de detection il faut changer la valeur de la condition if
	if(measure < 3500):
		print("Alerte : détection de pluie")

	# Temporisation d'une seconde
	sleep(1) 