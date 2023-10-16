# Objet du script : Allumer ou éteindre une LED avec un bouton.
# Le bouton est géré avec une interruption.
# Un premier appui sur le bouton allume la LED, un deuxième l'éteint.
# Matériel requis en plus de la NUCLEO-WB55 : un bouton connecté à la broche
# D4 et une LED connectée à la broche D2.
# filtre anti-rebonds réalisé avec une temporisation non blocante.

from pyb import Pin # Classe pour gérer les GPIO
from time import ticks_ms, ticks_diff # Bibliothèque pour gérer les temporisations
 
# On configure le bouton en entrée (IN) sur la broche D4.
# Le mode choisi est PULL UP : le potentiel de D4 est forcé à +3.3V
# lorsque le bouton n'est pas appuyé.

button_in = Pin('D4', Pin.IN, Pin.PULL_UP)

# On configure la LED en sortie Push-Pull (OUT_PP) sur la broche D2.
# Le mode choisi est PULL NONE : le potentiel de D2 n'est pas fixé.

led_out = Pin('D2', Pin.OUT_PP, Pin.PULL_NONE) # Broche de la LED
led_state = 0 # Variable globale pour mémoriser l'état de la LED (allumée ou pas)
led_out.value(led_state) # LED initialement éteinte

# Temporisation du filtre anti-rebonds, en millisecondes
DELAY_MS = const(50) 

# Variable globale qui décompte les appels à button_falling_ISR :
it_trigger_count = 0

# Variable globale pour mesurer le temps écoulé entre deux interruptions du bouton
elapsed_time = ticks_ms() 

# Fonction de gestion de l'interruption du bouton lorsqu'on l'enfonce
@micropython.native # Directive pour générer du code binaire optimisé pour STM32
def button_falling_ISR(pin):

	# Commence par désactiver les interruptions
	pyb.enable_irq(False)

	# Mot clef "global" indispensable pour que l'ISR modifie effectivement les variables concernées
	global it_trigger_count, led_state
	global elapsed_time
	
	it_trigger_count +=1
	print("Interruption du bouton activée ", it_trigger_count, " fois")

	# Autoriser deux activations successives si plus de DELAY_MS ms se sont écoulées 
	if ticks_diff(ticks_ms(), elapsed_time) > DELAY_MS: 
		led_state = not led_state # Inverse l'état de la variable (0->1 ou 1->0)
		led_out.value(led_state) # Inverse l'état de la LED
		# Ré-active les interruptions
		pyb.enable_irq(True)
		
	elapsed_time = ticks_ms()

# On "attache" l'ISR à la broche du bouton, elle prend effet alors que celui-ci est enfoncé (IRQ_FALLING)
button_in.irq(trigger=button_in.IRQ_FALLING, handler=button_falling_ISR)
