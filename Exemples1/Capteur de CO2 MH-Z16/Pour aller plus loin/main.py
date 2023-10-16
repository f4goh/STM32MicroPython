# Objet du script : Mise en œuvre d'un capteur de CO2 MU-Z16 de Grove
# On utilise cette fois-ci une bibliothèque de classes (mhz16.py).

import mhz16
from pyb import UART # Classe pour gérer l'UART
from time import sleep_ms

uart = UART(2) # Instance de l'UART numéro 2

# Initialisation de l'UART
uart.init(9600, bits=8, parity=None, stop = 1)

# Correction décalage du thermomètre (dépend du module/capteur)
TEMP_OFFSET = const(5)

# Instance du capteur
sensor = mhz16.MHZ16(uart, temp_offset = TEMP_OFFSET)

# Doit-on recalibrer le capteur ?
calibrate = False

# Doit-on préchauffer le capteur ?
preheat = False

# Démarrage de la calibration (dans une pièce aérée ou à l'extérieur)

if preheat:
	print("Préchauffe (5 minutes)")
	sensor.preheat()

if calibrate:
	print("Calibration\n")
	sensor.calibrate()

# Précision du capteur (ppm)
#ACCURACY = const(200)

# Seuil de détection haut du capteur (ppm)
THRESHOLD = const(2000)

while True:

	# Lance une mesure
	(temp_celsius, co2_ppm) = sensor.measure()
	
	# Si les valeurs remontées sont positives
	if temp_celsius != -1 and co2_ppm != -1:
	
		# Affiche  la température et la concentration de CO2
		print("Temperature : %d °C" %temp_celsius)

		if co2_ppm < THRESHOLD:
			print("Concentration en CO2 : %d ppm\n" %co2_ppm)
		else:
			print("Concentration en CO2 > %d ppm\n" %THRESHOLD)

	else:
		print("Problème de mesure")

	# Temporisation de cinq secondes
	sleep_ms(5000)
