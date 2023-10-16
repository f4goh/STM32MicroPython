# Objet du script :
# Exemple de configuration d'un ADC pour numériser une tension d'entrée variable grâce à un potentiomètre.
# Pour augmenter la précision, on calcule la moyenne de la tension d'entrée sur 10 mesures 
# (une mesure toutes les 5 millisecondes).
# Matériel requis : potentiomètre (Grove ou autre) connecté sur A0 avec une alimentation du Grove base shield
# positionnée sur 3.3V

import pyb # pour gérer les GPIO
from time import sleep_ms # Pour temporiser

print( "L'ADC avec MicroPython c'est facile" )

# Tension de référence / étendue de mesure de l'ADC : +3.3V
VAREF = 3.3

# Résolution de l'ADC 12 bits = 2^12 = 4096 (mini = 0, maxi = 4095)
RESOLUTION = const(4096)

# Quantum de l'ADC
quantum = VAREF / (RESOLUTION - 1)

# Initialisation de l'ADC sur la broche A0
adc_A0 = pyb.ADC(pyb.Pin( 'A0' ))

# Initialisations pour calcul de la moyenne
nb_val = 100
inv_nb_val = 1 / nb_val

while True: # Boucle "infinie" (sans clause sortie)
	
	sum_voltage = 0
	average_voltage = 0
	
	# Calcul de la moyenne de la tension aux bornes du potentiomètre

	for i in range(nb_val): # On fait Nb_Mesures conversions de la tension d'entrée
		
		# Lit la conversion de l'ADC (un nombre entre 0 et 4095 proportionnel à la tension d'entrée)
		value_sampled = adc_A0.read()
		
		# On calcule à présent la tension (valeur analogique) 
		voltage = value_sampled * quantum

		# On l'ajoute à la valeur calculée à l'itération précédente
		sum_voltage += voltage

		# Temporisation pendant 5 ms
		sleep_ms(5)
	
	# On divise par Nb_Mesures pour calculer la moyenne de la tension du potentiomètre
	average_voltage = sum_voltage * inv_nb_val 
	
	# Affichage de la tension moyenne sur le port série de l'USB USER
	print( "La valeur moyenne de la tension est : %.2f V" %average_voltage)