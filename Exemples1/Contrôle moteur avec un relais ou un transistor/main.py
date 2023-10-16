# Objet du script : Mise en œuvre d'un contrôle moteur avec un relais ou avec un transistor
# Matériel requis :
#  - La carte NUCLEO-WB55
#  - Une breadboard
#  - Un moteur à courant continu
#  - Une alimentation externe (batterie ou pile)
#  - Un relais HK4100F-DC5V-SHG ou un transistor NPN 2N2222A + une résistance de 220 Ohm, selon le montage choisi

from pyb import Pin, Timer
import gc # Ramasse miettes, pour éviter de saturer la mémoire

# Variables globales
motor_state = 0

# Bouton poussoir (en entrée + pull up)
sw1 = pyb.Pin('SW1')
sw1.init(pyb.Pin.IN, pyb.Pin.PULL_UP, af=-1)

# LED (LED de la carte NUCLEO)
green_led = pyb.LED(2)
red_led = pyb.LED(1)

# GPIO qui contrôle le relais/transistor
motor_pin = pyb.Pin('D4', Pin.OUT_PP)

# Interruption de SW1
def ITbutton1(line):
	# Variables globales
	global motor_state
	# Etat moteur à 0 ou 1
	if(motor_state == 1):
		motor_state = 0
	else:
		motor_state = 1

# Initialisation des vecteurs d'interruption
irq_1 = pyb.ExtInt(sw1, pyb.ExtInt.IRQ_FALLING, pyb.Pin.PULL_UP, ITbutton1)

# Boucle infinie
while True:

	if motor_state == 0:
		green_led.off()
		red_led.on()
		motor_pin.low()
		
	if motor_state == 1:
		green_led.on()
		red_led.off()
		motor_pin.high()
		
	# Appel du ramasse-miettes
	gc.collect()