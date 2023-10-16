# Objet du script :
# Pilotage d'un module Grove anneau de LED RGB avec un module Grove capteur de gestes

import neopixel, paj7620 # Pilotes pour l'anneau de LED RGB et le capteur de gestes
from time import sleep_ms # Pour temporiser et mesurer le temps écoulé
from machine import Pin, I2C # Pour gérer les broches et le bus I2C
import uasyncio # Pour la gestion asynchrone 

# On initialise l'anneau de LED sur la broche D2
_NB_LED = const(24) # 24 LED sur l'anneau
ring = neopixel.NeoPixel(Pin('D2'), _NB_LED)

# On utilise l'I2C n°1 de la carte NUCLEO-WB55 pour communiquer avec le capteur de gestes
i2c = I2C(1) 

# Pause d'une seconde pour laisser à l'I2C le temps de s'initialiser
sleep_ms(1000)

# Liste des adresses I2C des périphériques présents
print("Adresses I2C utilisées : " + str(i2c.scan()))

# Adresse du capteur sur le bus I2C : 0x73 
PAJ7620U2_ADR = const(0x73)

# Instanciation du capteur de gestes
g = paj7620.PAJ7620(i2c = i2c)

ROTATION = 1 # Sens de rotation (horaire au démarrage)
_NB_LED_M1 = const(_NB_LED - 1)

# Coroutine asynchrone de gestion de l'anneau de LED RGB
@micropython.native # Demande au compilateur bytecode de produire un code pour le STM32WB55
async def wheel():

	global ROTATION

	led = 0

	while True:
		
		# Index de la LED acourante
		if ROTATION: # Rotation horaire
			led += 1
			if led > _NB_LED_M1:
				led = 0
		else: # Rotation anti-horaire
			led -= 1
			if led < 0:
				led = _NB_LED_M1
		
		# Eteint toutes les LED
		for i in range(_NB_LED):
			ring[i] = (0, 0, 0)

		# Allume la LED courante
		ring[led] = (128, 128, 128)
		ring.write()
		
		# Temporisation non blocante
		await uasyncio.sleep_ms(10)

# Coroutine asynchrone de gestion du capteur de gestes
@micropython.native # Demande au compilateur bytecode de produire un code pour le STM32WB55
async def control():
	
	global ROTATION

	while True:

		gestures = g.gesture()

		if gestures == 7:
			print("Sens horaire")
			ROTATION = 1
		elif gestures == 8:
			print("Sens anti-horaire")
			ROTATION = 0

		# Temporisation non blocante
		await uasyncio.sleep_ms(100)

# Coroutine asynchrone pour lancer les deux autres coroutines
@micropython.native 
async def main():
	# Crée une tache par coroutine
	task1 = uasyncio.create_task(wheel())   # Tache pour la coroutine de gestion de l'anneau
	task2 = uasyncio.create_task(control()) # Tache pour la coroutine de gestion du capteur
	await task1, task2 # Reste en pause aussi longtemps que les deux taches ne sont pas terminées

# Démarre le planificateur (et donc, les deux taches)
uasyncio.run(main())