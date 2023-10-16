# Code adapté de :
# https://gitlab.com/olivierlenoir/MicroPython-MorseCode/-/tree/master/
# Author: Olivier Lenoir - <olivier.len02@gmail.com>
# Created: 2021-03-24
# License: MIT, Copyright (c) 2021 Olivier Lenoir
# Language: MicroPython V1.14
# Project: Morse Code
# Link: https://morsecode.world/international/morse.html

from utime import sleep_ms

# Le code Morse international
# 1 - La durée d'un point (.) est 1 tick.
# 2 - La durée d'un tiret (-) est 3 ticks.
# 3 - La durée séparant les . ou les - dans un caractère est 1 tick.
# 4 - La durée séparant deux caractères consécutifs d'un mot est 3 ticks
# 5 - La durée séparant deux mots est 9 ticks

# Dictionnaire pour l'encodage
_MORSE_CODE = {
	'A': '.-',
	'B': '-...',
	'C': '-.-.',
	'D': '-..',
	'E': '.',
	'F': '..-.',
	'G': '--.',
	'H': '....',
	'I': '..',
	'J': '.---',
	'K': '-.-',
	'L': '.-..',
	'M': '--',
	'N': '-.',
	'O': '---',
	'P': '.--.',
	'Q': '--.-',
	'R': '.-.',
	'S': '...',
	'T': '-',
	'U': '..-',
	'V': '...-',
	'W': '.--',
	'X': '-..-',
	'Y': '-.--',
	'Z': '--..',
	'1': '.----',
	'2': '..---',
	'3': '...--',
	'4': '....-',
	'5': '.....',
	'6': '-....',
	'7': '--...',
	'8': '---..',
	'9': '----.',
	'0': '-----',
	'&': '.-...',
	"'": '.----.',
	'@': '.--.-.',
	'(': '-.--.',
	')': '-.--.-',
	':': '---...',
	',': '--..--',
	'=': '-...-',
	'!': '-.-.--',
	'.': '.-.-.-',
	'-': '-....-',
	'+': '.-.-.',
	'_': '...-.',
	'"': '.-..-.',
	'?': '..--..',
	'/': '-..-.',
	}


# Quatum de temps (tick) par défaut (une seconde)
_TICK = const(1000)

@micropython.native
# Décodage d'un message écrit en code Morse 
class MorseDecode(object):

	# Initialisations
	def __init__(self):
		# Construit le dictionnaire pour le décodage
		self.morse_decode = {v: k for k, v in _MORSE_CODE.items()}

	# Décode un message en Morse (une séquence de '.', de '-' et d'espaces)
	def decode(self, morse_code):
		msg = ''
		for dd in morse_code.split():
			msg += self.morse_decode.get(dd, '#')
		return msg

@micropython.native
# Encodage d'un message en code Morse vers un message alphabétique
class MorseEncode(object):

	# Initialisations
	def __init__(self, signal_pin, tick = _TICK):
		self.signal = signal_pin # Broche de du périphérique émetteur
		self.signal(0) # Eteint le périphérique émetteur
		self.tick = tick # quantum de temps ('tick')

	# Envoie un message en Morse
	def message(self, msg):
		# On passe les lettres en majucules, on sépare les mots, on les parcours un par un :
		for word in msg.upper().split():
			self._word(word) # Encode le mot en Morse & émet le signal correspondant
			self.space() # Ajoute un espace en fin de mot et de message

	# Encodage d'un mot en Morse
	def _word(self, word):
		# Pour chacun de ses caractères ...
		for char in word:
			print(char, end=' ')
			# Retrouve le code Morse du caractère, procède à son émission 
			self._char(_MORSE_CODE.get(char, '#'))

	# Encodage puis émission d'un caractère en Morse
	def _char(self, morse_code):
		# Parcours les tiret (-) et les points (.) qui composent le caractère
		for dd in morse_code:
			if dd == '.': # Si c'est un point ...
				self.dot() # Emission d'un point (.)
			elif dd == '-': # Si c'est un tiret ...
				self.dash() # Emission d'un tiret (-)
			else: # Si ce n'est ni un '.' ni un '-', ne fais rien
				pass
		print()
		sleep_ms(self.tick * 2) # On attend 2 ticks dans l'état "bas"


	# Emission d'un point (.)
	def dot(self):
		print('.', end='') # Affiche un '.' dans le terminal
		self.signal(1) # On allume le périphérique émetteur (état "haut")
		sleep_ms(self.tick * 1) # Un point correspond à un état "haut" pendant 1 tick
		self.signal(0) # On éteint le périphérique émetteur (état "bas")
		sleep_ms(self.tick) # On attend 1 tick dans l'état "bas"

	# Emission d'un tiret (-)
	def dash(self):
		print('-', end='') # Affiche un '-' dans le terminal
		self.signal(1) # On allume le périphérique émetteur (état "haut")
		sleep_ms(self.tick * 3) # Un tiret correspond à un état "haut" pendant 3 ticks
		self.signal(0) # On éteint le périphérique émetteur (état "bas")
		sleep_ms(self.tick) # On attend 1 tick dans l'état "bas"

	# Emission d'un espace (entre deux mots)
	def space(self):
		print() # Affiche une ligne vide dans le terminal
		sleep_ms(self.tick * 6) # Un espace est codé avec un état "bas" pendant 6 ticks