# Objet du script : Mise en œuvre d'un afficheur 8x7 segments piloté par
# un contrôleur TM1638

# Importation des bibliothèques
import tm1638 # Pilotes de l'afficheur
from machine import Pin # Pilotes des entrées-sorties de la NUCLEO-WB55

# Déclaration de l'afficheur
tm = tm1638.TM1638(stb=Pin('D2'), clk=Pin('D3'), dio=Pin('D4'))

# Gestion des LED
tm.leds(0b01010101) # allume une LED sur 2
tm.leds(0b00000001) # allume la LED 1 et éteint les autres
tm.led(2, 0) # éteint la LED 3
tm.led(0,1) # allume la LED 1

# On récupère l'information sur les boutons
boutons = tm.keys()

# Segments
tm.show('  *--*  ')
tm.show('a.b.c.d.e.f.g.h.')

tm.number(-1234567)
tm.number(1234)

tm.scroll('Hello World')
tm.scroll('Bonjour tout le monde', 100)

# Change la luminosité des LED et segments
tm.brightness(0)

# Eteint les LED et les segments
tm.clear()

