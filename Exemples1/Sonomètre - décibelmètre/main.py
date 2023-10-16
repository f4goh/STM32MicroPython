# Objet du script : 
# Mise en œuvre du module sonomètre analogique SEN0232 de DFROBOT
# Ce module est très sensible et capable de renvoyer une intensité sonore exprimée en décibels.

from time import sleep_ms	# Pour temporiser
from pyb import Pin, ADC	# Gestion des broches et du coonvertisseur 
							# analogique-numérique (ADC)

VREF = 3.3 # Tension de référence de l'ADC
CONV = VREF / 4096 # Facteur de conversion lecture ADC -> Tension
VOLTAGE_TO_DB = VREF * 50 / 4096 # Facteur de conversion lecture ADC -> décibels

adc = ADC(Pin('A1')) # On "connecte" l'ADC à la broche A1

# Première étape : calibrage
# On mesure le voulume sonore ambiant pendant quelques temps pour être en mesure
# de discriminer par la suite les bruits anormaux.

ambiant_noise_level = 0

print("Etape de calibrage")
print("Ne faites pas de bruit !")
sleep_ms(10000)
print("Démarrage du calibrage")

for x in range(500):

	# Délai de 125 millisecondes pour laisser au capteur le temps de se stabiliser
	sleep_ms(125)
	
	# Lecture du bruit ambiant en décibels
	noise = adc.read() * VOLTAGE_TO_DB
	
	# Si la valeur du bruit est la plus grande détectée jusqu'ici
	# mémorise là
	if noise > ambiant_noise_level:
		ambiant_noise_level  = noise
		
print("Fin du calibrage")
print("Volume sonore ambiant : %.1f dB" %ambiant_noise_level)
sleep_ms(5000)

print("Sonomètre à l'écoute ...")

while True : # Boucle sans clause de sortie

	sleep_ms(125)
	
	noise = adc.read() * VOLTAGE_TO_DB
	
	# Si le bruit détecté est plus fort que le seuil de bruit ambiant
	# calculé pendant le calibrage ...
	if noise > ambiant_noise_level:
		# Affiche une alerte
		print("Bruit atypique !")
		print("Intensité : %.1f dB" %noise)
		sleep_ms(1000)