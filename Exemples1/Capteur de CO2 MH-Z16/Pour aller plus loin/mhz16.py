# Pilote du module Grove capteur de CO2 MH-Z16
# Ce script est adapté du forum :
# https://forum.pycom.io/topic/4821/solved-uart-and-mh-z16-co2-sensor/13
# Fiche technique du capteur :
# https://www.winsen-sensor.com/d/files/MH-Z16.pdf

from time import sleep_ms

# Taille de la réponse du capteur, en octets 
_NB_BYTES = const(9)

# Séquence d'octets pour lancer une mesure
_CMD_MEASURE = b'\xFF\x01\x86\x00\x00\x00\x00\x00\x79'

# Séquence d'octets pour calibrer
_CMD_CALIBRATE =  b'\xFF\x87\x87\x00\x00\x00\x00\x00\xF2'

class MHZ16:

	def __init__(self, uart, temp_offset = 0, co2_offset = 0):
		self._uart = uart
		self._temp_offset = temp_offset
		self._co2_offset = co2_offset

	def preheat(self):
		p = 0
		for i in range(300):
			# Lance une mesure
			self._uart.write(_CMD_MEASURE)
			# Pause d'une seconde
			sleep_ms(1000)
			p += 1
			if p == 60:
				p = 0
 
	def calibrate(self):
		self._uart.write(_CMD_CALIBRATE)

	def measure(self):
		
		try:
			# Lance une mesure
			self._uart.write(_CMD_MEASURE)
			sleep_ms(10)

			# Attends d'avoir reçu la réponse (9 caractères)
			while self._uart.any() < _NB_BYTES:
				sleep_ms(1)

			# Lis la réponse
			resp = bytearray(self._uart.read(_NB_BYTES))

			# Extrait la température et la concentration de CO2 de la réponse 
			co2_ppm = (resp[2] * 256 + resp[3]) + self._co2_offset
			temp_celsius = (resp[4] - 40) + self._temp_offset
			return(temp_celsius, co2_ppm)
		except:
			return(-1, -1)