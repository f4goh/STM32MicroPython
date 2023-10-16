# Objet du script : lecture d'un badge RFID

import pyb
import time
import mfrc522

#Initialisation du lecteur de badge
rdr = mfrc522.MFRC522('D13', 'D11', 'D12', 'D9', 'D10') # SCK, MOSI, MISO, RST, SDA

print("\n --> Veuillez présenter un badge sur le lecteur")

while True:
	(stat, tag_type) = rdr.request(rdr.REQIDL) # Détecte la présence d'un badge
	if stat == rdr.OK:
		(stat, raw_uid) = rdr.anticoll()
		if stat == rdr.OK:
			# Affichage type de badge et UID
			print("\nBadge détecté !")
			print(" - type : %03d" % tag_type)
			print(" - uid : %03d.%03d.%03d.%03d" % (raw_uid[0], raw_uid[1], raw_uid[2], raw_uid[3]))
			# Affichage données en mémoire
			if rdr.select_tag(raw_uid) == rdr.OK:
				key = [0xFF, 0xFF, 0xFF, 0xFF, 0xFF, 0xFF]
				if rdr.auth(rdr.AUTHENT1A, 8, key, raw_uid) == rdr.OK:
					print(" - données : %s" % rdr.read(8))
					rdr.stop_crypto1()
				# Affichage en cas de problème
				else:
					print("Erreur de lecture")
			else:
				print("Erreur badge")
