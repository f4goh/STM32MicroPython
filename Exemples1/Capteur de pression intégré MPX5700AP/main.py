# Lecture et numérisation du signal d'un capteur Grove de pression intégré

from pyb import Pin, ADC # Gestion de la broche analogique et de l'ADC
import time # Gestion du temps et des temporisations

# Pression de référence (atmosphérique) : 956 hPa
pref_hpa = const(956)

# Somme de dix values analogiques pour 956 hPa
pref_analog = const(6883)

ratio = pref_hpa / pref_analog

# Instance du convertisseur analogique-numérique
adc = ADC(Pin('A0'))

while True:
	
	value = 0 # Valeur analogique
	counter = 0 

	# On effectue dix conversions analogiques-numériques de la pression
	while counter < 10:
		value = value + adc.read()
		counter = counter + 1

	# Conversion de la value analogique en pression
	pressure = value * ratio

	print("Valeur analogique = %d" %value)

	print("Pression = %d hPa" %pressure)

	# Pause pendant 1 s
	time.sleep(1)
