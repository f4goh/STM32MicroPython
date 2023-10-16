# Objet du code : 
# Réception d'un message codé en MORSE avec une LED infrarouge (IR)
# Etape 1 : Réception en "polling", capture du signal analogique de la LED IR
# Lecture et numérisation du signal  avec un capteur Grove de luminosité (LS06-S phototransistor)
# Le commutateur du Grove Base Shield est placé sur 3.3V

from pyb import ADC, Pin # Convertisseur analogique-numérique et GPIO
from time import sleep_ms # Pour les temporisations

# Quantum de temps pour le code Morse ; durée minimum (en millisecondes) qui sépare
# deux symboles. 
TICK = const(1000) # Une seconde

# Instanciation et démarrage du convertisseur analogique-numérique sur la broche A0
adc = ADC(Pin('A0'))

# Affichage d'un en-tête dans le terminal série
print("\n" + "-" * 32)
print("Récepteur de code Morse")
print("-" * 32 + "\n")

while True:
	# Numérise la valeur lue sur la photodiode 
	measure = adc.read()
	print("Luminosité %d" %measure)
	sleep_ms(TICK) # Temporisation d'une demi-seconde