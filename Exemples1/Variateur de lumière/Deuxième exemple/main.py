# Objet du Script : Mise en œuvre d'une PWM pour réaliser un variateur de lumière.
# L'intensité de la LED cesse de varier après un premier appui sur le bouton sw1.
# Elle recommence à varier après un second appui sur sw1.
# Utilisation d'une interruption externe pour gérer le bouton.
# Matériel (en plus de la carte NUCLEO-WB55) : une LED connectée sur D6 et GND.

from pyb import Pin, Timer, ExtInt
from time import sleep_ms
import gc # Ramasse miettes, pour éviter de saturer la mémoire

# Initialisation du bouton SW1
sw1 = pyb.Pin( 'SW1' , pyb.Pin.IN)
sw1.init(pyb.Pin.IN, pyb.Pin.PULL_UP, af=-1)

# Est-ce que le bouton a été pressé ?
button_pressed = False

# Routine de gestion de l'interruption du bouton
def ISR_bouton(line):
#	print("line =", line)
	global button_pressed # mot clef "global" très important ici
	button_pressed = not button_pressed

ext = ExtInt(Pin('SW1'), ExtInt.IRQ_RISING, Pin.PULL_UP, ISR_bouton)

# initialisation de la PWM 
led_pin = Pin('D6') 
ti = 1 # Timer 
ch = 1 # Canal
tim = Timer(ti, freq=1000) # Fréquence de la PWM fixée à 1kHz
ch = tim.channel(ch, Timer.PWM, pin=led_pin)
i=0

while True:

	if button_pressed :

		while i < 101: # augmente l'intensité de la LED par pas de 1%
			ch.pulse_width_percent(i)
			i=i+1
			sleep_ms(10) # pause de 10 ms

		while i > 0: # réduit l'intensité de la LED par pas de 1%
			ch.pulse_width_percent(i)
			i=i-1
			sleep_ms(10) # pause de 10 ms

	# Appel du ramasse-miettes, indispensable pour que le programme ne se bloque pas
	# très rapidement en fragmentant complètement la RAM.
	gc.collect()