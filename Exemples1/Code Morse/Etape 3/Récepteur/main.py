# Objet du code : 
# Réception d'un message codé en MORSE avec une photodiode.
# Source adaptée de :
# https://gitlab.com/olivierlenoir/MicroPython-MorseCode/-/blob/master/micropython/

from micropython import schedule, alloc_emergency_exception_buf # Voir explications dans le script
from pyb import ADC, Pin, Timer # Accès aux ADC, aux GPIO et aux timers

# Quantum de temps pour le code Morse : durée minimum (en millisecondes) qui sépare
# deux symboles. Attention, cette valeur doit être la même dans le script de l'émetteur !
TICK = const(1000)

# Fréquence du timer à l'écoute des impulsions IR : 1 Hz
FREQ = const(1) 

# Seuil de détection pour le signal analogique.
# Au-dessus de cette valeur, l'impulsion IR reçue est considérée comme "haute" (1)
# Au-dessous de cette valeur, l'impulsion IR reçue est considérée comme "basse" (0)
LIGHT_THRES = const(2000)

# Instanciation et démarrage du convertisseur analogique-numérique sur la broche A0
adc = ADC(Pin('A0'))

# Tableau tampon pour assurer une remontée correcte des messages d'erreurs lorsque
# celles-ci surviennent dans la routine de service d'une interruption.
alloc_emergency_exception_buf(100)

# Variables globales pour le décodage "à la volée" du message en Morse
nb_low = 0 # Décompte des impulsions IR "basses" reçues consécutivement
nb_high = 0 # Décompte des impulsions IR "hautes" reçues consécutivement
symbol= '' # Dernier symbole du message Morse reçu (aucun)
append = False # Doit-on ajouter un symbole reçu au message en Morse en cours de réception ?
decode = False # Dispose-t-on d'un mot complet prêt à être traduit ?
morse_message = [] # Liste des symbolesconstituant un mot complet, dans leur ordre de réception

# Routine de service de l'interruption (ISR) de dépassement de compteur du timer 1.
# Cette ISR reçoit les impulsions infrarouge et les traduit en symboles '.', '-' et ' '.

@micropython.native # Directive pour optimiser le bytecode
def listen(timer):

	# Accès aux variables globales
	global nb_low, nb_high
	global symbol, decode, append

	# Suspend la lecture des impulsions jusqu'à ce que la coroutine "decode_task"
	# ait terminé son travail
	while append or decode:
		pass

	# Lecture de l'impulsion IR reçue et numérisation de celle-ci avec l'ADC puis
	# comparaison de la valeur avec le LIGHT_THRES fixé.
	if adc.read() < LIGHT_THRES: # Si la valeur numérisée est inférieure au seuil ...

		nb_low += 1 # On compte une impulsion basse supplémentaire
		
		# Si on avait compté 1 impulsion(s) haute(s) consécutive(s) jusqu'à présent...
		if nb_high == 1:
			symbol = '.' # Alors le dernier symbole Morse transmis était un '.'
			append = True # On peut ajouter ce '.' à la liste des symboles reçus
#			print('.', end='')

		# Si on avait compté 3 impulsions hautes consécutives jusqu'à présent...
		elif nb_high == 3:
			symbol = '-' # Alors le dernier symbole Morse transmis était un '-'
			append = True # On peut ajouter ce '-' à la liste des symboles reçus
#			print('-', end='')

		 # On vient de reçevoir une impulsion basse, donc le décompte des impulsions hautes
		 # consécutives et remis à zéro
		nb_high = 0
	
	else: # Si la valeur numérisée est supérieure au seuil ...
	
		nb_high += 1 # On compte une impulsion haute supplémentaire

		# Si on avait compté 3 impulsions basses consécutives jusqu'à présent...
		if nb_low == 3:
			symbol = ' ' # Alors le dernier symbole Morse transmis était un ' ' (séparateur de caractères)
			append = True # On peut ajouter ce ' ' à la liste des symboles reçus
#			print(' ', end='')

		# Si on avait compté 9 impulsions basses consécutives jusqu'à présent...
		elif nb_low == 9:
			# Alors le dernier symbole reçu est un espace long ; on a reçu un mot complet !
			decode = True # On peut lancer la traduction du mot reçu.

		 # On vient de reçevoir une impulsion haute, donc le décompte des impulsions basses
		 # consécutives et remis à zéro
		nb_low = 0

# Démarre le timer 1 à la fréquence de FREQ Hz.
tim1 = Timer(1, freq = FREQ)

# Assigne la fonction "listen" à l'interruption de dépassement de compteur du timer 1.
tim1.callback(listen)

# Instantiation du décodeur de code Morse
from morsecode import MorseDecode
morse = MorseDecode()

import uasyncio # Pour l'exécution asynchrone

# Procède au décodage de msg écrit en code Morse vers l'alphabet latin
@micropython.native # Directive pour optimiser le bytecode
def morse_to_latin(msg):
	print(morse.decode(msg))

# Coroutine / tache (asynchrone) de décodage des mots reçus depuis le code Morse vers
# l'alphabet latin.

@micropython.native # Directive pour optimiser le bytecode
async def decode_task():

	DELAY = TICK // 10 # Pour temporiser ...

	# Accès aux variables globales
	global symbol, decode, append

	while True:

		if append: # Si on a reçu un nouveau symbole ...

			morse_message.append(symbol) # Ajoute le symbole à ceux déjà reçus
			append = False # Signale à l'ISR "listen" que le travail est fait

		elif decode: # Si on a reçu tous les symboles d'un mot complet ...

			msg = ''.join(morse_message) # Sauvegarde le mot
			morse_message.clear() # Vide la liste des symboles reçus
			decode = False # Signale à l'ISR "listen" que le travail est fait

			# Procède au décodage du mot en alphabet latin "dès que possible"
			schedule(morse_to_latin, msg)

		await uasyncio.sleep_ms(DELAY)

# Affichage d'un en-tête dans le terminal série
print("\n" + "-" * 32)
print("Récepteur de code Morse")
print("-" * 32 + "\n")

# Appel au planificateur qui lance l'exécution asynchrone de la fonction decode_task 
uasyncio.run(decode_task())