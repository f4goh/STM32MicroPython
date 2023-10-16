# Objet du script :
# Capturer un signal analogique avec un ADC et extraire ses fréquences à l'aide
# d'une transformation de Fourieur discrète (DFT).
# Reçoit en entrée un signal analogique modulé en tension, généré par une
# photodiode éclairée avec une lampe fluo-compacte.
# Au lancement du script, notre analyseur recalcule spectre de Fourier
# du signal lumineux, qui devrait avoir une fondamentale à f = 100 Hz.
# Le code pour la DFT est celui de Peter Hinch :
#    https://github.com/peterhinch/micropython-fourier

# Bibliothèques
from math import sqrt
from pyb import Pin
from time import sleep_ms
 
# Obtient le deuxième élément d'un couple
@micropython.native 
def takeSecond(elem):
	return elem[1]

# Extrait les fréquences du signal connecté à l'ADC sur 'A0'
@micropython.native
def find_frequency():

	# Nombre maximum de fréquences à afficher
	MAX_PEAKS = const(5)

	# Classe DFT par Peter Hinch 
	from dftclass import DFTADC, FORWARD
	
	# Nombre de mesures réalisées par l'ADC
	# Attention : pour les besoins de la DFT, ce doit être
	# une puissance de 2 !
	NBSAMPLES = const(128) 
	acq_time = 0.1 # Durée de l'acquisition en secondes
	
	freq_samp = NBSAMPLES / acq_time
	print("Fréquence d'échantillonage (Hz) : ", freq_samp)
	
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

		# Crée une liste de couples (fréquence, amplitude) 
		freq_amp.append((i*index_to_freq, fft_norm))

	# Trie la liste des couples (fréquence, amplitude) dans l'odre des
	# amplitudes décroissantes.
	freq_amp.sort(reverse = True, key = takeSecond)

	# Affiche les MAX_PEAKS premières comosantes par amplitudes décroissantes.
	for i in range(0, MAX_PEAKS):
		p = freq_amp[i]
		print(i+1, 'Freq (Hz) : ', round(p[0],1) , 'Ampl (AU) : ', round(p[1],1))
	
	# Ligne de séparation (composée de 50 caractères '-')
	print('-' * 50)

# Boucle principale
while True:

	# Extrait les fréquences du signal connecté à l'ADC sur 'A0'
	find_frequency()

	# Temporisation de 5 secondes
	sleep_ms(5000)


