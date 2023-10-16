# Objet du script : 
# Jouer un jingle sur un buzzer/speaker (Grove ou autre).
# Cet exemple fait la démonstration de l'usage de la PWM pour la broche D6 sur laquelle est 
# branché le buzzer/speaker.

import pyb

# Liste des fréquences des notes qui seront jouées par le buzzer/speaker
frequency = [262, 294, 330, 349, 370, 392, 440, 494]

# Liste des rapports cycliques (énergie injectée) pour moduler la
# puissance du buzzer/speaker (pourcentages de la période).
percent = [5, 7, 9, 11, 13, 15, 17, 19]

# D6 génère une PWM avec TIM1, CH1
d6 = pyb.Pin('D6', pyb.Pin.OUT_PP) 

# Gestion d'erreurs, pour s'assurer que le buzzer/speaker sera éteint correctement si l'utilisateur
# interromps le script avec CTRL+C.
try:
	while True :
		# Itération entre 0 et 7
		for i in range (0,7) :
			# On ajuste la fréquence pendant l'itération
			tim1 = pyb.Timer(1, freq=frequency[i])
			pwm = tim1.channel(1, pyb.Timer.PWM, pin=d6)
			# Rapport cyclique 
			pwm.pulse_width_percent(percent[i])
			
# En cas d'interruption clavier avec CTRL+C
except KeyboardInterrupt:
	pwm.pulse_width_percent(0) # Arrêt de la génération PWM
	tim1.deinit() # Arrêt du timer