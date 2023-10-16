from pyb import UART
from time import sleep_ms

class US100:

	def distance_mm(self):
		# Initialisation communication avec le capteur
		uart = UART(2)
		uart.init(9600, bits=8, parity=None, stop=1)
		sleep_ms(1)
		uart.write(b'\x55')
		
		t = 0
		buf = bytearray(2)
		
		# Attente d'un caractère à lire sur la liaison série
		while not uart.any() and t < 1000:
			t = t + 1
			sleep_ms(5)
			
		#Lecture du caractère
		if t < 1000:
			uart.readinto(buf, 2)
			
		# Lecture et renvoie de la distance	
		dist = buf[0] * 256 + buf[1]
		if dist > 11000:
			dist = -1 # objet trop loin ou erreur de détection
		return dist
