# Objet du script : Mettre en œuvre un module suiveur de ligne
# en utilisant l'interruption de la broche numérique sur laquelle il est
# connecté.

from machine import Pin # Gestion de la broche du suiveur de ligne 

# Variable globale qui sera modifiée par la routine de service de l'interruption
line_detected = False

# Routine de service de l'interruption
# Cette fonction donne la valeur "True" à la variable globale "line_detected" 
# si l'état de la broche "pin" change.
@micropython.viper # Optimise agressivement le pseudo-code MicroPython
def handle_interrupt(pin):
  global line_detected
  line_detected = True
  global interrupt_pin
  interrupt_pin = pin

line_finder = Pin('D7', Pin.IN) # Broche du détecteur de ligne

# On "attache" l'interruption à la broche du détecteur de ligne
# Cela signifie que le gestionnaire d'interruptions contenu dans le STM32WB55 va "surveiller" 
# la tension sur la broche D7. Si cette tension augmente et passe de 0 à 3.3V (IRQ_RISING)
# alors le gestionnaire d'interruption forcera le STM32WB55 à exécuter la fontion "handle_interrupt".

line_finder.irq(trigger=Pin.IRQ_RISING, handler=handle_interrupt)

while True:
	if line_detected: # si line_detected = True alors, cela signifie que l'interruption a eue lieu.
		print("Ligne noire franchie !")
		line_detected = False
	# Place le microcontrôleur en sommeil en attendant la prochaine interruption
	pyb.wfi() 

