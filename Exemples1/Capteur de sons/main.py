# Objet du script : 
# Mise en œuvre du module capteur de son Grove
# Attention, ce module fonctionne en 5V!

from time import sleep_ms	# Pour temporiser
from pyb import Pin, ADC	# Gestion des broches et du coonvertisseur 
							# analogique-numérique (ADC)

adc = ADC(Pin('A1')) # On "connecte" l'ADC à la broche A1

# Première étape : calibrage
# On mesure le voulume sonore ambiant pendant quelques temps pour être en mesure
# de discriminer par la suite les bruits anormaux
# Il s'agit de compenser l'offset naturel du capteur.

ambiant_noise_level = 0

print("Démarrage du calibrage")
print("Ne faites pas de bruit !")
sleep_ms(2000)

for x in range(1500):

	# Délai de 50 millisecondes pour laisser au capteur le temps de se stabiliser
	sleep_ms(50)
	
	# Lecture du bruit ambiant
	noise = adc.read()
	
	# Si la valeur du bruit est la plus grande détectée jusqu'ici
	# mémorise là
	if noise > ambiant_noise_level:
		ambiant_noise_level  = noise

# Auhmente de 50 le seuil de son ambiant
ambiant_noise_level += 50
		
print("Fin du calibrage")
print("Bruit ambiant : %d" %ambiant_noise_level)
sleep_ms(5000)

print("Micro à l'écoute ...")

while True : # Boucle sans clause de sortie

	sleep_ms(50)
	
	noise = adc.read()
	
	# Si le bruit détecté est plus fort que le seuil de bruit ambiant
	# calculé pendant le calibrage ...
	if noise > ambiant_noise_level:
		# Affiche une alerte
		print("Bruit atypique !")
		print("Valeur de l'ADC (prop. volume sonore) : %d" %noise)
		sleep_ms(1000)