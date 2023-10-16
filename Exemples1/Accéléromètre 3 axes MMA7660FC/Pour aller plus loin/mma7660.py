# Classe qui implémente le pilote de l'accélèromètre 3 axes MMA7660FC (+/- 1.5g)
# Fonctions du registre TILT ajoutées à partir des explications :
# - De l'ouvrage "MicroPython et Pyboard - Python sur microcontrôleur : 
#   de la prise en main à l'utilisation avancée".
#   Auteur : Dominique Meurisse, ISBN-10 : 2409022901, ISBN-13 :‎ 978-2409022906
# - Des exemples fournis par Frédéric Boulanger, CentraleSupélec - Département Informatique
#   https://github.com/Frederic-soft/pyboard/blob/master/MMA7660/MMA7660.py

_DEVICE_ADDRESS = const(0x4C) # Adresse de l'accéléromètre sur le bus I2C

# Adresse du registre de sortie exposant les 3 octets contenant les accélérations
#  Accélération selon x : adresse = 0
#  Accélération selon y : adresse = 1
#  Accélération selon z : adresse = 2
_OUTPUT_REG = const(0)

# Adresse du registre de détection de conditions particulières
_TILT_REG = const(3)

# Adresse du registre de paramétrage des interruptions de l'accéléromètre
_INTSU_REG = const(6)

# Paramètres pour le registre INTSU
# Active toutes les interruptions
_INT_SET = b'\xFF'

# Adresse du registre permettant de fixer la fréquence d'échantillonnage
_SR_REG = const(8)

# Paramètres pour le registre SR
# Fréquence de mesure / échantillonnage (en nb par seconde)
#_SRATE1 = b'\x07'
#_SRATE2 = b'\x06'
#_SRATE4 = b'\x05'
#_SRATE8 = b'\x04'
#_SRATE16 = b'\x03'
#_SRATE32 = b'\x02'
#_SRATE64 = b'\x01'
_SRATE120 = b'\x00'

# Adresse du registre de sélection du mode
_SM_REG = const(7)

# Paramètres pour le registre SM
_STANDBY = b'\x00' # Mode "standby"
_ACTIVE = b'\x01' # Mode "actif"

# Adresse du registre des paramètres des taps
_PDET_REG = const(9)

# Paramètres le registre PDET
# Détection des taps sur les 3 axes (bits [7-5] à 0)
# Anti-rebond  : on filtre 20 oscillations, soit 0x14 (bits [4-0]) (valeur possible de 1 à 31)
_TAPS_BEBOUNCE = b'\x14'

# Adresse du registre de filtrage de la détection des taps
_PD_REG = const(10)

# Paramètre pour le registre PD
# Délai de détection des taps, agrège jusqu'à 31 taps consécutifs
_TAPS_FUSE = b'\x1F'

# Facteur de conversion entre les valeurs lues dans les registres et l'accélération physique
# exprimée en g.
_RAW_TO_G = 0.047

class MMA7660():

	def __init__(self, i2c, addr = _DEVICE_ADDRESS, srate = _SRATE120):
		self.i2c = i2c
		self.i2c.scan()
		self.address = addr 
		# Tableau "tampon" d'octets pour récupérer les valeurs du registre de sortie de 
		# l'accéléromètre
		self.databuf = bytearray(3)
		# Tableau contenant les valeurs dimensionnées des accélérations suivant les trois axes
		self.data = [0,0,0]
		# On place l'accéléromètre est en mode "standby"
		self.stop()

		# On active les interruptions
		self.i2c.writeto_mem(self.address, _INTSU_REG, _INT_SET)
		# On fixe sa fréquence de mesures
		self.i2c.writeto_mem(self.address, _SR_REG, srate)
		# On fixe les paramètres de la détection des "taps"
		self.i2c.writeto_mem(self.address, _PDET_REG, _TAPS_BEBOUNCE)
		self.i2c.writeto_mem(self.address, _PD_REG, _TAPS_FUSE)

	# Méthode pour démarrer l'accéléromètre
	def start(self):
		self.i2c.writeto_mem(self.address, _SM_REG, _ACTIVE)

	# Méthode pour arrêter l'accéléromètre
	def stop(self):
		self.i2c.writeto_mem(self.address, _SM_REG, _STANDBY)

	# Méthode pour changer la fréquence de mesures
	def setSamplingRate(self, rate):
		# Passe en mode "standby"
		self.stop()
		# Programme la fréquence d'échantillonnage (seize mesures par seconde)
		self.i2c.writeto_mem(self.address, _SR_REG, rate)
		# Passe en mode "actif" 
		self.start()

	# Méthode pour obtenir les mesures d'accélération
	def get(self):
		self.databuf = self.i2c.readfrom_mem(self.address, _OUTPUT_REG, 3) # Lecture des données

		# Pour l'accélération selon l'axe x
		ax = self.databuf[0] & 0x3F # Complément à deux
		if ax > 31:
			ax = ax - 64
		self.data[0] = ax * _RAW_TO_G # Conversion en g

		# Pour l'accélération selon l'axe y
		ay = self.databuf[1] & 0x3F
		if ay > 31:
			ay = ay - 64
		self.data[1] = ay * _RAW_TO_G

		# Pour l'accélération selon l'axe z
		az = self.databuf[2] & 0x3F
		if az > 31:
			az = az - 64
		self.data[2] = az * _RAW_TO_G

		return tuple(self.data)

	# Méthode pour temporiser jusqu'à la mise à jour du registre TILT
	def _read_tilt_reg(self):
		# Lecture du registre (un octet)
		reg_content = self.i2c.readfrom_mem(self.address, _TILT_REG, 1)

		# Si le registre n'était pas en cours de mise à jour (bit numéro 6 égal à "1")
		if not (reg_content[0] & (1<<6)):
			return reg_content[0]
		else:
			return 0

	# Méthode pour déterminer si l'accéléromètre est secoué
	# Retourne :
	#  1 si l'accéléromètre est secoué 
	#  0 sinon
	def shake(self):
		val = self._read_tilt_reg() & (1<<7)
		if val:
			return 1
		else:
			return 0

	# Méthode pour déterminer si l'accéléromètre est tapoté
	# Retourne :
	#  1 si l'accéléromètre est tapoté 
	#  0 sinon
	def tap(self):
		val = self._read_tilt_reg() & (1<<5)
		if val:
			return 1
		else:
			return 0

	# Méthode pour déterminer si l'accélèromètre et posé côté pile ou côté face
	# Retourne :
	#  0 si l'accélèromètre est tourné côté "FACE"
	#  1 si l'accélèromètre est tourné côté "PILE"
	#  -1 si état indéterminé
	def facing(self):
		val = self._read_tilt_reg() & 0b11 
		if val == 1:
			return 0
		elif val == 2:
			return 1
		else:
			return -1 

	# Méthode pour détemrminer le mode portrait/paysage
	# Retourne :
	#  1 si mode paysage, vers la gauche
	#  2 si mode paysage, vers la droite
	#  5 si position verticale inversée
	#  6 si position verticale normale
	def orientation(self):
		return ( self._read_tilt_reg() & 0b11100 ) >> 2
