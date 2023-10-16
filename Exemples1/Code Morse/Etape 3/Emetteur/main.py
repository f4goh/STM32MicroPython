# Objet du code : 
# Emission d'un message codé en MORSE avec une LED infrarouge (IR).
# Etape 2 : Emission du message 'Hello World'
# Le commutateur du Grove Base Shield est placé sur 3.3V
# Source adaptée de :
# https://gitlab.com/olivierlenoir/MicroPython-MorseCode/-/blob/master/micropython/

# Quantum de temps pour le code Morse ; durée minimum (en millisecondes) qui sépare
# deux symboles. 
TICK = const(1000) # Une seconde

from pyb import Pin # Classe pour gérer les broches (GPIO)
# La LED IR est connectée à la broche D4
led = Pin('D4', Pin.OUT_PP)

# Instantiation de l'encodeur émetteur de code Morse
from morsecode import MorseEncode
morse = MorseEncode(led, tick = TICK)

# Affichage d'un en-tête dans le terminal série
print("\n" + "-" * 32)
print("Emetteur de code Morse")
print("-" * 32 + "\n")

# Envoi en boucle du message "Hello World" encodé en Morse
while True:
	morse.message('Hello World')
