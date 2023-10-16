# Objet du script : Mettre en œuvre un capteur de mouvement PIR avec une temporisation non blocante.
# Le module PIR Motion sensor de Grove que nous avons sélectionné renvoie un signal non nul pendant une seconde après qu'il ait
# détecté un mouvement. Si d'autres mouvements surviennent pendant cette seconde, il ne les distinguera pas de celui qui l'a 
# activé en premier.
# On utilise par ailleurs la méthode "pyb.wfi()" pour placer le microcontrôleur en mode économie d'énergie entre deux interruptions.
# Cette fonction doit être utilisée dans des scripts qui font aussi appel à des interruptions car elles sont nécessaires pour
# sortir sur commande le microcontrôleur de son sommeil.

from machine import Pin
import time # Bibliothèque pour gérer les temporisations

# Routine de service de l'interruption
# Cette fonction ne fait qu'une chose : elle donne la valeur "True" à la variable globale "motion".

def handle_interrupt(pin):
	global motion
	motion = 1 # On signale le mouvement

led = Pin('D8', Pin.OUT) # Broche de la LED signalant l'alarme

pir = Pin('D4', Pin.IN) # Broche du capteur PIR

# On "attache" l'interruption à la broche du capteur PIR.
# Cela signifie que le gestionnaire d'interruptions contenu dans le STM32WB55 va "surveiller" 
# la tension sur la broche D4. Si cette tension augmente et passe de 0 à 3.3V (IRQ_RISING)
# alors le gestionnaire d'interruption forcera le STM32WB55 à exécuter la fontion "handle_interrupt".

pir.irq(trigger=Pin.IRQ_RISING, handler=handle_interrupt)

motion = 0 # Variable globale qui sera modifiée par la rouine de service de l'interruption
start = 0 # Variable globale pour mesurer le temps écoulé 

while True:
	
	# On mesure le temps en millisecondes écoulées depuis le démarrage de MicroPython
	now = time.ticks_ms()

	if led.value() == 0 and motion == 1 : # Si la LED est éteinte et que l'interruption a eue lieu...
		print('Mouvement détecté!') 
		# On mémorise le le temps en millisecondes écoulées depuis le démarrage de MicroPython
		start = time.ticks_ms()
		led.value(1) # On allume la LED
	
	# Si la LED est allumée et que 1 seconde s'est écoulée depuis la dernière détection de mouvement...
	elif led.value() == 1 and time.ticks_diff(now, start) > 999: 
		print('En attente...')
		led.value(0) # On éteint la LED
		motion = 0 # On réinitialise l'indicateur d'occurence d'interruption
		
	# Place le microcontrôleur en sommeil en attendant la prochaine interruption
	pyb.wfi()
