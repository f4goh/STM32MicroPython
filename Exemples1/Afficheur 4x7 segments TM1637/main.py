# Exemple adapté de https://github.com/mcauser/micropython-tm1637'
# Objet du script :
# Mesure la température (en degrés celsius) de l'air ambiant toutes les secondes
# Affiche la température sur l'afficheur Grove 7-segments
# Cet exemple nécessite un shield X-NUCLEO IKS01A3, un Grove Base Shield pour Arduino et un Afficheur Grove 7-segments.
# L'afficheur 7-segments doit être connecté sur la fiche "A0" du Grove Base Shield pour Arduino.

from machine import I2C # Pilotes du bus I2C
import stts751 # Pilotes du capteur de température

# Pilotes GPIO et temporisation de Micropython
import pyb
from time import  sleep_ms
from pyb import Pin
# Pilotes de l'afficheur 7-segments
import tm1637

# Initialisation de l'afficheur 7-segments
tm = tm1637.TM1637(clk=Pin('A0'), dio=Pin('A1'))

# On utilise l'I2C n°1 de la carte NUCLEO-WB55 pour communiquer le capteur de température
i2c = I2C(1) 

# Pause d'une seconde pour laisser à l'I2C le temps de s'initialiser
sleep_ms(1000)

sensor = stts751.STTS751(i2c)

blue_led = pyb.LED(1)
green_led = pyb.LED(2)
red_led = pyb.LED(3)

while True:
	
	# Lecture de la température et arrondi à l'entier le plus proche
	temp = round(sensor.temperature())
	
	# Affichage des données au format entier
	# le end='' à la fin signale qu'il ne doit pas y avoir de saut de ligne après
	print("Température : %1d °C (" %temp, end='')
	
	tm.number(temp) # Affiche la température
	
	if temp > 24:
		red_led.on()
		print("Chaud)")
	elif temp > 16 and temp <= 24:
		green_led.on()
		print("Confortable)")
	else:
		blue_led.on()
		print("Froid)")

    # Eteint toutes les LED
	red_led.off()
	green_led.off()
	blue_led.off()

	# Temporisation d'une seconde
	sleep_ms(1000) 