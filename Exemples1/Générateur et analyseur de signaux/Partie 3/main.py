# Objet du script :
# Générer un signal rectangulaire à l'aide de sa série de Fourier avec le DAC d'une
# carte NUCLEO-L476RG, en lui ajoutant progressivement des termes (fondamentale, harmoniques).
# On commence avec le terme du premier ordre de (une fonction sinus) et, à chaque appui 
# sur le bouton utilisateur (bleu), on lui ajoute un terme d'ordre supérieur.
# On peut ainsi voir évoluer, avec un oscilloscope ou bien grâce à un échantillonnage en
# continu sur l'ADC d'une autre carte à microcontrôleur, la forme du signal depuis une sinusoïde
# jusqu'à un oscillogramme proche d'un signal carré (50 termes max dans notre exemple).

# Matériel utilisé :
# - Une carte NUCLEO-L476RG. La broche de sortie de son unique DAC est 'A2'.
#   Cette information est disponible ici : https://os.mbed.com/platforms/ST-Nucleo-L476RG/.
# - Deux câbles Dupont mâles

# Importation des bibliothèques (classes et méthodes)
from math import sin, pow, pi
from array import array
from pyb import DAC, Pin
import gc

# Déclaration du bouton utilisateur de la NUCLEO-L476RG.
# L'alias 'SW' pour sa broche 'PC13' peut être trouvé ici :
# https://github.com/micropython/micropython/blob/master/ports/stm32/boards/NUCLEO_L476RG/pins.csv

USR_BTN = Pin('SW', Pin.IN, Pin.PULL_UP)

# Est-ce qu'une nouvelle série doit être recalculée ?
COMPUTE = 1

# Fonction de gestion de l'interruption du bouton
def USR_BTN_ISR(pin):

	# Déclarations "global" indispensables dans les fonctions
	# pour éviter des comportements aléatoires du programme !
	global COMPUTE
	global NB_COEF
	
	# Si aucun recalcul de la série n'est en cours ...
	if COMPUTE ==0:
		# Incrémente le nombre de coefficients de Fourier
		NB_COEF += 1 
		if NB_COEF > NB_COEF_MAX:
			NB_COEF = 1
		# Lance l'ordre de recalculer la série
		COMPUTE = 1

# Activation de l'interruption du bouton utilisateur
USR_BTN.irq(trigger = USR_BTN.IRQ_FALLING, handler = USR_BTN_ISR)

# Fréquence du signal (Hz)
FEQUENCY_HZ = const(100)

# Nombre de pas de temps constituant une période du signal. 
PERIOD = const(128)

# Pulsation du signal (rad/s)
OMEGA = 2 * pi / PERIOD

# Nombre maximum de termes dans la série de Fourier du signal carré
# que nous allons générer.
NB_COEF_MAX = const(50)

# Nombre actuel de termes dans la série de Fourier du signal.
# On commence avec un seul terme, donc, au démarrage le DAC émettra
# une fonction sinus de fréquence FEQUENCY_HZ et d'amplitude variant 
# entre 0V et 3.3 V
NB_COEF = 1

# Résolution du DAC : 2^12
DAC_RES = const(12)

# Valeur maximum de commande du DAC
DAC_MAX = pow(2,DAC_RES)-1

# Instanciation du DAC
dac = DAC(1, bits=DAC_RES)

# Tableau de floats qui contiendra les coefficients de Fourier du signal carré
# précalculés jusqu'au terme NB_COEF_MAX.
coef = array('f', [0] * NB_COEF_MAX)

 # Pré-calcule les coefficients de Fourier d'un signal carré (1,3,5,...)
@micropython.native # Optimisation du bytecode pour STM32
def compute_coefs():

	# Déclarations "global" indispensables dans les fonctions
	# pour éviter des comportements aléatoires du programme !
	global coef
	
	# Précalcul des NB_COEF_MAX prmiers coefficients de la série de 
	# Fourier d'un signal carré
	coef[0] = 1
	for i in range(1,NB_COEF_MAX):
		coef[i] = coef[i - 1] + 2

# Tableau de floats qui contiendra une période du signal carré.
# On réalise tous les calculs avec des floats pour ne pas perdre en précision.
# Ils ne seront convertis en entiers codés sur 16 bits (pour programmer le DAC) 
# qu'en toute dernière opération, dans la fonctions update_DAC_buffer (ci-après).
sqsig = array('f',[0]*PERIOD)

