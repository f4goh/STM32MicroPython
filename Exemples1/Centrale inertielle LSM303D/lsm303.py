# Pilote du MEMS LSM303D de STMicroelectronics
# Fiche technique du composant : https://www.st.com/en/mems-and-sensors/lsm303d.html
# Sources pour le pilote :
#  https://github.com/Seeed-Studio/Grove_6Axis_Accelerometer_And_Compass_v2/blob/master/LSM303D.cpp
#  https://github.com/kamikaze/pyboard-examples/blob/master/imu/lsm303.py (pour l'accéléromètre exclusivement !)

from machine import I2C
from time import sleep_ms
import struct

LSM303D_ADDR =const(0x1E)

STATUS_M = const(0x07)

OUT_X_L_A = const(0x28)
OUT_X_H_A = const(0x29)
OUT_Y_L_A = const(0x2A)
OUT_Y_H_A = const(0x2B)
OUT_Z_L_A = const(0x2C)
OUT_Z_H_A = const(0x2D)

OUT_X_L_M = const(0x08)
OUT_X_H_M = const(0x09)
OUT_Y_L_M = const(0x0A)
OUT_Y_H_M = const(0x0B)
OUT_Z_L_M = const(0x0C)
OUT_Z_H_M = const(0x0D)

CTRL1 = const(0x20)
CTRL2 = const(0x21)
CTRL5 = const(0x24)
CTRL6 = const(0x25)
CTRL7 = const(0x26)

# Facteurs de conversion entre la valeur numérique l'accélération et 
# l'accélération en g (d'après la page 10 de la fiche technique).
ACC_02G = 0.000061
ACC_04G = 0.000122
ACC_06G = 0.000183
ACC_08G = 0.000244
ACC_16G = 0.000732

ACC_RNG = [2 ,4, 6, 8, 16]

# Fréquences possibles de l'accéléromètre (en Hz)
ACC_FRQ = [3.125, 6.25, 12.5, 25, 50, 100, 200, 400, 800, 1600]

# Facteurs de conversion entre la valeur numérique du champ magnétique et 
# le champ magnétique en µT (d'après la page 10 de la fiche technique).
# Pour information : 1 Milligauss = 0.1 Microtesla
MAG_02G = 0.008
MAG_04G = 0.016
MAG_08G = 0.032
MAG_12G = 0.0479

MAG_RNG = [2, 4 ,8, 12]

# Fréquences possibles du magnétomètre (en Hz)
MAG_FRQ = [3.125, 6.25, 12.5, 25, 50, 100]

# Paramètres requis pour le calibrage de magnétomètre.
# Ces valeurs doivent être déterminées pour chaque module Grove à l'aide
# de la fonction calibrate_mag en appliquant la procédure de calibrage.

OFFSET_X = const(0)
OFFSET_Y = const(0)
OFFSET_Z = const(0)

SCALE_X = const(1)
SCALE_Y = const(1)
SCALE_Z = const(1)

