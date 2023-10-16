# Objet du script :
# Conception d'un système d'alarme basé sur un détecteur de mouvements.
# Un capteur de mouvement PIR est configuré en interruption sur la broche D2.
# Un buzzer est connecté à la broche D3 et piloté par une PWM.
# Matériel requis :
#   - Un capteur PIR (de préférence fonctionnant en 3.3V)
#   - Un buzzer (de préférence fonctionnant en 3.3V)
# On utilise une interruption pour capturer le signal du détecteur de mouvements.


from time import ticks_ms, ticks_diff # Pour gérer les temporisations
from pyb import Pin, Timer

# Configuration du buzzer
frequency = 440
buz = Pin('D3')

# D3 génère une PWM avec TIM1, CH3
timer1 = Timer(1, freq=frequency)
channel3 = timer1.channel(3, Timer.PWM, pin=buz)

# Configuration du capteur PIR
PIR_Pin = Pin('D2', Pin.IN)

# Durée de l'alarme en millisecondes
_ALARM_DURATION_MS = const(999)

# Variables globales
motion = False # Est-ce que j'ai détecté un mouvement ?
tick_alarm_start = 0 # Nombre de millisecondes système au moment de l'alarme

# Fonction de gestion de l'interruption du capteur PIR
def interrupt_handler(pin):
	
	global motion, tick_alarm_start
	global interrupt_pin
	
	# Signale qu'un mouvement a été détecté
	motion = True
	
	# Date de l'évènement
	tick_alarm_start = ticks_ms()

	# Broche générant l'interruption
	interrupt_pin = PIR_Pin

# Activation de l'interruption du capteur PIR
PIR_Pin.irq(trigger=PIR_Pin.IRQ_RISING, handler=interrupt_handler)

# Boucle principale
while True:

	if motion:
		
		print('Mouvement détecté')
		
		# Désactive l'interruption du capteur PIR
		PIR_Pin.irq(trigger=PIR_Pin.IRQ_RISING, handler=None)

		# Rapport cyclique paramétré à 5% (le buzzer est alimenté 5% du temps d'une période)
		channel3.pulse_width_percent(5)

		# Nombre de millisecondes écoulées depuis la détection du mouvement

		if ticks_diff(ticks_ms(), tick_alarm_start) > _ALARM_DURATION_MS:

			# Rapport cyclique paramétré à 0% (le buzzer n'est plus alimenté)
			channel3.pulse_width_percent(0)
		
			# Interruption du capteur réactivée
			PIR_Pin.irq(trigger=PIR_Pin.IRQ_RISING, handler=interrupt_handler)
			print('Détecteur de mouvement desactivé')
			
			# Signale que le traitement de la détection de mouvement est terminé
			motion = False

	# Place le microcontrôleur en sommeil en attendant la prochaine interruption
	pyb.wfi() 
