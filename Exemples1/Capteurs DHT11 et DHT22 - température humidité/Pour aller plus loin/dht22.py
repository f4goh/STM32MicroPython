# Exemple adapté de https://github.com/kurik/uPython-DHT22/blob/master/main.py
# Construction d'un pilote pour le DHT22 en utilisant un timer pour compter les
# fronts (descendants) des signaux.

from time import sleep_ms # Pour temporiser
from pyb import ExtInt, Pin, Timer # Pour gérer les broches, les interruptions des broches et les Timers.

# Nous devons utiliser ici des variables globales car toute allocation de variable locale
# entrainerait un délai qui planterait la communication.

data = None
timer = None
micros = None

FALL_EDGES = const(42) # La réception comporte 42 fronts descendants

times = list(range(FALL_EDGES))
index = 0

# Le gestionnaire d'interruptions : capture la réponse du capteur après lee START
@micropython.native
def edge(line):

	global index
	global times
	global micros

	times[index] = micros.counter()
	if index < (FALL_EDGES - 1): # Pour éviter un dépassement de buffer s'il y a du bruit sur la ligne
		index += 1

# Initialisation du capteur
@micropython.native
def init(timer_id = 2, data_pin = 'D2'):

	global data
	global micros
	
	# Broche de la ligne de communication
	data = Pin(data_pin)
	
	# Identifiant du timer sélectionné
	timer = timer_id
	
	# Paramètres pour un timer de fréquence 1 microseconde
	micros = Timer(timer, prescaler=65, period=0x3fffffff)

	# Gestionnaire de l'interruption du timer
	ExtInt(data, ExtInt.IRQ_FALLING, Pin.PULL_UP, edge)

@micropython.native
def do_measurement():

	global data
	global micros
	global index

	# Envoie la commande START
	data.init(Pin.OUT_PP)
	data.low()
	micros.counter(0)
	while micros.counter() < 25000:
		pass
		
	# Passe la broche en IN
	data.high()
	micros.counter(0)
	index = 0
	data.init(Pin.IN, Pin.PULL_UP)

	# Après 5 millisecondes, la mesure doit être terminée
	sleep_ms(5)
	
# Lis les données renvoyées par le capteur
@micropython.native
def process_data():
	global times
	i = 2 # On ignore les deux premiers fronts descendants qui sont la réponse à la commande START
	result_i = 0
	result = list([0, 0, 0, 0, 0])
	
	while i < FALL_EDGES:
		result[result_i] <<= 1
		if times[i] - times[i - 1] > 100:
			result[result_i] += 1
		if (i % 8) == 1:
			result_i += 1
		i += 1
		
	[int_rh, dec_rh, int_t, dec_t, csum] = result
	humidity = ((int_rh * 256) + dec_rh)/10
	temperature = (((int_t & 0x7F) * 256) + dec_t)/10
	if (int_t & 0x80) > 0:
		temperature *= -1
	comp_sum = int_rh + dec_rh + int_t + dec_t
	if (comp_sum & 0xFF) != csum:
		raise ValueError('La somme de contrôle est incorrecte')
	return (humidity, temperature)

@micropython.native
def measure():
	do_measurement()
	if index != (FALL_EDGES -1):
		raise ValueError('Echec du transfert de données : %s fronts descendants seulement' % str(index))
	return process_data()