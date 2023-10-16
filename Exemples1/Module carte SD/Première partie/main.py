#Source : https://github.com/micropython/micropython/tree/master/drivers
# Objet du script : Présenter les fonctions de lecture et écriture offertes par sdcard.py.

#Broches Arduino utilisées pour le SPI
# MOSI : D11
# MISO : D12
# SCK : D13
# CS : D9
# Module SD utilisé : MH-SD Card Module alimentable en 3.3V 
# Attention : les modules µSD Catalex ne semblent pas fonctionner avec sdcard.py !
 
import sdcard, os
from pyb import SPI

spi = SPI(1, SPI.MASTER, baudrate=100000, polarity=1, phase=0) # Instance du bus SPI
sd = sdcard.SDCard(spi, machine.Pin('D9')) # Broche de sélection du module carte SD

vfs = os.VfsFat(sd) # Déclaration d'un système de fichier FAT
os.mount(vfs, "/fc") # Montage du volume logique associé au module carte SD

print("Liste des fichiers présents sur la carte SD (test du système de fichiers)")
print(os.listdir("/fc"))

letters = "abcdefghijklmnopqrstuvwxyz\n"
more_letters = letters * 200 # 5400 caractères
numbers = "1234567890\n"

fn = "/fc/fichier1.txt"
print()

print("Lecture / écriture de plusieurs blocs")
with open(fn, "w") as f:
	n = f.write(more_letters)
	print(n, "octets écrits")
	n = f.write(numbers)
	print(n, "octets écrits")
	n = f.write(more_letters)
	print(n, "octets écrits")

with open(fn, "r") as f:
	result1 = f.read()
	print(len(result1), "octets lus")

fn = "/fc/fichier2.txt"
print()
print("Lecture/écriture d'un seul block")
with open(fn, "w") as f:
	n = f.write(numbers)  # un seul block
	print(n, "octets écrits")

with open(fn, "r") as f:
	result2 = f.read()
	print(len(result2), "octets lus")

os.umount("/fc")

print()
print("Contrôle des données écrites")
success = True

if result1 == "".join((more_letters, numbers, more_letters)):
	print("Grand fichier : OK")
else:
	print("Grand fichier : Echec")
	success = False
	
if result2 == numbers:
	print("Petit fichier : OK")
else:
	print("Petit fichier : Echec")
	success = False
print()
print("Tests", "réussis" if success else "échoués")
