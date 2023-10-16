# Objet du Script : Mise en œuvre d'une PWM pour réaliser un variateur de lumière.
# L'intensité de la LED cesse de varier lorsque le bouton sw1 est relâché.
# Gestion du bouton par "scrutation" ("polling" en anglais).
# Matériel (en plus de la carte NUCLEO-WB55) : une LED connectée sur D6 et GND.

from pyb import Pin, Timer
from time import sleep_ms
import gc # Ramasse miettes, pour éviter de saturer la mémoire

# Initialisation du bouton SW1
sw1 = pyb.Pin( 'SW1' , pyb.Pin.IN)
sw1.init(pyb.Pin.IN, pyb.Pin.PULL_UP, af=-1)

button_pressed = False

# initialisation de la PWM 
led_pin = Pin('D6') 
ti = 1 # Timer 
ch = 1 # Canal
tim = Timer(ti, freq=1000) # Fréquence de la PWM fixée à 1kHz
ch = tim.channel(ch, Timer.PWM, pin=led_pin)
i=0

while True:

	if not sw1.value(): # Si le bouton est appuyé

		while i < 101: # Augmente l'intensité de la LED par pas de 1%
			ch.pulse_width_percent(i)
			i=i+1
			sleep_ms(10) # Pause de 10 ms

		while i > 0: # Réduit l'intensité de la LED par pas de 1%
			ch.pulse_width_percent(i)
			i=i-1
			sleep_ms(10) # Pause de 10 ms

	else:
		ch.pulse_width_percent(0) # Si le bouton n'est pas appuyé

	# Appel du ramasse-miettes, indispensable pour que le programme ne se bloque pas
	# très rapidement en fragmentant complètement la RAM.
	gc.collect()