# Minimum et maximum de la série de Fourier sur une période
max_val = 0
min_val = DAC_MAX

# Précalcule une période du signal carré
@micropython.native # Optimisation du bytecode pour STM32
def compute_square_period():

	# Déclarations "global" indispensables dans les fonctions
	# pour éviter des comportements aléatoires du programme !
	global sqsig
	global coef
	global min_val, max_val
	global NB_COEF
	global OMEGA
	
	#sqsig = [0]*PERIOD
	max_val = 0
	min_val = DAC_MAX
	
	# Calcul de la série de Fourier
	for i in range(PERIOD):
		
		# Le décompte de i commence à 0, donc il faut décaler de i+1
		# pour que la fréquence du permier terme ne soit pas nulle !
		x = OMEGA * (i+1)

		val = 0.
		
		# Calcule la série de Fourier tronquée d'un signal carré
		# en utilisant les NB_COEFF premiers coefficents de Fourier
		# Série de Fourier "pure" :
		#for j in range(NB_COEF):
		#	val += (1./coef[j]) * sin(coef[j] * x)
		
		# Série de Fourier tronquée avec "approximation sigma" 
		# Voir : https://fr.wikipedia.org/wiki/Approximation_sigma
		for j in range(NB_COEF):
			y = (j+1)/(NB_COEF)
			lanczos = (sin(y)/y) # Fonction sinus cardinal, facteur σ de Lanczos 
			fourier = (1./coef[j]) * sin(coef[j] * x)
			val += lanczos * fourier
			# val += fourier*(1 - lanczos) # Correction de l'approcximation sigma

		# Enregistre la valeur de la série de fourier au point i de la période
		sqsig[i] = val
		
		# Calcule les valeurs minimum et maximum de la série de Fourier sur la période
		# Elles seront utiles pour renormaliser l'amplitude de celle-ci entre 0 et 2^12 - 1
		# (valeur de commande maximum à envoyer au DAC pour une sortie en 3.3V sur 'A2').
		if val > max_val:
			max_val = val
		elif val < min_val:
			min_val = val

# Génère le signal carré avec le DAC
@micropython.native # Optimisation du bytecode pour STM32
def update_DAC_buffer():

	# Déclarations "global"    indispensables dans les fonctions
	# pour éviter des comportements aléatoires du programme !
	global sqsig
	global min_val, max_val

	# Renormalise la série de Fourier calculée dans sqsig et la l'injecte dans le tableau 
	# d'octets 'buf'. 
	# ATTENTION : C'est la seule méthode que nous avons trouvée pour peupler sqsig de sorte  
	# que write_timed l'accepte comme argument ET ne produise pas un signal de sortie du DAC 
	# complètement farfelu !
	# Avis aux amateurs : si vous trouvez une solution plus élégante ...
	
	inv_range = DAC_MAX / (max_val - min_val)
	buf = array('H', int((sqsig[i] - min_val)*inv_range) for i in range(PERIOD))
	
	# Programme de DAC pour générer en boucle la période du signal contenu dans buf,
	# à la fréquence FEQUENCY_HZ.
	# Démarre la génération du signal, acessible par la broche 'A2'.

	dac.write_timed(buf, FEQUENCY_HZ * len(buf), mode=DAC.CIRCULAR)

 # Pré-calcule (une seule fois) les NB_COEF_MAX premiers coefficients de 
 # la série de Fourier d'un signal carré.
compute_coefs()
		
# Boucle principale, à l'écoute des interruptions du bouton 
# utilisateur via la variable globale COMPUTE.
while True:
	
	# Si une demande de calcul est reçue ...
	if COMPUTE:
		
		# Appel du ramasse-miettes (ne peut pas faire de mal !)
		gc.collect()
		
		print('Calcul en cours de %d coefficients de Fourier' %NB_COEF)

		# Recalcule une période de la nouvelle série
		compute_square_period()
		
		# Charge dans le DAC la nouvelle série
		update_DAC_buffer()
		
		# Indique que le calcul est terminé
		COMPUTE = 0
		
		print('Calcul terminé !')
