# Objet du script : mise en œuvre d'un lecteur RFID 125 kHz de Grove
# Ce script est adapté du site https://gcworks.fr/tutoriel/esp/LecteurRFID125kHz.html

from pyb import UART # Classe pour gérer l'UART

uart = UART(2) # Instance de l'UART numéro 2

# Initialisation à 9600 bauds, trames de 8 bits, sans contrôle de parité avec un stop bit à 1
uart.init(9600, bits=8, parity = None, stop = 1)

# Nombre d'octets dans l'identifiant du TAG
_RFID_TAG_SIZE = const(10)

while True:
	
	# Lecture d'un tag RFID. 
	# Les données arrivent sur le port série et sont stockées dans un tableau d'octets

	# Lorsque tous les octets de l'identifiant du tag / badge RFID sont dans la file de réception
	if uart.any() > _RFID_TAG_SIZE: 
		
		# Charge les octets dans un tableau
		tag_data = uart.read()
		print("Donnees tag RFID :            ", tag_data.decode("ascii"))

		# On isole et on décode les 5 octets de poids faible du champ "10 ASCII Data Characters"
		rfid_hexa = ""
		for i in range(5, 11):
			rfid_hexa += chr(tag_data[i])
		print("Identifiant RFID en hexa :    ", rfid_hexa)

		# L'identifiant RFID indiqué sur le tag est obtenu par conversion hexadecimal -> décimal
		rfid = str(int(rfid_hexa, 16))
		while len(rfid)< _RFID_TAG_SIZE:
			rfid = "0" + rfid
		print("Identifiant RFID en decimal : %s \n" %rfid)