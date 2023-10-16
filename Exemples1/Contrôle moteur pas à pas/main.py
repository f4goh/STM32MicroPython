# Objet du script : mise en œuvre d'un contrôle de moteur pas à pas

from pyb import Pin, Timer
from time import sleep_ms
import gc # Ramasse miettes, pour éviter de saturer la mémoire

# Variables globales
motor_state = 0
motor_rotation = 0

# BP (en entrée + pull up)
sw1 = pyb.Pin('SW1')
sw1.init(pyb.Pin.IN, pyb.Pin.PULL_UP, af=-1)
sw2 = pyb.Pin('SW2')
sw2.init(pyb.Pin.IN, pyb.Pin.PULL_UP, af=-1)

# Initialisation des LED de la carte NUCLEO
blue_led = pyb.LED(3)
green_led = pyb.LED(2)
red_led = pyb.LED(1)

# GPIO qui controle le relais/transistor
A = pyb.Pin('D0', Pin.OUT_PP)
B = pyb.Pin('D1', Pin.OUT_PP)
C = pyb.Pin('D2', Pin.OUT_PP)
D = pyb.Pin('D3', Pin.OUT_PP)

motor_pin = (A, B, C, D)

# Interruption de SW1
def ITbutton1(line):
	# Variables globales
	global motor_state
	# Etat moteur à 0 ou 1
	if(motor_state == 1):
		motor_state = 0
	else:
		motor_state = 1

# Interruption de SW2
def ITbutton2(line):
	# Variables globales
	global motor_rotation
	# Sens moteur à 0 (sens horaire) ou 1 (sens anti-horaire)
	if(motor_rotation == 1):
		motor_rotation = 0
	else:
		motor_rotation = 1
	# Faire un reset du moteur
	motor_stop()

# Initialisation des vecteurs d'interruption
irq_1 = pyb.ExtInt(sw1, pyb.ExtInt.IRQ_FALLING, pyb.Pin.PULL_UP, ITbutton1)
irq_2 = pyb.ExtInt(sw2, pyb.ExtInt.IRQ_FALLING, pyb.Pin.PULL_UP, ITbutton2)

def motor_stopped():
	# Gestion des LED
	blue_led.off()
	green_led.off()
	red_led.on()
	# Eteind toutes les sorties
	for i in range(0, 4, 1):
		motor_pin[i].low()

def motor_running(direction, TempoSpeed):

	i = 0

	#Tourner dans le sens horaire
	if(direction == 0):
		# Gestion des LED
		blue_led.off()
		green_led.on()
		red_led.off()
		# Dans le sens horaire
		for i in range(0, 4, 1):
			# Allume le segment 1
			motor_pin[i].on()
			sleep_ms(TempoSpeed)
			# Allume le segment 2
			if(i == 3):
				motor_pin[0].on()
			else:
				motor_pin[i+1].on()
			sleep_ms(TempoSpeed)
			# Eteind le segment 1
			motor_pin[i].off()
			sleep_ms(TempoSpeed)
	
	#Tourner dans le sens anti-horaire
	if(direction == 1):
		# Gestion des LED
		blue_led.on()
		green_led.off()
		red_led.off()
		# Dans le sens anti-horaire
		for i in range(3, -1, -1):
			# Allume le segment 2
			motor_pin[i].on()
			sleep_ms(TempoSpeed)
			# Allume le segment 1
			if(i == 0):
				motor_pin[3].on()
			else:
				motor_pin[i-1].on()
			sleep_ms(TempoSpeed)
			# Eteind le segment 2
			motor_pin[i].off()
			sleep_ms(TempoSpeed)

# Temporisation de la vitesse de rotation du moteur. /!\ ne peut être inférieure à 3ms /!\
TempoSpeed = 3

# Boucle infinie
while True:

	if(motor_state == 0):
		motor_stopped()
		
	if(motor_state == 1):
		motor_running(motor_rotation, TempoSpeed)

	# Appel du ramasse-miettes
	gc.collect()
