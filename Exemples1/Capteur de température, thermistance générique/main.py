# Objet du script : mesurer et afficher une température en utilisant une thermistance avec MicroPython.
# Matériel requis en supplément de la NUCLEO-WB55 : une thermistance et une résistance.

from pyb import ADC, Pin # Gestion du convertisseur analogique-numérique et des broches d'entrées-sorties
from time import sleep, time # Pour mesurer le temps écoulé et temporiser
from math import log # Pour calculer des logarithmes

# Tension de référence / étendue de mesure de l'ADC : +3.3V
varef = 3.3

# Résolution de l'ADC 12 bits = 2^12 = 4096 (mini = 0, maxi = 4095)
RESOLUTION = const(4096)
echADC = RESOLUTION - 1

# Quantum de l'ADC
quantum = varef / echADC

# Caractéristiques de la thermistance utilisée
R = 10 # Résistance à 25°C : 10 kOhms
B = 3950.0 # Indice thermique
T1 = 25 # Température absolue en K

# Broche A1 en entrée analogique
adc_A1 = ADC(Pin('A1'))

oldtempC = 0.0
temps_s = time()

while True:
	
	# Lecture de la broche A1
	value = adc_A1.read()
	
	# Calcul de la tension
	voltage = value * quantum
	
	# Calcul de la valeur de résistance de la thermistance
	Rt = R * voltage / (Vref - voltage)
	
	#Calcul des températures en Kelvins et degrés Celsius
	tempK = 1/(1/(273.15 + T1) + log(Rt/R)/B)
	tempC = tempK - 273.15

	# Affichage du résultat (si valeur dépassée à 0,2 près)
	if tempC < (oldtempC-0.2) or tempC > (oldtempC+0.2):
		oldtempC = tempC
		print("-"*21, "Temps :", time() - temps_s , "s", "-"*21)
		print("Température : %.2f°C\t\tTempérature : %.2f°K" %(tempC, tempK))
		
	# Temps de pause
	sleep(1)

