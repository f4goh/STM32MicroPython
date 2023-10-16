# Objet du script :
# Capturer un signal analogique avec un ADC et extraire ses fréquences à l'aide
# d'une transformation de Fourieur discrète (DFT).
# Reçoit en entrée un signal analogique modulé en tension, généré par le DAC
# d'une NUCLEO-L476RG (le générateur de signal).
# Chaque fois que le signal en question change, notre analyseur recalcule le
# spectre de Fourier.
# La broche 'D2' est gérée en interruption, elle recevra les ordre de mesure
# de la part du générateur.
# Le code pour la DFT est celui de Peter Hinch :
#    https://github.com/peterhinch/micropython-fourier

# Bibliothèques 
from math import sqrt
from pyb import Pin
from time import sleep_ms

# Associe une interruption aux fronts montants de la broche 'D2'.
# Cette broche permettra de se synchroniser avec les recalculs du 
# générateur de signaux

TRIGGER_PIN = Pin('D2', Pin.IN, Pin.PULL_DOWN)

# Est-ce qu'un front montant a été détecté sur la broche 'D2' ?
TRIGGER = False

# Gestion de l'interruption de la broche 'D2'
def TRIGGER_PIN_ISR(pin):
	global TRIGGER
	TRIGGER = not TRIGGER

# Activation de l'interruption de la broche 'D2'
TRIGGER_PIN.irq(trigger = TRIGGER_PIN.IRQ_RISING, handler = TRIGGER_PIN_ISR)

# Obtient le deuxième élément d'un couple
@micropython.native 
def takeSecond(elem):
	return elem[1]

# Extrait les fréquences du signal connecté à l'ADC sur 'A0'
@micropython.native
def find_frequency():

	# Nombre maximum de fréquences à afficher
	MAX_PEAKS = const(26)

	# Classe DFT par Peter Hinch 
	from dftclass import DFTADC, FORWARD
	
	# Nombre de mesures réalisées par l'ADC
	# Attention : pour les besoins de la DFT, ce doit être
	# une puissance de 2 !
	NBSAMPLES = const(1024) 
	acq_time = 0.1 # Durée de l'acquisition
	
	freq = NBSAMPLES / acq_time
	print("Fréquence d'échantillonage (Hz) : ", freq)
	
	# Pour la conversion des index en fréquences dans la DFT
	index_to_freq = 1 / acq_time

	# Acquisition d'un échantillon du signal par l'ADC
	mydft = DFTADC(NBSAMPLES,'A0',timer = 1)

	# Calcul de la DFT, les valeurs sont dans 
	# mydft.re (partie réelle) et mydft.im (partie imaginaire).
	dft_time = mydft.run(FORWARD,acq_time)
	
	print('Temps de calcul de la DFT (µs) : ', dft_time)

	half_NBSAMPLES = NBSAMPLES//2
	
	# Liste pour collecter les couples (fréquence, amplitude) 
	freq_amp = []
	
	for i in range(1,half_NBSAMPLES):
	
		# Calcul des amplitudes de la DFT
		x = (mydft.re)[i]
		y = (mydft.im)[i]
		fft_norm = sqrt(x*x + y*y)

		# Crée une liste des couples (fréquence, amplitude) 
		freq_amp.append((i*index_to_freq, fft_norm))

	# Trie la liste des couples (fréquence, amplitude) dans l'odre descendant, par amplitudes
	freq_amp.sort(reverse=True, key=takeSecond)

	# Affiche les MAX_PEAKS principales fréquences, par amplitudes décroissantes
	for i in range(0, MAX_PEAKS):
		p = freq_amp[i]
		print(i+1, 'Freq (Hz) : ', round(p[0],1) , 'Ampl (AU) : ', round(p[1],1))

print("Attente d'un signal depuis l'analyseur")

# Boucle principale
while True:

	# Si un front montant est déte cté sur la broche 'D2' 
	if TRIGGER:

		print("Signal reçu, extraction des fréquences")

		# Extrait les fréquences du signal connecté à l'ADC sur 'A0'
		find_frequency()

		print('-' * 50)

		# Indique que le traitement est terminé
		TRIGGER = False
		

