# Objet du script : Allumer ou éteindre une LED avec un bouton.
# Le bouton est géré avec une interruption.
# Un premier appui sur le bouton allume la LED, un deuxième l'éteint.
# Matériel requis en plus de la NUCLEO-WB55 : un bouton connecté à la broche
# D4 et une LED connectée à la broche D2.
# Filtre anti-rebonds réalisé avec les interruptions d'un timer

# Buffer alloué pour que les messages d'erreur des routines de service des interruptions
# soient notifiés correctement (peut être commenté après test du code)
import micropython
micropython.alloc_emergency_exception_buf(100)

from pyb import Pin, Timer # Pour gérer les GPIO et les timers

timer_running = 0 # Est-ce que le timer est en train de compter ?
previous_state = -1 # Etat précédent du bouton
current_state = 0 # Etat actuel du bouton 
led_state = 0 # Variable mémorisant l'état de la LED

# Routine de service de l'interruption de dépassement de compteur du timer 1.
# Elle s'exécute tous les 10-ièmes de seconde.
def timer_overflow_ISR(timer):
	# Variables globales
	global led_state, current_state, previous_state, timer_running
	# Relevé de l'état du bouton
	current_state = button_in.value()
	# Si l'état  n'a pas changé depuis la précédente interruption du timer
	if current_state == previous_state:
		# Arrête le timer
		timer.deinit()
		# Inverse l'état de la LED (0->1 ou 1->0)
		led_state = not led_state
		led_out.value(led_state)
		# Mets à jour les variables globales
		timer_running = 0
		previous_state = 0
		current_state = -1
		# Ré-active l'interruption du bouton
		button_in.irq(trigger=button_in.IRQ_RISING, handler=button_falling_ISR)
	else:
		# Autrement, mémorise l'état actuel du bouton
		previous_state = current_state


# On configure le bouton en entrée (IN) sur la broche D4.
# Le mode choisi est PULL UP : le potentiel de D4 est forcé à +3.3V
# lorsque le bouton n'est pas appuyé.
button_in = Pin('D4', Pin.IN, Pin.PULL_UP)

# On configure la LED en sortie Push-Pull (OUT_PP) sur la broche D2.
# Le mode choisi est PULL NONE : le potentiel de D2 n'est pas fixé.

led_out = Pin('D2', Pin.OUT_PP, Pin.PULL_NONE) # Broche de la LED
led_out.value(led_state) # LED initialement éteinte

# Compte le nombre de fois où l'interruption du bouton a été lancée
it_trigger_count = 0

# Routine de service de l'interruption du bouton
def button_falling_ISR(pin):
	# Démarre le timer 1 à la fréquence de 10 Hz.
	global it_trigger_count
	it_trigger_count +=1
	print("Interruption du bouton activée ", it_trigger_count, " fois")
	global timer_running # Variables globales
	if not timer_running: # Si aucun timer n'est démarré
		# Commence par désactiver l'interruption du bouton
		button_in.irq(trigger=button_in.IRQ_RISING, handler=None)
		# Démarre un timer de fréquence 10 Hz
		tim1 = pyb.Timer(1, freq=10)
		timer_running = 1
		# La routine/ISR "timer_overflow_ISR" sera exécutée toutes le 1/10 secondes, au moment de
		# l'interruption de dépassement du timer
		tim1.callback(timer_overflow_ISR)

# On "attache" l'ISR à la broche du bouton, elle prend effet alors que celui-ci est enfoncé (IRQ_FALLING)
button_in.irq(trigger=button_in.IRQ_FALLING, handler=button_falling_ISR)
