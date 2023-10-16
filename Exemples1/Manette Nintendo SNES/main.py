# Objet du script :
# Lire les messages de la manette Nintendo SNES avec Micropython

from pyb import Pin # Gestion des broches
from time import sleep_ms # Pour temporiser
import gc # Ramasse miettes, pour éviter de saturer la mémoire

# Constantes pour associer les boutons aux valeurs
BTN_A = 256
BTN_B = 1
BTN_X = 512
BTN_Y = 2
BTN_SELECT = 4
BTN_START = 8
BTN_UP = 16
BTN_DOWN = 32
BTN_LEFT = 64
BTN_RIGHT = 128
BTN_L = 1024
BTN_R = 2048

#Mise en entrée/sortie des ports
PIN_LATCH = Pin('D2', Pin.OUT)
PIN_CLOCK = Pin('D3', Pin.OUT)
PIN_DATA = Pin('D4', Pin.IN)

print("Manette SNES en MicroPython :")

# Fonction d'acquisition des données
@micropython.native
def getSnesButtons():
	value = 0
	PIN_LATCH.high()
	PIN_LATCH.low()
	# Lecture de la valeur des 16 bits de données
	for i in range(0, 16, 1):
		value |= PIN_DATA.value() << i
		PIN_CLOCK.high()
		PIN_CLOCK.low()
	# Retour de la valeur
	return ~value

# Fonction d'affichage des données
@micropython.native
def loop():
	oldBtns = -65536

	# Appel de la fonction d'acquisition
	btns = getSnesButtons()

	# Tant que les valeurs sont les mêmes on ne fait rien
	while(oldBtns == btns):
		btns = getSnesButtons()
	oldBtns = btns

	# Affichage en fonction des données récupérées
	if(btns & BTN_A):
		print("A ", end = '')
	else:
		print("- ", end = '')

	if(btns & BTN_B):
		print("B ", end = '')
	else:
		print("- ", end = '')

	if(btns & BTN_X):
		print("X ", end = '')
	else:
		print("- ", end = '')

	if(btns & BTN_Y):
		print("Y ", end = '')
	else:
		print("- ", end = '')

	if(btns & BTN_SELECT):
		print("SELECT ", end = '')
	else:
		print("------ ", end = '')

	if(btns & BTN_START):
		print("START ", end = '')
	else:
		print("----- ", end = '')

	if(btns & BTN_UP):
		print("UP ", end = '')
	else:
		print("-- ", end = '')

	if(btns & BTN_DOWN):
		print("DOWN ", end = '')
	else:
		print("---- ", end = '')

	if(btns & BTN_LEFT):
		print("LEFT ", end = '')
	else:
		print("---- ", end = '')

	if(btns & BTN_RIGHT):
		print("RIGHT ", end = '')
	else:
		print("----- ", end = '')

	if(btns & BTN_L):
		print("L ", end = '')
	else:
		print("- ", end = '')

	if(btns & BTN_R):
		print("R ")
	else:
		print("- ")

	# Appel du ramasse-miettes, pour défragmenter la RAM.
	gc.collect()

	sleep_ms(500) # Temporisation d'une demi-seconde

# Boucle infinie d'acquisition et affichage
while True:
	loop()
