# Objet du script : Mise en œuvre de l'accéléromètre 3 axes MMA7660FC (+/- 1.5g)
# Datasheet : https://www.nxp.com/docs/en/data-sheet/MMA7660FC.pdf
# Cet exemple est adapté de :
# https://github.com/ControlEverythingCommunity/MMA7660FC/blob/master/Python/MMA7660FC.py

from machine import I2C # Pour gérer le bus I2C
from time import sleep_ms # Pour gérer les temporisations

# On utilise l'I2C n°1 de la carte NUCLEO-WB55 pour communiquer avec le capteur
i2c = I2C(1) 

# Pause d'une seconde pour laisser à l'I2C le temps de s'initialiser
sleep_ms(1000)

# Liste des adresses I2C des périphériques présents
print("Adresses I2C utilisées : " + str(i2c.scan()))

# Adresse du capteur sur le bus I2C : 0x4C (76) 
MMA7660FC_ADR = const(76)

# Adresse du registre de sélection du mode : 0x07 (7)
MMA7660FC_SMR = const(7)

# Mode "standby" : 0x00 (0)
MMA7660FC_STANDBY = b'\x00'

# Mode "Actif" : 0x01 (1)
MMA7660FC_ACTIVE = b'\x01'

# Adresse du registre permettant de fixer la fréquence d'échantillonnage : 0x08(8)
MMA7660FC_SRR = const(8)

# Adresse du registre de sortie exposant les 3 octets contenant les accélérations : 0x00(0)
MMA7660FC_ODR = const(0)

# La fréquence d'échantillonnage sera deux mesures par seconde : 0x06(6)
# On peut changer cette valeur pour des mesures plus fréquentes, jusqu'à 120 par seconde
# (voir https://www.nxp.com/docs/en/data-sheet/MMA7660FC.pdf)

MMA7660FC_SRATE1 = b'\x07'
MMA7660FC_SRATE2 = b'\x06'
MMA7660FC_SRATE4 = b'\x05'
MMA7660FC_SRATE8 = b'\x04'
MMA7660FC_SRATE16 = b'\x03'
MMA7660FC_SRATE32 = b'\x02'
MMA7660FC_SRATE64 = b'\x01'
MMA7660FC_SRATE120 = b'\x00'

# Passe en mode "standby"
# - écrit dans la mémoire du périphérique I2C situé à l'adresse MMA7660FC_ADR
# - écrit à partir de l'adresse MMA7660FC_SMR
# - écrit les octets contenus dans MMA7660FC_STANDBY, qui doivent être placés dans un tableau
i2c.writeto_mem(MMA7660FC_ADR, MMA7660FC_SMR, MMA7660FC_STANDBY)

# Programme la fréquence d'échantillonnage (seize mesures par seconde)
i2c.writeto_mem(MMA7660FC_ADR, MMA7660FC_SRR, MMA7660FC_SRATE16)

# Passe en mode "actif" 
i2c.writeto_mem(MMA7660FC_ADR, MMA7660FC_SMR, MMA7660FC_ACTIVE)

# Pause de 500 millisecondes pour s'assurer que l'écriture est bien terminée
sleep_ms(500)

# Facteur de conversion entre les valeurs lues dans les registres et l'accélération physique
# exprimée en g.
RAW_TO_G = 0.047

while True: # Boucle sans clause de sortie

	# Lecture du vecteur d'accélération : trois octets à partir de l'adresse du registre de sortie 
	# MMA7660FC_ODR
	data = i2c.readfrom_mem(MMA7660FC_ADR, MMA7660FC_ODR, 3)

	sleep_ms(500)

	# Les valeurs de l'accélération sont codées sur les six premiers bits (de droite à gauche) de 
	# chaque octet.
	# On doit donc appliquer un masque binaire sur les octets lus, avec l'opération logique "&" afin 
	# de mettre à zéro les deux bits les plus à gauche.
	# Le masque qui convient est donc  00111111 (en binaire) = 0x3F (en hexadécimal).

	xAccl = data[0] & 0x3F

	# On recentre le résultat non signé codé sur 6 bits de l'intervalle [0, 64] dans l'intervalle
	# [-32, 31] afin de restituer le signe de l'accélération suivant chaque axe (complément à deux).
	
	if xAccl > 31 :
		xAccl -= 64

	yAccl = data[1] & 0x3F
	if yAccl > 31 :
		yAccl -= 64

	zAccl = data[2] & 0x3F
	if zAccl > 31 :
		zAccl -= 64

	# Affichage des accélérations en g, en appliquant le facteur de conversion RAW_TO_G
	# Les données sont affichées comme des nombres décimaux avec 1 chiffre après la virgule (%.1f)

	print("Acceleration axe X : %.1f g" %(xAccl * RAW_TO_G))
	print("Acceleration axe Y : %.1f g" %(yAccl * RAW_TO_G))
	print("Acceleration axe Z : %.1f g" %(zAccl * RAW_TO_G))

	# Temporisation d'un quart de seconde
	sleep_ms(250)