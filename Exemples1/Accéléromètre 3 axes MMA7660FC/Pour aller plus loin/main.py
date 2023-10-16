# Objet du script : Mise en œuvre de l'accéléromètre 3 axes MMA7660FC (+/- 1.5g)
# Datasheet : https://www.nxp.com/docs/en/data-sheet/MMA7660FC.pdf

from machine import I2C
import mma7660 # Pour gérer l'accéléromètre
import pyb # Pour gérer les entrées-sorties (LED)
from time import sleep_ms # Pour les temporisations

# On utilise l'I2C n°1 de la carte NUCLEO-WB55 pour communiquer avec le capteur
i2c = I2C(1) 

# Pause d'une seconde pour laisser à l'I2C le temps de s'initialiser
sleep_ms(1000)

# Liste des adresses I2C des périphériques présents
print("Adresses I2C utilisées : " + str(i2c.scan()))

# Instanciation de l'accéléromètre
accelerometer = mma7660.MMA7660(i2c)

# On appelle la méthode "start()" pour démarrer l'accéléromètre
accelerometer.start()

# Instantiation des LED
blue_led = pyb.LED(1)
green_led = pyb.LED(2)
red_led = pyb.LED(3)

THRESHOLD = 0.75 # Seuil d'accélération pour allumer ou éteindre les LED

last_face = -1
last_orientation = -1

while True:

	# On appelle la méthode "get()" pour récupérer les mesures de l'accéléromètre
	ax, ay, az = accelerometer.get()
	
	# Si la valeur absolue de l'accélération sur l'axe X est supérieure à THRESHOLD mg alors
	if abs(ax) > THRESHOLD :
		green_led.on()
	else:
		green_led.off()
		
	# Si la valeur absolue de l'accélération sur l'axe Y est supérieure à THRESHOLD mg alors
	if abs(ay) > THRESHOLD : 
		blue_led.on()
	else:
		blue_led.off()

	# Si la valeur absolue de l'accélération sur l'axe Z est supérieure à THRESHOLD mg alors
	if abs(az) > THRESHOLD : 
		red_led.on()
	else:
		red_led.off()

	# Rapporte les taps
	if accelerometer.tap():
		print("Tap !")

	# Rapporte les secousses
	if accelerometer.shake():
		print("Secousse !")

	# Rapporte l'orientation (type "pile ou face") du module. Pour que la réponse de cette
	# fonction soit cohérente, vous devez positionner le module Grove de sorte que
	# sont axe Z soit proche de la verticale.

	if abs(az) > 0.7: # Si le module est tenu presque horizontalement
		face = accelerometer.facing()
		if face != last_face:
			last_face = face
			if face == 0:
				print("Plan du module (côté connecteur Grove) orienté vers le haut")
			elif face == 1 :
				print("Plan du module (côté connecteur Grove) orienté vers le bas")
	else:
		last_face = -1

	# Test de l'orientation en mode portrait - paysage. Pour que la réponse de cette
	# fonction soit cohérente, vous devez positionner le module Grove de sorte que
	# sont axe Z pointe vers vous et soit proche de l'horizontale.
	
	if abs(az) < 0.3: # Si le module est tenu presque verticalement
		orientation = accelerometer.orientation()
		if orientation != last_orientation:
			last_orientation = orientation
			if orientation == 6:
				print("Portrait - paysage : axe Y vers la droite, axe X vers le bas")
			elif orientation == 5:
				print("Portrait - paysage : axe Y vers la gauche, axe X vers le haut")
			elif orientation == 2:
				print("Portrait - paysage : axe Y vers le bas, axe X vers la gauche")
			elif orientation == 1:
				print("Portrait - paysage : axe Y vers le haut, axe X vers la droite")
	else:
		last_orientation = -1

	sleep_ms(250) # Temporisation d'un quart de seconde
