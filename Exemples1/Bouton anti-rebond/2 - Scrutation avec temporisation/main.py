# Objet du script : Eteindre une LED en maintenant un bouton appuyé.
# Le bouton est géré en "polling" (scrutation).
# Ajout d'une fonction de temporisation selon la source :
# https://docs.micropython.org/en/latest/pyboard/tutorial/debounce.html

from pyb import Pin # Pour gérer les GPIO
from time import sleep_ms

WAIT_MS = const(20)
WAIT_STEP_MS = const(1)

# Fonction de temporisation
def wait_button_stable(pin):
	# Attend que la valeur de la broche ait changée
	# Elle doit rester stable pendant au moins WAIT_MS millisecondes
	global button_state
	button_state = pin.value()
	print("Statut du bouton : ", button_state)
	elapsed_time = 0
	while elapsed_time < WAIT_MS:
		if pin.value() != button_state:
			elapsed_time += WAIT_STEP_MS
		else:
			elapsed_time = 0
		sleep_ms(WAIT_STEP_MS)

BUT_PIN = 'D4' # Broche du bouton
LED_PIN = 'D2' # Broche de la LED

# On configure le bouton en entrée (IN) sur la broche D4 en "PULL UP"

button_in = Pin(BUT_PIN, Pin.IN, Pin.PULL_UP)

# On configure la LED en sortie Push-Pull (OUT_PP) sur la broche D2.
# Le mode choisi est PULL NONE : le potentiel de D2 n'est pas fixé.
led_out = Pin(LED_PIN, Pin.OUT_PP, Pin.PULL_NONE)

# On commence avec la LED éteinte
button_state = 0 # Variable contenant l'état du bouton
led_state = 0 # Variable contenant l'état de la LED
led_out.value(led_state) # Eteint la LED

while True : # Boucle sans clause de sortie ("infinie")

	# Attend que l'état de la broche du bouton soit stable
	wait_button_stable(button_in)

	# Dans notre configuration button_state vaut 1 lorsque le bouton est enfoncé, 
	# ce qui inverse l'état de la LED
	if button_state == 1:
		if led_state == 1:
			led_state = 0
		else:
			led_state = 1
		print("Statut de la LED : ", led_state)
		
	led_out.value(led_state)
