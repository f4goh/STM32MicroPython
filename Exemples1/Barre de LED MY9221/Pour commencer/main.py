# Objet du script : mise en œuvre de la barre de LED GROVE MY9221 avec MicroPython
# Cet exemple est une simple copie (et traduction) de  la ressource se trouvant ici :
# https://github.com/mcauser/micropython-my9221
# Matériel : une carte NUCLEO-WB55, un Grove Base Shield et un module Grove LED Bar V2.0.
# Le module est branché sur le connecteur D4 du Grove Base Shield.
 
from machine import Pin # Pour piloter les broches
from my9221 import MY9221 # Pour piloter la barre de LED

# Instanciation de la barre de LED
# Attention de bien modifier les références des broches si vous le connectez
# ailleurs sur le Grove Base Shield !
ledbar = MY9221(Pin('D4'), Pin('D5'))

# Toutes les LED son allumées, avec une luminosité maximum
ledbar.level(10)

# Quatre LED allumées, à demi-luminosité
ledbar.level(4, 0x0F)

# Orientation inversée, la première LED est verte
ledbar.reverse(True)
ledbar.level(1)

# Orientation normale, la première LED est rouge
ledbar.reverse(False)
ledbar.level(1)

# N'allume que certaines LED
ledbar.bits(0b1111100000) # masque binaire, les 5 dernières lED sont allumées
ledbar.bits(0b0000011111) # masque binaire, les 5 premières lED sont allumées
ledbar.bits(1) # Soit 0b0000000001 => seule la première LED est allumée
ledbar.bits(3) # Soit 0b0000000011 => seules les 2 premières LED son allumées
ledbar.bits(7) # Soit 0b0000000111 => seules les 3 premières LED son allumées

# La première et la dernière LED sont allumées, très faiblement
ledbar.bits(513, 7) # car 513 = 0b1000000001

# Allume les LED impaires, puis les LED paires
for i in range(50):
	ledbar.bits(0b0101010101)
	ledbar.bits(0b1010101010)
	buf = b'\x00\xff\x00\xff\x00\xff\x00\xff\x00\xff'
	ledbar.bytes(buf)

# Simule un effet de dégradé
for i in range(50):
	buf = bytearray([0,1,3,7,15,31,63,127,255,255])
	ledbar.reverse(True)
	ledbar.bytes(buf)
	ledbar.reverse(False)
	ledbar.bytes(buf)

# Différentes luminosités
from time import sleep_ms
buf = [0,0,0,0,0,255,127,63,15,7]
ledbar.bytes(buf)
sleep_ms(1000)

# Bandeau de LED cyclique, avec luminosité variable
buf = [0,1,3,7,15,31,63,127,255,255]
for i in range(0):
    buf.insert(0,buf.pop())
    ledbar.bytes(buf)
    sleep_ms(100)

# Allume les LED suivant une séquence aléatoire
import urandom
for i in range(100):
    ledbar.bits(urandom.getrandbits(10))

# Examine toutes les combinaisons d'éclairage possibles
for i in range(1024):
    ledbar.bits(i)

# Affichage en niveaux de gris, codés sur 8 bits (par défaut)
# Luminosité 0x00-0xFF
ledbar._write16(0x00) # commande
ledbar._write16(0xFF) # led 1
ledbar._write16(0xFF) # led 2
ledbar._write16(0x00) # led 3
ledbar._write16(0x00) # led 4
ledbar._write16(0x00) # led 5
ledbar._write16(0xFF) # led 6
ledbar._write16(0xFF) # led 7
ledbar._write16(0x00) # led 8
ledbar._write16(0x00) # led 9
ledbar._write16(0x00) # led 10
ledbar._write16(0x00) # canal inutilisé, requis
ledbar._write16(0x00) # canal inutilisé, requis
ledbar._latch()

# Affichage en niveaux de gris, codés sur 12 bits
# Luminosité 0x000-0xFFF
ledbar._write16(0x0100) # commande
ledbar._write16(0x0FFF) # led 1
ledbar._write16(0x0000) # led 2
ledbar._write16(0x00FF) # led 3
ledbar._write16(0x0000) # led 4
ledbar._write16(0x000F) # led 5
ledbar._write16(0x000F) # led 6
ledbar._write16(0x0000) # led 7
ledbar._write16(0x00FF) # led 8
ledbar._write16(0x0000) # led 9
ledbar._write16(0x0FFF) # led 10
ledbar._write16(0x0000) # canal inutilisé, requis
ledbar._write16(0x0000) # canal inutilisé, requis
ledbar._latch()

# Affichage en niveaux de gris, codés sur 14 bits
# Luminisoté 0x000-0x3FFF
ledbar._write16(0x0200) # commande
ledbar._write16(0x3FFF) # led 1
ledbar._write16(0x03FF) # led 2
ledbar._write16(0x0000) # led 3
ledbar._write16(0x0000) # led 4
ledbar._write16(0x0000) # led 5
ledbar._write16(0x003F) # led 6
ledbar._write16(0x0003) # led 7
ledbar._write16(0x0000) # led 8
ledbar._write16(0x0000) # led 9
ledbar._write16(0x0000) # led 10
ledbar._write16(0x0000) # canal inutilisé, requis
ledbar._write16(0x0000) # canal inutilisé, requis
ledbar._latch()

# Affichage en niveaux de gris, codés sur 16 bits
# Luminosité 0x0000-0xFFFF
ledbar._write16(0x0300) # commande
ledbar._write16(0xFFFF) # led 1
ledbar._write16(0x0FFF) # led 2
ledbar._write16(0x00FF) # led 3
ledbar._write16(0x000F) # led 4
ledbar._write16(0x0007) # led 5
ledbar._write16(0x0003) # led 6
ledbar._write16(0x0001) # led 7
ledbar._write16(0x0000) # led 8
ledbar._write16(0x0000) # led 9
ledbar._write16(0x0000) # led 10
ledbar._write16(0x0000) # canal inutilisé, requis
ledbar._write16(0x0000) # canal inutilisé, requis
ledbar._latch()