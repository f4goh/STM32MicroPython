# Test de la fonction TAP
# Création d'un podomètre sur la base d'un  exemple fourni par Frédéric Boulanger
# CentraleSupélec - Département Informatique


from machine import I2C # Pour gérer le bus I2C
from time import sleep_ms # Pour gérer les temporisations

# On utilise l'I2C n°1 de la carte NUCLEO-WB55 pour communiquer avec le capteur
MMA_I2C = I2C(1) 

# Pause d'une seconde pour laisser à l'I2C le temps de s'initialiser
sleep_ms(1000)

# Liste des adresses I2C des périphériques présents
print("Adresses I2C utilisées : " + str(MMA_I2C.scan()))

MMA_address =  const(0x4C) 
 
# Adresse du registre de détection de conditions particulières
_TILT_REG = const(3)

# Adresse du registre de paramétrage des interruptions de l'accéléromètre
_INTSU_REG = const(6)

# Adresse du registre de sélection du mode
_SM_REG = const(7)

# Adresse du registre permettant de fixer la fréquence d'échantillonnage
_SR_REG = const(8)

# Adresse du registre des paramètres des taps
_PDET_REG = const(9)

# Adresse du registre de filtrage de la détection des taps
_PD_REG = const(10)
 
# Met l'accéléromètre en mode on
def MMA_on():
	MMA_I2C.writeto_mem(MMA_address, _SM_REG, b'\x01')
 
# Met l'accéléromètre en mode standby
def MMA_off():
	MMA_I2C.writeto_mem(MMA_address, _SM_REG, b'\x00')
 
# Mini podomètre

# Configuration 
MMA_off() # Désactivation de l'accéléromètre

MMA_I2C.writeto_mem(MMA_address, _INTSU_REG, b'\xFF') # activer toutes les interruptions pour les taps
MMA_I2C.writeto_mem(MMA_address, _SR_REG, b'\x00') # configurer l'échantillonnage pour la détection des taps

# Détection des taps sur les 3 axes (bits [7-5] à 0)
# Anti-rebond  : on filtre quatre oscillations, soit 0x04 (valeur possible de 1 à 31)
MMA_I2C.writeto_mem(MMA_address, _PDET_REG, b'\x04') 

MMA_I2C.writeto_mem(MMA_address, _PD_REG, b'\x03') # délai de détection des taps, agrège 3 taps adjacents

MMA_on() # Activation de l'accéléromètre

tap_count = 0 # compteur de taps

while True:
	
	# lecture du registre TILT
	tilt = MMA_I2C.readfrom_mem(MMA_address, _TILT_REG, 1)
	val = tilt[0]

	if val & (1<<5):
		print("TAP")
		tap_count += 1
		print("Nb de taps : %d" %tap_count)


