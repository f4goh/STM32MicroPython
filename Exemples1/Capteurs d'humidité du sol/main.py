# Objet du script :
# Mise en œuvre des capteurs d'humidité du sol de type résistifs et capacitifs.
# Si vous utilisez un capteur résistif, choisir CAP = False. 
# Si vous utilisez un capteur capacitif, choisir CAP = True.
#
# Procédure de calibrage :
# 1. Mettre CALIB = False
# 2. Laisser le capteur dans l'air et remonter les valeurs brutes de l'ADC. 
#    Mémoriser le résultat : CAL_AIR = ...
# 3. Plonger le capteur aux 2/3 dans l'eau (sans mouiller ses composants
#    électroniques !) et remonter les valeurs brutes de l'ADC. 
#    Mémoriser le résultat : CAL_WATER = ... 
# 3. Mettre CALIB = True
# 4. Relancez les mesures pour obvserver des valeurs d'humlidité en pourcentage.

from time import sleep # Pour temporiser
from pyb import Pin, ADC # Pour gérer les broches et l'ADC 
import soil_moisture # pilote du capteur d'humidité du sol

# Est-ce qu'on a déjà calibré ?
CALIB = True

# Est-ce que le capteur est capacitif ?
# (si non, il est pris pour résistif)
CAP = True

NB_MES = 255 
INV_NB_MES = 1 / NB_MES

# Capteur sur A0 (analogique)
adc = ADC(Pin('A0'))

if CALIB: # Si on a déjà déterminé les constantes de calibration
	
	if CAP: # S'il s'agit d'un capteur capacitif
		
		# Retour de la mesure "raw" pour ...
		CAL_AIR = 2535 # Mon capteur capacitif plongé dans l'air
		CAL_WATER = 1535 # Mon capteur capacitif plongé dans l'eau
	
	else: # S'il s'agit d'un capteur résistif
		
		# Retour de la mesure "raw" pour ...
		CAL_AIR = 0 # Mon capteur résistif plongé dans l'air
		CAL_WATER = 2365 # Mon capteur résistif plongé dans l'eau

	# Instance de la classe du capteur avec les constantes de calibrage spécifiées
	sensor = soil_moisture.SOILMOIST(adc, sig_air = CAL_AIR, sig_water = CAL_WATER)

else: # Si on n'a pas encore calibré

	#instance de la classe du capteur
	sensor = soil_moisture.SOILMOIST(adc)

while True:

	if not CALIB: # Si on est en phase de calibrage

		# Renvoie les mesure "raw" pour pouvoir les constantes
		# obtenir les constantes CAL_AIR et CAL_WATER
		sum = 0
		for i in range(NB_MES):
			# Mesure brute (en quanta de l'ADC)
			sum = sum + sensor.raw()

		# Moyenne de NB_MES mesures
		avg = sum * INV_NB_MES
				
		print("Valeur brute de l'ADC : " %avg) 

	else: # Si on a déjà calibré le capteur

		print("Humidité %1d %%" %sensor.measure()) 
	
	sleep(10) # Temporisation de dix secondes