# Objet du script :
# Piloter un servomoteur
# Exemple de valeurs de PWM pour le servomoteur Grove livré avec les kits 
# de base pour Arduino.


from time import sleep # Pour temporiser
import pyb # Pour accéder  aux broches et aux compteurs (timers)

servo = pyb.Pin('D6')

Timer_Num = 1 # Numéro du timer
Timer_Cha = 1 # Canal du timer
Timer_Freq = 50 # Fréquence du timer (en Hz)

while True:

	print("Servomoteur à 0 degrés")
	tim_servo = pyb.Timer(Timer_Num, freq=Timer_Freq) # Démarrage du timer
	tim_servo.channel(Timer_Cha, pyb.Timer.PWM, pin=servo, pulse_width_percent=5)	# Servomoteur à 0 degrés
	sleep(5) # temporisation de 5 secondes

	print("Servomoteur à 90 degrés")
	tim_servo = pyb.Timer(Timer_Num, freq=Timer_Freq) # Démarrage du timer
	tim_servo.channel(Timer_Cha, pyb.Timer.PWM, pin=servo, pulse_width_percent=2)	# Servomoteur à 90 degrés
	sleep(5) # temporisation de 5 secondes
	
	print("Servomoteur à -90 degrés")
	tim_servo = pyb.Timer(Timer_Num, freq=Timer_Freq) # Démarrage du timer
	tim_servo.channel(Timer_Cha, pyb.Timer.PWM, pin=servo, pulse_width_percent=9.5)	# Servomoteur à -90 degrés
	sleep(5) # temporisation de 5 secondes


tim_servo.deinit() # Arrêt du timer