# Objet du script : Mettre en œuvre un capteur de mouvement PIR
# Le module PIR Motion sensor de Grove que nous avons sélectionné renvoie un signal non nul 
# pendant une seconde après qu'il ait détecté un mouvement. Si d'autres mouvements surviennent
# pendant cette seconde, il ne les distinguera pas de celui qui l'a activé en premier. 

from machine import Pin
from time import sleep

# Variable globale qui sera modifiée par la routine de service de l'interruption
motion = False

# Routine de service de l'interruption
# Cette fonction ne fait qu'une chose : elle donne la valeur "True" à la variable globale "motion".
def handle_interrupt(pin):
	global motion
	motion = True


led = Pin('D8', Pin.OUT) # Broche de la LED

pir = Pin('D4', Pin.IN) # Broche du capteur PIR

# On "attache" l'interruption à la broche du capteur PIR.
# Cela signifie que le gestionnaire d'interruptions contenu dans le STM32WB55 va "surveiller" 
# la tension sur la broche D4. Si cette tension augmente et passe de 0 à 3.3V (IRQ_RISING)
# alors le gestionnaire d'interruption forcera le STM32WB55 à exécuter la fontion "handle_interrupt".

pir.irq(trigger=Pin.IRQ_RISING, handler=handle_interrupt)

while True:
	if motion: # si motion = True alors, cela signifie que l'interruption a eue lieu.
		print('Mouvement détecté!')
		led.value(1) # Allume la LED
		sleep(1) # Temporise pendant 1 seconde
		led.value(0) # Eteint la LED
		motion = False
		print('En attente...')
	# Place le microcontrôleur en sommeil en attendant la prochaine interruption
	pyb.wfi() 

