# Objet du script :
# Conception d'une veilleuse d'obscurité ... 
# - Lit l'intensité lumineuse ambiante avec un capteur Grove 
# de luminosité (LS06-S phototransistor)
# - Allume une LED (module Grove) avec une intensité 
# inversement proportionnelle à la lumière ambiante.
# Alimentation du Grove base shield sur 5V
# LED connectée sur D6 (PWM Timer 1, Channel 1)
# Photodiode connectée sur A1

from time import sleep_ms
from pyb import ADC, Timer

# Photorésistance sur A1 (analogique)
adc = ADC('A1')

# LED sur D6 (sortie PWM)
led = pyb.Pin('D6', pyb.Pin.OUT_PP)

# Configuration du timer : timer 1 channel 1
# sur broche d6 (d'après la cartographie des PWM de la NUCELO-WB55)
d6 = pyb.Pin('D6', pyb.Pin.OUT_PP)

# Fréquence du timer fixée à 100 Hz
tim_d6 = pyb.Timer(1, freq = 100)

# Génération de signal PWM démarrée sur D6
pwm_d6 = tim_d6.channel(1, pyb.Timer.PWM, pin=d6)

# Fonction pour remapper un intervalle de valeurs dans un autre
def map (value, from_min, from_max, to_min, to_max):
	return (value-from_min) * (to_max-to_min) / (from_max-from_min) + to_min

while True:

	# Récupération de la valeur de la photorésistance
	sampled = adc.read()
	
	# Convertit la lecture analogique en pourcentage
	ambiant_light_percentage = map(sampled, 0, 4095, 0, 100)

	# Change l'intensité de luminosité de la LED via la PWM
	pwm_d6.pulse_width_percent(100 - ambiant_light_percentage)
	
	# Temporisation d'une seconde
	sleep_ms(1000)