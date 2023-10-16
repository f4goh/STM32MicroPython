# Objet du script : utiliser la technologie RFID pour réaliser une serrure sécurisée (bis)

import pyb
import time
import mfrc522

# Initialisation du lecteur de badge
rdr = mfrc522.MFRC522('D13', 'D11', 'D12', 'D9', 'D10') #SCK, MOSI, MISO, RST, SDA

# Initialisation des LEDs (LED_1, LED_2, LED_3)
blue_led = pyb.LED(3)
green_led = pyb.LED(2)
red_led = pyb.LED(1)

blue_led.on()
red_led.off()
green_led.off()

# Initialisation du servomoteur
servo = pyb.Pin('D6')

# Initialisation du buzzer
buzzer = pyb.Pin('D3')

# Initialisations des boutons
sw1 = pyb.Pin('SW1', pyb.Pin.IN)
sw1.init(pyb.Pin.IN, pyb.Pin.PULL_UP, af=-1)
sw2 = pyb.Pin('SW2', pyb.Pin.IN)
sw2.init(pyb.Pin.IN, pyb.Pin.PULL_UP, af=-1)
sw3 = pyb.Pin('SW3', pyb.Pin.IN)
sw3.init(pyb.Pin.IN, pyb.Pin.PULL_UP, af=-1)

# Variables
counter = 0
MASTERKEY = [None]*12
e = 0
nb_max_tag = const(8)

print("\nEnregistrement d'un premier badge")

#Boucle infinie
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

	# Enregistrement d'un nouveau badge si on appuie sur SW1
	elif sw1.value() == 0:
		if e < nb_max_tag:
			blue_led.on()
			print("\nEnregistrement d'un autre badge")
			(stat, tag_type) = rdr.request(rdr.REQIDL)
			(stat, raw_uid) = rdr.anticoll()
			while(stat == rdr.ERR): # En attente tant qu'il n'y a pas de badge détecté
				(stat, tag_type) = rdr.request(rdr.REQIDL)
				(stat, raw_uid) = rdr.anticoll()
			if stat == rdr.OK: # Si badge détecté alors on enregistre
				e = e + 4 # Pointer dans un emplacement vide de MASTERKEY
				MASTERKEY = MASTERKEY + raw_uid[0:4] # MASTERKEY stocke les anciens UID + le nouveau UID
				print("-"*36)
				print("| UID enregistré : %03d.%03d.%03d.%03d |" %(MASTERKEY[e], MASTERKEY[e+1], MASTERKEY[e+2], MASTERKEY[e+3]))
				print("-"*36)
				blue_led.off()
		else:
			print("\n|!| Erreur : déjà 3 badges enregistrés |!|")

	# Affichage des UID enregistrés si on appuie sur SW2
	elif sw2.value() == 0:
		print("\nListe des UID enregistrés")
		print("-"*23)
		for i in range(0, e+1, 4):
			print("| --> %03d.%03d.%03d.%03d |"%(MASTERKEY[i+0], MASTERKEY[i+1], MASTERKEY[i+2], MASTERKEY[i+3]))
		print("-"*23)

	# Suppression d'un badge si appuie sur SW3
	elif sw3.value() == 0:
		print("\nSupression d'un badge")
		red_led.on()
		while(stat == rdr.ERR): # En attente tant qu'il n'y a pas de badge détecté
			(stat, tag_type) = rdr.request(rdr.REQIDL)
			(stat, raw_uid) = rdr.anticoll()
		if stat == rdr.OK:
			j = 0
			while(MASTERKEY[j:j+4] != raw_uid[0:4]): # Recherche de l'UID du badge présenté dans ceux stockés
				j = j + 4
			del MASTERKEY[j:j+4] # Suppression du badge
			e = e - 4
			print("Badge n°%d supprimé !" %(j/4+1))
			red_led.off()

	#Affichage de l'UID dans le moniteur série
	elif stat == rdr.OK and counter != 0:
		(stat, raw_uid) = rdr.anticoll()
		if stat == rdr.OK:
			del raw_uid[4]
			print("\nUID lu : %03d.%03d.%03d.%03d" %(raw_uid[0], raw_uid[1], raw_uid[2], raw_uid[3]))

		# Vérification du badge
		if (raw_uid[0:4] == MASTERKEY[0:4]) or (raw_uid[0:4] == MASTERKEY[4:8]):
			print("--> Badge : valide")
			green_led.on() # Allume la LED verte
			tim_servo = pyb.Timer(1, freq=50)
			tim_servo.channel(1, pyb.Timer.PWM, pin=servo, pulse_width_percent=12.5) # Fait tourner le servomoteur de 90 degrés
			time.sleep(3) # Temporisation de 3 secondes
			tim_servo.channel(1, pyb.Timer.PWM, pin=servo, pulse_width_percent=7.5)
			time.sleep_ms(500) # Délais pour que le servomoteur se remette en place
			tim_servo.deinit() # Arrêt du timer pour le servomoteur
			green_led.off()
		else:
			print("--> Badge : non valide")
			red_led.on() # Allume la LED rouge
			for j in range(0, 5): # Séquence du buzzer
				tim_buzzer = pyb.Timer(1, freq=1000)
				tim_buzzer.channel(3, pyb.Timer.PWM, pin=buzzer, pulse_width_percent=5)
				time.sleep_ms(200)
				tim_buzzer = pyb.Timer(1, freq=3000)
				tim_buzzer.channel(3, pyb.Timer.PWM, pin=buzzer, pulse_width_percent=5)
				time.sleep_ms(200)
			tim_buzzer.deinit() # Arrêt du timer pour le buzzer
			red_led.off() # Eteint la LED rouge
