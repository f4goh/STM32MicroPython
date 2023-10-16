# Objet du script : mise en œuvre d'un capteur de CO2 MU-Z16 de Grove
# Ce script est adapté du forum https://forum.pycom.io/topic/4821/solved-uart-and-mh-z16-co2-sensor/13
# Fiche technique du capteur : https://www.winsen-sensor.com/d/files/MH-Z16.pdf

from pyb import UART # Classe pour gérer l'UART
from time import sleep_ms

uart = UART(2) # Instance de l'UART numéro 2

# Initialisation à 9600 bauds, trames de 8 bits, sans contrôle de parité avec un stop bit à 1
uart.init(9600, bits=8, parity=None, stop = 1)

# Doit-on recalibrer le capteur ?
calibrate = False

# Doit-on préchauffer le capteur ?
preheat = False

# Correction décalage du thermomètre (dépend du module/capteur)
TEMP_OFFSET = const(5)

# Correction décalage du capteur de CO2 (déterminé avec un autre capteur étalonné de CO2)
CO2_OFFSET = const(0)

# Séquence d'octets pour lancer une mesure
CMD_MEASURE = b'\xFF\x01\x86\x00\x00\x00\x00\x00\x79'

# Séquence d'octets pour calibrer
CMD_CALIBRATE = b'\xFF\x87\x87\x00\x00\x00\x00\x00\xF2'

# Nombre d'itérations de chauffe du capteur
HEATING_ROUNDS = const(300) 

if preheat:
	print("Préchauffe (%d minutes)\n" %(HEATING_ROUNDS // 60))
	p = 0
	for i in range(HEATING_ROUNDS):
		# Lance une mesure
		uart.write(CMD_MEASURE)
		# Pause d'une seconde
		sleep_ms(1000)
		p += 1
		if p == 60:
			p = 0
			print(str((i+1) // 60) + " minute(s) écoulée(s)")

# Calibration éventuelle (dans une pièce aérée ou à l'extérieur)
if calibrate:
	print("Démarrage de la calibration\n")
	uart.write(CMD_CALIBRATE)
	print("Fin de la calibration\n")

# Précision du capteur (ppm)
#ACCURACY = const(200)

# Seuil de détection haut du capteur (ppm)
THRESHOLD = const(2000)

while True:

	# Lance une mesure
	uart.write(CMD_MEASURE)
	sleep_ms(10)
	
	# Attends d'avoir reçu la réponse (9 caractères)
	while uart.any() < 9:
		sleep_ms(1)

	# Lecture de la réponse
	resp = bytearray(uart.read(9))

	# Extrait la température et la concentration de CO2 de la réponse 
	co2_ppm = int(resp[2]) * 256 + int(resp[3]) + CO2_OFFSET
	temp_celsius = (int(resp[4]) - 40) + TEMP_OFFSET

	# Affiche  la température et la concentration de CO2
	print("Temperature : %d °C" %temp_celsius)
	if co2_ppm < THRESHOLD:
		print("Concentration en CO2 : %d ppm\n" %co2_ppm)
	else:
		print("Concentration en CO2 > %d ppm\n" %THRESHOLD)

	# Temporisation de cinq secondes
	sleep_ms(5000)