class LSM303D():

	# Initialisations
	def __init__(self, i2c, address = LSM303D_ADDR, ox = OFFSET_X, oy = OFFSET_Y, oz = OFFSET_Z, sx = SCALE_X, sy = SCALE_Y, sz = SCALE_Z):
		
		self.address = address
		self.i2c = i2c
		self.i2c.scan()
		
		# Listes tampons pour lire les registres
		self.one_byte = bytearray(1)
		self.six_bytes =  bytearray(6)
		
		# Statut de l'IMU
		self.mag_range = 2 # Sensibilité du magnétomètre +/- 2g
		self.acc_range = 2 # Sensibilité de l'accéléromètre +/- 2 Gauss
		self.acc_freq = 50 # Fréquence des mesures de l'accéléromètre
		self.mag_freq = 50 # Fréquence des mesures du magnétomètre
		
		# Vecteur pour le calibrage du magnétomètre
		self.mag_offset = [ox, oy, oz]
		self.mag_scale = [sx, sy, sz]

		# Arrête l'accéléromètre
		self.i2c.writeto_mem(self.address, CTRL1, bytearray([0x00]))

		# Paramétrage par défaut de l'IMU
		# Valeur inscrite dans le registre CTRL1 : 0x57 = 0101 0111
		# - Les mesures sur les 3 axes sont actives : 111
		# - Mises à jour en continu des mesures d'accélération : 0
		# - Fréquence de l'accéléromètre mise à 50 Hz : 0101
		
		self.i2c.writeto_mem(self.address, CTRL1, bytearray([0x57]))

		# Valeur inscrite dans le registre CTRL2 : 0000 0000
		# - Accelerometer anti-alias filter bandwidth. : 773 Hz
		# - Sensisibilité de l'accéléromètre : +/- 2g
		# - Auto-test de l'accélération désactivé
		# - SPI interface : 4 wires (pas utilisé par notre module)
		self.i2c.writeto_mem(self.address, CTRL2, bytearray([0x00]))

		# Valeur inscrite dans le registre CTRL5 : 0x70 = 0111 0000
		# - Capteur de température désactivé : 0
		# - Résolution du capteur magnétique haute: 11
		# - Fréquence du capteur magnétique mise à 50 Hz : 100
		# - Interruptions non activées : 00
		self.i2c.writeto_mem(self.address, CTRL5, bytearray([0x70]))

		# Valeur inscrite dans le registre CTRL6 : 0000 0000
		# - Sensibilité du magnétomètre +/- 2 gauss : 00
		self.i2c.writeto_mem(self.address, CTRL6, bytearray([0x00]))

		# Valeur inscrite dans le registre CTRL7 : 0000 0000 
		# - High-pass filter mode selection for acceleration data : 00
		# - Filtered acceleration data selection bypassed : 0
		# - Temperature sensor is on while magnetic sensor is on : 0
		# - Mises à jour en continu des mesures magnétiques : 00
		self.i2c.writeto_mem(self.address, CTRL7, bytearray([0x00]))

	# Arrête l'accéléromètre
	def stop_acc(self):
		self.i2c.writeto_mem(self.address, CTRL1, bytearray([0x00]))
		self.acc_freq = 0
		print("Accéléromètre désactivé")

	# Arrête le magnétomètre
	def stop_mag(self):
		self.i2c.writeto_mem(self.address, CTRL5, bytearray([0x78]))
		self.mag_freq = 0
		print("Magnétomètre désactivé")

	# Renvoie les composantes "brutes" (non dimensionnées) du vecteur accélération
	def get_raw_acc(self):

		# Obtient la valeur de l'accélération (codée sur 16 bits en complément à deux)
		self.i2c.readfrom_mem_into(self.address,OUT_X_L_A | 0x80, self.six_bytes)
		raw_accel_data = struct.unpack('<hhh', self.six_bytes)

		acc_x = raw_accel_data[0]
		acc_y = raw_accel_data[1] 
		acc_z = raw_accel_data[2] 

		return (acc_x, acc_y, acc_z)

	# Renvoie les composantes dimensionnées du vecteur accélération (en g)
	def get_acc(self):
		
		raw_accel_data = self.get_raw_acc()
		
		if self.acc_range == 2: # amplitude +/- 2g
			acc_x = raw_accel_data[0] * ACC_02G
			acc_y = raw_accel_data[1] * ACC_02G
			acc_z = raw_accel_data[2] * ACC_02G
		elif self.acc_range == 4: # amplitude +/- 4g
			acc_x = raw_accel_data[0] * ACC_04G
			acc_y = raw_accel_data[1] * ACC_04G
			acc_z = raw_accel_data[2] * ACC_04G
		elif self.acc_range == 6: # amplitude +/- 6g
			acc_x = raw_accel_data[0] * ACC_06G
			acc_y = raw_accel_data[1] * ACC_06G
			acc_z = raw_accel_data[2] * ACC_06G
		elif self.acc_range == 8: # amplitude +/- 8g
			acc_x = raw_accel_data[0] * ACC_08G
			acc_y = raw_accel_data[1] * ACC_08G
			acc_z = raw_accel_data[2] * ACC_08G
		elif self.acc_range == 16: # amplitude +/- 16g
			acc_x = raw_accel_data[0] * ACC_16G
			acc_y = raw_accel_data[1] * ACC_16G
			acc_z = raw_accel_data[2] * ACC_16G

		return (acc_x, acc_y, acc_z)

	# Pour changer la fréquence de l'accéléromètre
	def set_acc_freq(self, value):
		if value in ACC_FRQ:
			# Arrête l'accéléromètre
			self.stop_acc()

			# Redémarre l'accéléromètre à la fréquence requise
			if value == 3.125:
				self.i2c.writeto_mem(self.address, CTRL1, bytearray([0x17]))
			elif value == 6.25:
				self.i2c.writeto_mem(self.address, CTRL1, bytearray([0x27]))
			elif value == 12.5:
				self.i2c.writeto_mem(self.address, CTRL1, bytearray([0x37]))
			elif value == 25:
				self.i2c.writeto_mem(self.address, CTRL1, bytearray([0x47]))
			elif value == 50:
				self.i2c.writeto_mem(self.address, CTRL1, bytearray([0x57]))
			elif value == 100:
				self.i2c.writeto_mem(self.address, CTRL1, bytearray([0x67]))
			elif value == 200:
				self.i2c.writeto_mem(self.address, CTRL1, bytearray([0x77]))
			elif value == 400:
				self.i2c.writeto_mem(self.address, CTRL1, bytearray([0x87]))
			elif value == 800:
				self.i2c.writeto_mem(self.address, CTRL1, bytearray([0x97]))
			elif value == 1600:
				self.i2c.writeto_mem(self.address, CTRL1, bytearray([0xA7]))
			self.acc_freq = value
			print("Fréquence de l'accéléromètre : +/- %.3f Hz" %value)
		else:
			print("Vous avez requis +/- %.3f Hz pour l'accéléromètre." %value)
			print("Les valeurs autorisées sont : ")
			for itm in ACC_FRQ:
				print(" +/- %.3f Hz" %itm)
			raise AttributeError("Erreur set_acc_freq")

	# Pour changer l'amplitude de l'accéléromètre
	def set_acc_range(self, value):
		if value in ACC_RNG:
			if value == 2:
				self.i2c.writeto_mem(self.address, CTRL2, bytearray([0x00]))
			elif value == 4:
				self.i2c.writeto_mem(self.address, CTRL2, bytearray([0x08]))
			elif value == 6:
				self.i2c.writeto_mem(self.address, CTRL2, bytearray([0x10]))
			elif value == 8:
				self.i2c.writeto_mem(self.address, CTRL2, bytearray([0x18]))
			elif value == 16:
				self.i2c.writeto_mem(self.address, CTRL2, bytearray([0x20]))
			self.acc_range = value
			print("Amplitude de l'accéléromètre : +/- %1d g" %value)
		else:
			print("Vous avez requis +/- %1d g pour l'accéléromètre." %value)
			print("Les valeurs autorisées sont : ")
			for itm in ACC_RNG:
				print(" +/- %1d g" %itm)
			raise AttributeError("Erreur set_acc_range")

	# Renvoie les composantes "brutes" (non dimensionnées) du vecteur champ magnétique
	def get_raw_mag(self):

		self.i2c.readfrom_mem_into(self.address, STATUS_M ,self.one_byte)

		# Masque sur le bit de poids faible du registre de statuts (valeur mise à jour ?)
		if int(self.one_byte[0] & 0b00000001):
			# Obtient la valeur du champ magnétique (codée sur 16 bits en complément à deux)
			self.i2c.readfrom_mem_into(self.address, OUT_X_L_M | 0x80, self.six_bytes)
			raw_mag_data = struct.unpack_from('<hhh', self.six_bytes)
			
			# Applique les corrections de calibrage
			mag_x = (raw_mag_data[0] - self.mag_offset[0]) * self.mag_scale[0]
			mag_y = (raw_mag_data[1] - self.mag_offset[1]) * self.mag_scale[1]
			mag_z = (raw_mag_data[2] - self.mag_offset[2]) * self.mag_scale[2]
		else:
			mag_x = float("NaN")
			mag_y = float("NaN")
			mag_z = float("NaN")

		return (mag_x, mag_y, mag_z)

	# Renvoie les composantes dimensionnées du vecteur champ magnétique (en µT)
	def get_mag(self):

		raw_mag_data = self.get_raw_mag()

		if self.mag_range == 2: # amplitude +/- 2 gauss
			mag_x = raw_mag_data[0] * MAG_02G
			mag_y = raw_mag_data[1] * MAG_02G
			mag_z = raw_mag_data[2] * MAG_02G
		elif self.mag_range == 4: # amplitude +/- 4 gauss
			mag_x = raw_mag_data[0] * MAG_04G
			mag_y = raw_mag_data[1] * MAG_04G
			mag_z = raw_mag_data[2] * MAG_04G
		elif self.mag_range == 8: # amplitude +/- 8 gauss
			mag_x = raw_mag_data[0] * MAG_08G
			mag_y = raw_mag_data[1] * MAG_08G
			mag_z = raw_mag_data[2] * MAG_08G
		elif self.mag_range == 12: # amplitude +/- 12 gauss
			mag_x = raw_mag_data[0] * MAG_12G
			mag_y = raw_mag_data[1] * MAG_12G
			mag_z = raw_mag_data[2] * MAG_12G

		return (mag_x, mag_y, mag_z)

	# Pour changer la fréquence du magnétomètre
	def set_mag_freq(self, value):
		if value in MAG_FRQ:
			
			# Arrête le magnétomètre
			self.stop_mag()
			
			# Redémarre le magnétomètre à la fréquence requise
			if value == 3.125:
				self.i2c.writeto_mem(self.address, CTRL5, bytearray([0x60]))
			elif value == 6.25:
				self.i2c.writeto_mem(self.address, CTRL5, bytearray([0x64]))
			elif value == 12.5:
				self.i2c.writeto_mem(self.address, CTRL5, bytearray([0x68]))
			elif value == 25:
				self.i2c.writeto_mem(self.address, CTRL5, bytearray([0x6C]))
			elif value == 50:
				self.i2c.writeto_mem(self.address, CTRL5, bytearray([0x70]))
			elif value == 100:
				if sef.acc_freq == 0 or sef.acc_freq > 50:
					self.i2c.writeto_mem(self.address, CTRL5, bytearray([0x74]))
				else:
					print("La fréquence du magnétomètre ne peut être fixée à 100 Hz que si l'accéléromètre est arrêté ou bien a une fréquence supérieure à 50 Hz.")
					raise AttributeError("Erreur set_mag_freq")
			self.mag_freq = value
			print("Fréquence du magnétomètre : +/- %.3f Hz" %value)
		else:
			print("Vous avez requis +/- %.3f Hz pour le magnétomètre." %value)
			print("Les valeurs autorisées sont : ")
			for itm in MAG_FRQ:
				print(" +/- %.3f Hz" %itm)
			raise AttributeError("Erreur set_mag_freq")

	# Pour changer l'amplitude du magnétomètre
	def set_mag_range(self, value):
		if value in MAG_RNG:
			if value == 2:
				self.i2c.writeto_mem(self.address, CTRL6, bytearray([0x00]))
			elif value == 4:
				self.i2c.writeto_mem(self.address, CTRL6, bytearray([0x20]))
			elif value == 8:
				self.i2c.writeto_mem(self.address, CTRL6, bytearray([0x40]))
			elif value == 12:
				self.i2c.writeto_mem(self.address, CTRL6, bytearray([0x60]))
			self.mag_range = value
			print("Amplitude du magnétomètre : +/- %1d gauss" %value)
		else:
			print("Vous avez requis +/- %1d Gauss pour le magnétomètre." %value)
			print("Les valeurs autorisées sont : ")
			for itm in MAG_RNG:
				print(" +/- %1d gauss" %itm)
			raise AttributeError("Erreur set_mag_range")
			
	# Calibre le magnétomètre
	# Cette fonction détermine les valeurs minimum et maximum des mesures 
	# de champ magnétique selon chaque axe, puis calcule les corrections
	# à apporter aux valeurs renvoyées par le magnétomètre.
	# La procédure nécessite d'imprimer au magnétomètre des mouvements dans
	# l'espace, en forme de "8" pendant deux minutes.
	
	def calibrate_mag(self):

		# Initialisation des valeurs extêmes pour le calibrage

		MAX_ITER = const(100) # Nombre d'itérations pour le calibrage
		DUMMY = const(32767)

		min_x = DUMMY  
		min_y = DUMMY
		min_z = DUMMY

		max_x = -DUMMY
		max_y = -DUMMY
		max_z = -DUMMY

		print("Démarrage du calibrage")

		for index in range (1, MAX_ITER):

			# Lecture du champ magnétique sur les trois axes orthogonaux
			raw_mag_data = self.get_raw_mag()
			
			x = raw_mag_data[0]
			y = raw_mag_data[1]
			z = raw_mag_data[2]

			# A chaque itération, on détermine les valeurs min et max du champ magnétique selon x,y et z

			min_x = min(min_x, x)
			min_y = min(min_y, y)
			min_z = min(min_z, z)

			max_x = max(max_x, x)
			max_y = max(max_y, y)
			max_z = max(max_z, z)

			sleep_ms(250)

		# Affichage sur le port série des valeurs extêmes pour le calibrage
		print("Fin calibrage")
		print("\n")
		print("Amplitudes relevées pour le calibrage :")
		print("\n")
		print("min_x : %5d, max_x : %5d" % (min_x, max_x))
		print("min_y : %5d, max_y : %5d" % (min_y, max_y))
		print("min_z : %5d, max_z : %5d" % (min_z, max_z))

		# Calcul des décalages (offsets) "Hard Iron" pour chaque axe :

		self.mag_offset = [(max_x + min_x)/2, (max_y + min_y)/2, (max_z + min_z)/2]

		# Calcul des coefficients pour la correction approximative des 
		# distorsions "Soft Iron" pour chaque axe :

		avg_delta_x = (max_x - min_x) / 2
		avg_delta_y = (max_y - min_y) / 2
		avg_delta_z = (max_z - min_z) / 2

		avg_delta = (avg_delta_x + avg_delta_y + avg_delta_z) / 3

		self.mag_scale = [avg_delta/avg_delta_x, avg_delta/avg_delta_y, avg_delta/avg_delta_z]

		print("Les constantes de calibrage sont :")
		print("\n")
		print("  OFFSET_X = %.1f" % self.mag_offset[0])
		print("  OFFSET_Y = %.1f" % self.mag_offset[1])
		print("  OFFSET_Z = %.1f" % self.mag_offset[2])
		print("\n")
		print("  SCALE_X = %.1f" % self.mag_scale[0])
		print("  SCALE_Y = %.1f" % self.mag_scale[1])
		print("  SCALE_Z = %.1f" % self.mag_scale[2])
