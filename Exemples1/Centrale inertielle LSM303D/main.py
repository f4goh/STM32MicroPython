# Objet du script : mise en œuvre du module Grove "6 Axis Accelerometer And Compass_V2.0".
# Il utilise un bus I2C.
# Cet exemple montre comment programmer une boussole avec compensation d'inclinaison 
# à l'aide de ce module. 
# La compensation d'inclinaison est calculée à l'aide des instructions du document AN3192 
# de STMicroelectronics disponible en téléchargement sur le site Web STM32python.
# Source : https://github.com/Seeed-Studio/Grove_6Axis_Accelerometer_And_Compass_v2/blob/master/LSM303D.cpp

from machine import I2C
from lsm303 import LSM303D # Pilote de l'IMU
from time import sleep_ms
from math import sqrt, atan2, pi, asin, cos, sin
import gc # Ramasse miette

# On utilise l'I2C n°1 de la carte NUCLEO-WB55 pour communiquer avec le capteur
i2c = I2C(1) 

# Pause d'une seconde pour laisser à l'I2C le temps de s'initialiser
sleep_ms(1000)

# Liste des adresses I2C des périphériques présents
print("Adresses I2C utilisées : " + str(i2c.scan()))

# Paramètres pour calibrer le magnétomètre (par défaut, "neutres" car le module est déjà parfaitement
# calibré en usine).

OFFSET_X = 0
OFFSET_Y = 0
OFFSET_Z = 0

SCALE_X = 1
SCALE_Y = 1
SCALE_Z = 1

# Initialisation de l'instance de l'IMU
imu = LSM303D(i2c, ox = OFFSET_X, oy = OFFSET_Y, oz = OFFSET_Z, sx = SCALE_X, sy = SCALE_Y, sz = SCALE_Z)

# Précalculs de constantes trigonométriques
twopi = 2 * pi
halfpi = pi * 0.5
three_halfpi = 3 * halfpi

# Facteur de conversion entre les radians et les degrés pour les angles
RadToDeg = 180 / pi

# Doit-on lancer la procédure de collecte de données pour calibrer le magnétomètre ?
# ATTENTION : ce module étant déjà calibré en usine le recalibrer aura probablement pour conséquence de dégrader 
# sa précision, nous déconseillons donc cette opération. Cependant, elle pourrait être utile si le module est 
# fixé sur un système plus gros qui introduit des distorsions Hard Iron et Soft Iron supplémentaires.

CALIBRATE_COMP = False

if CALIBRATE_COMP:
	# Lance la routine de calibrage
	imu.calibrate_mag()

else:
	# Simule une boussole avec compensation d'inclinaison
	while True:

		# Mesure des vecteurs accélération et champ magnétique 
		acc = imu.get_acc()
		mag = imu.get_mag()
		
		# Calcule la norme des vecteurs
		norm_acc = sqrt(acc[0]*acc[0] + acc[1]*acc[1] + acc[2]*acc[2])
		norm_mag = sqrt(mag[0]*mag[0] + mag[1]*mag[1] + mag[2]*mag[2])

		# Si les deux normes sont non-nulles
		if norm_acc > 0 and norm_mag > 0:

			# Normalise les composantes des vecteurs afin de pouvoir calculer
			# les arcsinus et arccosinus qui suivent.

			inv_acc = 1 / norm_acc

			ax = acc[0] * inv_acc
			ay = acc[1] * inv_acc
			az = acc[2] * inv_acc 
		
			inv_mag = 1 / norm_mag

			bx = mag[0] * inv_mag
			by = mag[1] * inv_mag
			bz = mag[2] * inv_mag
			
			# Calcule les angles d'Euler
			
			pitch = asin(-ax)
			temp = cos(pitch)
			if temp:
				roll = asin(ay/cos(pitch))
			else:
				roll = 0

			xh = bx * cos(pitch) + bz * sin(pitch)
			yh = bx * sin(roll) * sin(pitch) + by * cos(roll) - bz * sin(roll) * cos(pitch)
			# zh = -bx * cos(roll) * sin(pitch) + by * sin(roll) + bz * cos(roll) * cos(pitch)

			# Heading (ou Yaw) : cap (ou lacet) que l'on recherche, la rotation autour de (Oz)
			if xh > 0 and yh >= 0:
				heading = atan2(yh, xh)
			elif xh < 0:
				heading = pi + atan2(yh, xh)
			elif xh > 0 and yh <= 0:
				heading = twopi + atan2(yh, xh)
			elif xh == 0 and yh < 0:
				heading = halfpi
			elif xh == 0 and yh > 0:
				heading = three_halfpi

			# Expression des angles en degrés pour affichage
			pitch_deg = pitch * RadToDeg
			roll_deg = roll * RadToDeg
			heading_deg = heading * RadToDeg
			
			# Affichage des angles
			print("Pitch (tangage) = %.1f°" % pitch_deg)
			print("Roll (roulis) = %.1f°" % roll_deg)
			print("Heading (cap) = %.1f°" % heading_deg)
			print("")
		
		gc.collect() # défragmentation de la RAM
		sleep_ms(250)
