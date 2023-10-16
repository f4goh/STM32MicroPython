# Objet du script : Mesure de température toutes les secondes.
# Affiche les valeurs mesurées sur le port série de l'USB user
# Cet exemple nécessite un Grove Base Shield et un capteur de température DS18X20 connecté sur A0
# Source : https://github.com/micropython/micropython

from time import sleep_ms
import machine
import onewire # Bibliothèque pour le protocole OneWire
import ds18x20 # Bibliothèque pour le capteur de température DS18X20

# On a connecté notre capteur à la broche A0
dat = machine.Pin('A0')

# Crée un objet "OneWire" (instance du protocole OneWire)
onew = onewire.OneWire(dat)

# Connecte la sonde à cette instance
ds = ds18x20.DS18X20(onew)

# Recherche des périphériques sur le bus OneWire
roms = ds.scan()
print('Périphériques trouvés:', roms)

# Effectue 20 mesures de température consécutives
for i in range(20):
	print('Température (degrés Celsius) :', end=' ')
	ds.convert_temp()
	sleep_ms(1000)
	# Pour tous les objets connectés au OneWire
	for rom in roms: 
		temp = round(ds.read_temp(rom),1)
		print(temp, end=' ')
	# Imprime une ligne blanche 
	print("\n")