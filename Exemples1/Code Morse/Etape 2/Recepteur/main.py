# Objet du code : 
# Réception d'un message codé en MORSE avec une photodiode. 
# Etape 2 : On applique un seuil au signal analogique. Récéption contrôlée par un timer.
# Source adaptée de :
# https://gitlab.com/olivierlenoir/MicroPython-MorseCode/-/blob/master/micropython/

from micropython import alloc_emergency_exception_buf # Voir explications dans le script
from pyb import ADC, Pin, Timer # Accès aux ADC, aux GPIO et aux timers

# Quantum de temps pour le code Morse : durée minimum (en millisecondes) qui sépare
# deux symboles. Attention, cette valeur doit être la même dans le script de l'émetteur !
TICK = const(1000)

# Seuil de détection pour le signal analogique.
# Au-dessus de cette valeur, l'impulsion IR reçue est considérée comme "haute" ('1')
# Au-dessous de cette valeur, l'impulsion IR reçue est considérée comme "basse" ('0')
LIGHT_THRES = const(2000)

# Instanciation et démarrage du convertisseur analogique-numérique sur la broche A0
adc = ADC(Pin('A0'))

# Tableau tampon pour assurer une remontée correcte des messages d'erreurs lorsque
# celles-ci surviennent dans la routine de service d'une interruption.
alloc_emergency_exception_buf(100)

# Routine de service de l'interruption (ISR) de dépassement de compteur du timer 1.
# Cette ISR reçoit les impulsions infrarouge et les traduit en symboles '0' et '1' selon leur intensité

@micropython.native # Directive pour optimiser le bytecode
def listen(timer):

	# Lecture de l'impulsion IR reçue et numérisation de celle-ci avec l'ADC puis
	# comparaison de la valeur avec le LIGHT_THRES fixé.

	if adc.read() < LIGHT_THRES: # Si la valeur numérisée est inférieure au seuil ...
		print('0', end='') # Affiche un '0' (sans saut de ligne)

	else: # Si la valeur numérisée est supérieure au seuil ...
		print('1', end='') # Affiche un '1' (sans saut de ligne)

# Fréquence du timer à l'écoute des impulsions IR : 1 Hz
FREQ = const(1) 

# Démarre le timer 1 à la fréquence de FREQ Hz.
tim1 = Timer(1, freq = FREQ)

# Assigne la fonction "ecoute" à l'interruption de dépassement de compteur du timer 1.
tim1.callback(listen)

# Affichage d'un en-tête dans le terminal série
print("\n" + "-" * 32)
print("Récepteur de code Morse")
print("-" * 32 + "\n")