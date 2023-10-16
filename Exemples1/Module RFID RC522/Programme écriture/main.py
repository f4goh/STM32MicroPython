# Objet du script : écrtiture sur un badge RFID

import pyb
import time
import mfrc522

#Initialisation du lecteur de badge
rdr = mfrc522.MFRC522('D13', 'D11', 'D12', 'D9', 'D10')		#SCK, MOSI, MISO, RST, SDA

print("\n--> Veuillez présenter un badge sur le lecteur")

while True:
	# Détecte la présence d'un badge
	(stat, tag_type) = rdr.request(rdr.REQIDL)
	if stat == rdr.OK:
		(stat, raw_uid) = rdr.anticoll()
		if stat == rdr.OK:
			print("\nBadge détecté !")
			# Authentification
			if rdr.select_tag(raw_uid) == rdr.OK:
				key = [0xFF, 0xFF, 0xFF, 0xFF, 0xFF, 0xFF]
				# Ecriture
				if rdr.auth(rdr.AUTHENT1A, 8, key, raw_uid) == rdr.OK:
					print("--> Ecriture en cours...")
					stat = rdr.write(8, b"\x00\x01\x02\x03\x04\x05\x06\x07\x08\x09\x0a\x0b\x0c\x0d\x0e\x0f") #valeur hexa
					if stat == rdr.OK:
						print("--> Ecriture terminée !")
					else:
						print("--> Impossible d'écrire sur la carte !")
				# Affichage
				print("Données en mémoire : %s" % rdr.read(8))
				# Arrêt
				rdr.stop_crypto1()
		else:
			print("Erreur badge")
	time.sleep_ms(500)
