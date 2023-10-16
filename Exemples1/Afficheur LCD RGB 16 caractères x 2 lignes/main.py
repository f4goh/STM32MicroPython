# Bibliothèques pour le LCD RGB copiées depuis ce site : https://github.com/Bucknalla/micropython-i2c-lcd
# Objet du script :
# Mesure la température (en degrés Celsius) de l'air ambiant toutes les secondes
# Affiche la température sur le LCD RGB Grove et sur le terminal de l'USB USER
# Ajuste la couleur de fond du LCD et allume les LED selon la température lue
# Cet exemple nécessite un shield X-NUCLEO IKS01A3, un Grove Base Shield pour Arduino et un LCD RGB Grove.
# Attention, le LCD RGB Grove doit être alimenté en 5V, pensez à placer le commutateur du Grove Base Shield
# pour Arduino sur la bonne position !
# NB : C'est le shield X-NUCLEO IKS01A3 qui apporte les résistances de PULL-UP sur les broches 
# SCL et SDA de l'I2C, indispensables au bon fonctionnement du LCD RGB Grove.

from machine import I2C # Bibliothèque pour gérer l'I2C
import stts751 # Bibliothèque pour gérer le capteur MEMS de température 
import pyb # Bibliothèque qui sera utilisée pour gérer les LED
from time import sleep_ms # Bibliothèque qui sera utilisée pour gérer les temporisations
import i2c_lcd # Bibliothèque pour gérer l'afficheur LCD RGB Grove

# On utilise l'I2C n°1 de la carte NUCLEO-WB55 pour communiquer avec le capteur
i2c = I2C(1) 

# Pause d'une seconde pour laisser à l'I2C le temps de s'initialiser
sleep_ms(1000)

sensor = stts751.STTS751(i2c)

#Instance de la classe Display
lcd = i2c_lcd.Display(i2c)
lcd.home()

# Initialisation des trois LED
blue_led = pyb.LED(1)
green_led = pyb.LED(2)
red_led = pyb.LED(3)

while True:

	# Mesure de température
	temp = sensor.temperature()
	

	# Affichage sur le port série de l'USB USER
	print("Température : %.1f °C (" %temp, end='')

	lcd.move(0,0) #On se place en colonne 0, ligne 0
	lcd.write('Temperature (C)') # On écrit à partir de la position du curseur la chaîne "Temperature (C)"
	lcd.move(0,1) #On se place en colonne 0, ligne 1
	lcd.write(str(temp)) # On écrit la représentation affichable de la température
	
	if temp > 25 :
		red_led.on()
		print("chaud)")
		lcd.color(255,0,0) # Rétroéclairage du LCD : rouge
	elif temp > 18 and temp <= 25 :
		green_led.on()
		print("confortable)")
		lcd.color(0,255,0) # Rétroéclairage du LCD : vert
	else:
		blue_led.on()
		print("froid)")
		lcd.color(0,0,255) # Rétroéclairage du LCD : bleu

	# On éteint les LED
	red_led.off()
	green_led.off()
	blue_led.off()
	
	# Temporisation d'une seconde
	sleep_ms(1000)