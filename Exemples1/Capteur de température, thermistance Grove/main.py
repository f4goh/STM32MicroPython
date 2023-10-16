"""
Mesure de température à partir d'une thermistance d'un module Grove Temperature sensor V1.2 relié à l'entrée A0
L'ADC interne fonctionnant sur 3.3V, le capteur doit être alimenté en 3.3V sur la carte d'adaptation Grove.

Rappel: La valeur d'une thermistance CTN obéit à la relation R=R0 x exponentielle (B( 1/T -1/298))
avec B=4275°Kelvin R0=100KOhm et Ten °Kelvin= T en°C +273

La tension U du capteur est reliée à A0 = 3.3V x R1 /( R1+R) avec R1=100K=R0
En déduire U en fonction de R0 puis T en °C:

  U=3.3/1+exponentielle (B( 1/T -1/298))
  T= 1/((ln(3.3/U -1) /B)+1/298)

Voir https://wiki.seeedstudio.com/Grove-Temperature_Sensor_V1.2/#reference
Source : F HERGNIOT, Lycée Algoud-Laffemas, Valence
"""

from time import sleep_ms # Pour temporiser
from pyb import Pin, ADC # Pilotes des broches et de l'ADC
from math import log # Fonction logarithme (népérien)

adc_A0 = ADC('A0') # Initialisation de l'ADC sur l'entrée A0 
print("Mesure de temperature à partir d'une thermistance Groove sencor V1.2") 

# Règle de 3 pour déduire la tension aux bornes de la thermistance à partir de la 
# valeur convertie de l'ADC
ratio = 3.3/4096 

def get_temperature_CTN_v12():

	B = const(4275) # coeff B de la thermistance
	R0 = const(100000) # R0 = 100k x correctif précision avec vraie mesure

	N = adc_A0.read() # Conversion de 12 bits - 4096 valeurs de 0 à 3.3V
	U= N * ratio # On déduit la tension de la valeur convertie de l'ADC

	temp = 1.0/(log((3.3/U) -1)/B+1/298)-273 # Calcule la température à partir de la tension

	return temp


def demo():

	while True:
	
		temperature = get_temperature_CTN_v12()
		
		# Affiche la température sous forme de flottant xx,x
		print("La valeur de la temperature est : %.1f °C" %temperature)
		sleep_ms(1000)

if __name__ == '__main__':
	demo()