# Objet du script 
# Montre comment piloter un moteur à courant continu avec un pont en H
# sur la base du composant L293D ou L298N de chez STMicroelectronics.

from pyb import Pin, Timer
import time
import gc # Ramasse miettes, pour éviter de saturer la mémoire

# Variables globales
BP1 = 0
BP2 = 0
BP3 = 1

# BP (en entrée + pull up)
sw1 = pyb.Pin('SW1')
sw1.init(pyb.Pin.IN, pyb.Pin.PULL_UP, af=-1)
sw2 = pyb.Pin('SW2')
sw2.init(pyb.Pin.IN, pyb.Pin.PULL_UP, af=-1)
sw3 = pyb.Pin('SW3')
sw3.init(pyb.Pin.IN, pyb.Pin.PULL_UP, af=-1)

# LED (LED de la carte NUCLEO)
red_led = pyb.LED(1)
blue_led = pyb.LED(3)
green_led = pyb.LED(2)

# Driver moteur ("enable" + "input 1" et "input 2" en sorties)
motor_enable = pyb.Pin('D3')
motor_pin1 = pyb.Pin('D4', Pin.OUT_PP)
motor_pin2 = pyb.Pin('D5', Pin.OUT_PP)

# PWM pour le moteur (Timer 1 channel 3, fréquence = 1kHz et sur "enable")
tim1 = Timer(1, freq=1000)
ch3 = tim1.channel(3, Timer.PWM, pin=motor_enable)

# Interruption de SW1 (le moteur tourne dans le sens "avant")
def ITbutton1(line):

	# Variables globales
	global BP1
	global BP2
	global BP3
	
	# Incrémente BP1, le reste à 0
	BP1 = BP1 + 1
	BP2 = 0
	BP3 = 0

# Interruption de SW2 (le moteur tourne dans le sens "arrière")
def ITbutton2(line):

	# Variable globales
	global BP1
	global BP2
	global BP3
	
	# Incrémente BP2, le reste à 0
	BP1 = 0
	BP2 = BP2 + 1
	BP3 = 0

# Interruption de SW3 (arrête le moteur)
def ITbutton3(line):

	# Variables globales
	global BP1
	global BP2
	global BP3
	
	# Incrémente BP3, le reste à 0
	BP1 = 0
	BP2 = 0
	BP3 = BP3 + 1

# Initialisation des vecteurs d'interruption
irq_1 = pyb.ExtInt(sw1, pyb.ExtInt.IRQ_FALLING, pyb.Pin.PULL_UP, ITbutton1)
irq_2 = pyb.ExtInt(sw2, pyb.ExtInt.IRQ_FALLING, pyb.Pin.PULL_UP, ITbutton2)
irq_3 = pyb.ExtInt(sw3, pyb.ExtInt.IRQ_FALLING, pyb.Pin.PULL_UP, ITbutton3)

# Fonction qui gère le moteur
def motor_state(speed):

	# Variables globales
	global BP1
	global BP2
	global BP3

	# Si BP1 appuyé
	if((BP1 != 0) and (BP2 == 0) and (BP3 == 0)):
		# Allume la LED bleu
		blue_led.on()
		# Allume l'enable 1 / Eteint l'enable 2
		motor_pin1.high()
		motor_pin2.low()
		# PWM pour régler la tension du moteur
		ch3.pulse_width_percent(speed)
	 	
	# Si BP2 appuyé
	if((BP1 == 0) and (BP2 != 0) and (BP3 == 0)):
		# Allume la LED verte
		green_led.on()
		# Allume l'enable 2 / Eteint l'enable 1
		motor_pin1.low()
		motor_pin2.high()
		# PWM pour régler la tension du moteur
		ch3.pulse_width_percent(speed)
		
	# Si BP3 appuyé
	if((BP1 == 0) and (BP2 == 0) and (BP3 != 0)):
		# Allume la LED rouge
		red_led.on()
		# Eteint l'enable 1 et 2
		motor_pin1.low()
		motor_pin2.low()
		# PWM pour régler la tension du moteur
		ch3.pulse_width_percent(0)

# Variable pour gérer la vitesse de rotation du moteur
speed = 100

#Boucle infinie
while True:

	# Eteint toutes les LED par défaut
	blue_led.off()
	green_led.off()
	red_led.off()
	
	# Passe en parametre la vitesse souhaitée
	motor_state(speed)
	
	# Appel du ramasse-miettes
	gc.collect()