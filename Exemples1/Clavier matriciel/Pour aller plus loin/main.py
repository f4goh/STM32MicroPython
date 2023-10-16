# Objet du script : 
# Mise en œuvre d'un digicode avec le keypad.

from pyb import Pin, ExtInt
from time import sleep
print("start")

#*** Définition des vecteurs d'entrée, de sortie et d'interruptions ***
IN = [0]*4
OUT = [0]*4
IRQ = [0]*4

#*** Définition des connexions physiques ***
ROW = ['A15', 'C10', 'A10', 'C6']
COLUMN = ['A9','C12', 'C13', 'A8']

#*** Définition de la matrice représentative du clavier ***
MATRIX = [[1,2,3,'A'],[4,5,6,'B'],[7,8,9,'C'],['*',0,'#','D']]	

#*** Attribution des sorties ***
for a in range(4):
	OUT[a] = Pin(ROW[a], Pin.OUT)
	OUT[a].value(1)

blue_led = pyb.LED(3)
green_led = pyb.LED(2)
red_led = pyb.LED(1)

#*** Flags et fonctions d'interruption ***
flag = 0
flag_BP = 0

def inter(line):	# Appui keypad
	global flag
	sleep(0.2)
	flag = 1
	
def BP(line):		# Appui SW1
	global flag_BP
	global nb_input
	print("Saisir nouveau code : ")
	blue_led.on()
	flag_BP = 1
	nb_input = 0

#*** Attribution des entrées en interruption ***
for a in range(4):
	IN[a] = pyb.Pin( COLUMN[a] , pyb.Pin.IN)
	IN[a].init(pyb.Pin.IN, pyb.Pin.PULL_DOWN, af=-1)
	IRQ[a] = ExtInt(IN[a], ExtInt.IRQ_RISING, Pin.PULL_DOWN, inter)
	
sw1 = pyb.Pin('SW1')
sw1.init(pyb.Pin.IN, pyb.Pin.PULL_UP, af=-1)
irq_BP = pyb.ExtInt(sw1, pyb.ExtInt.IRQ_FALLING, pyb.Pin.PULL_UP, BP)

#*** Définition des variables permettant la gestion du digicode ***	
old_carac = -1
nb_input = 0
code = [1,2,3,'A']
input_code = [0]*4

#*** Fonction qui gère l'appuie sur une touche du keypad ***
def appuie():
	global flag
	global old_carac
	global nb_input
	global input_code
	global code
	
	flag = 0
		
	for i in range(4):
		if(IN[i].value()==1):	# Test quelle colonne est concernée par l'appuie 
			for j in range(4):	# Eteint les différentes lignes
				OUT[j].value(0);
				if(IN[i].value()==0):
					# Trouve le bouton appuyé et l'affiche en gérant les rebonds et 
					# supprimant les appuies longs
					if (MATRIX[i][j]!=old_carac):
						print(MATRIX[i][j])
						old_carac = MATRIX[i][j]
						input_code[nb_input] = MATRIX[i][j]
						
						if(flag_BP == 1):
							code[nb_input] = MATRIX[i][j]	# Change le code
							 
						nb_input = nb_input + 1
						
					for k in range(4):
						OUT[k].value(1)		# Rallume toutes les lignes
					break;	

#*** Fonction qui teste si le code entré est le bon ***
def test_code():
	global nb_input
	
	for i in range(4):
		if(code[i] != input_code[i]):
			print("Code faux")
			red_led.on()
			nb_input = 0
			sleep(2)
			red_led.off()
			print("\nEntrez le code à 4 chiffres : ")
			return -1
	print("Code juste")
	green_led.on()
	nb_input = 0
	sleep(2)
	green_led.off()
	print("\nEntrez le code à 4 chiffres : ")

			
#*** Début du programme principal ***
print("Entrez le code à 4 chiffres : ")	
	
while True:
	if((flag == 1) and (nb_input < 4)):	# Si une touche a été appuyée
		appuie()
		
	if (nb_input >= 4):	# Si le code est saisie en entier
		
		if(flag_BP==1):		# Gestion du nouveau code
			flag_BP=0
			print("Le nouveau code est : ", code[0], code[1], code[2], code[3])
			nb_input = 0
			sleep(2)
			blue_led.off()
			print("\nEntrez le code à 4 chiffres : ")	
			
		else:
			test_code()
