# Objet du script : 
# Jouer un jingle sur un buzzer/speaker (Grove ou autre) d'après l'exemple
# "Jouer la musique Pirates des Caraïbles" de l'IDE Vittascience.
# Cet exemple fait la démonstration de l'usage de la GPIO D6, sur laquelle est 
# branché le buzzer/speaker, 

import machine
import utime

# Buzzer connecté sur la broche D6
d6 = machine.Pin('D6', machine.Pin.OUT)

# Fréquences et durées des différentes notes musicales

FREQUENCIES_1 = [330, 392, 440, 440, 0, 440, 494, 523, 523, 0, 523, 587, 494, 494, 0, 440, 392, 440, 0]

DURATIONS_1 = [125, 125, 250, 125, 125, 125, 125, 250, 125, 125, 125, 125, 250, 125, 125, 125, 125, 375, 125]

FREQUENCIES_2 = [330, 392, 440, 440, 0, 440, 523, 587, 587, 0, 587, 659, 698, 698, 0, 659, 587, 659, 440, 0, 440, 494, 523, 523, 0, 587, 659, 440, 0, 440, 523, 494, 494, 0, 523, 440, 494, 0]

DURATIONS_2 = [125, 125, 250, 125, 125, 125, 125, 250, 125, 125, 125, 125, 250, 125, 125, 125, 125, 125, 250, 125, 125, 125, 250, 125, 125, 250, 125, 250, 125, 125, 125, 250, 125, 125, 125, 125, 375, 375]

# Simule la fréquence de la note en inversant très rapidement l'état de D6 pendant sa durée
@micropython.native # Décorateur pour forcer la génération d'un code assembleur pour STM32 (plus rapide)
def pitch (pin, noteFrequency, noteDuration, silence_ms = 10):
	if noteFrequency is not 0:
	
		microsecondsPerWave = 1e6 / noteFrequency
		millisecondsPerCycle = 1000 / (microsecondsPerWave * 2)
		loopTime = noteDuration * millisecondsPerCycle

		for x in range(loopTime):
			pin.high()
			utime.sleep_us(int(microsecondsPerWave))
			pin.low()
			utime.sleep_us(int(microsecondsPerWave))

	else:
		utime.sleep_ms(noteDuration)
	utime.sleep_ms(silence_ms)

# Joue en boucle la mélodie
while True:

	# Répète trois fois ...
	for j in range(2):
		# Joue une fois les notes de la liste NOTES_1
		for i in range(len(FREQUENCIES_1)):
			pitch(d6, FREQUENCIES_1[i], DURATIONS_1[i])

	# Joue une fois les notes de la liste NOTES_2
	for k in range(len(FREQUENCIES_2)):
		pitch(d6, FREQUENCIES_1[k], DURATIONS_2[k])
