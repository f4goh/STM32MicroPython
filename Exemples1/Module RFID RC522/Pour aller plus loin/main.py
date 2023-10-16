# Objet du script : utiliser la technologie RFID pour réaliser une serrure sécurisée

import pyb
import time
import mfrc522

#Initialisation du lecteur de badge
rdr = mfrc522.MFRC522('D13', 'D11', 'D12', 'D9', 'D10')		#SCK, MOSI, MISO, RST, SDA

# Initialisation des LEDs (LED_1, LED_2, LED_3)
blue_led = pyb.LED(3)
green_led = pyb.LED(2)
red_led = pyb.LED(1)
blue_led.on()
red_led.off()
green_led.off()

# Initialisation du servomoteur
servo = pyb.Pin('D6')

# Variables
counter = 0
MASTERKEY = [None]*4

print("\nEnregistrement d'un premier badge")

# Boucle infinie
while True:
	# Lecture d'un badge
	(stat, tag_type) = rdr.request(rdr.REQIDL)
	# Enregistrement de l'UID d'un badge
	if stat == rdr.OK and counter == 0:
		(stat, raw_uid) = rdr.anticoll()
		if stat == rdr.OK:
			MASTERKEY = raw_uid[0:4] # Récupère les valeurs de l'UID
			print("-"*36)
			print("| UID enregistré : %03d.%03d.%03d.%03d |" %(MASTERKEY[0], MASTERKEY[1], MASTERKEY[2], MASTERKEY[3]))
			print("-"*36)
			counter = counter + 1 # Incrémente le counter pour ne plus revenir dans cette boucle
			blue_led.off()

	# Affichage de l'UID dans le moniteur série
	elif stat == rdr.OK and counter != 0:
		(stat, raw_uid) = rdr.anticoll()
		if stat == rdr.OK:
			print("\nUID lu : %03d.%03d.%03d.%03d" %(raw_uid[0], raw_uid[1], raw_uid[2], raw_uid[3]))

		# Vérification du badge
		if (raw_uid[0:4] == MASTERKEY[0:4]):
			print("--> Badge : valide")
			green_led.on() # Allume la LED verte
			tim_servo = pyb.Timer(1, freq=50)
			tim_servo.channel(1, pyb.Timer.PWM, pin=servo, pulse_width_percent=12.5) #Fait tourner le servomoteur de 90 degrés
			time.sleep(3) # Temporisation de 3 secondes
			tim_servo.channel(1, pyb.Timer.PWM, pin=servo, pulse_width_percent=7.5)
			time.sleep_ms(500) # Délais pour que le servomoteur se remette en place
			tim_servo.deinit() # Arrêt du timer pour le servomoteur
			green_led.off() # Eteint la LED verte
		else:
			print("--> Badge : non valide")
			red_led.on() # Allume la LED rouge
			time.sleep(1) # Temporisation d'une seconde
			red_led.off() # Eteint la LED rouge
