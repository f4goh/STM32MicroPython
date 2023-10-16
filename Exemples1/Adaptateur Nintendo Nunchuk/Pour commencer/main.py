# Objet du script : Mise en œuvre de l'adaptateur Nintendo Nunchuk
# Pour commencer : récupérer les données de la manette WiiMote.

from machine import I2C, Pin
from time import sleep_ms
from wiichuck import WiiChuck

i2c = I2C(1)

# Pause d'une seconde pour laisser à l'I2C le temps de s'initialiser
time.sleep_ms(1000)

wii = WiiChuck(i2c)

while True:
	direction = ''
	if wii.joy_up:
		direction = 'Haut'
	elif wii.joy_down:
		direction = 'Bas'
	elif wii.joy_right:
		direction = 'Droite'
	elif wii.joy_left:
		direction = 'Gauche'
	else:
		direction = '-----'
	if(wii.c):
		Cbutton = 'C'
	else:
		Cbutton = '-'
	if(wii.z):
		Zbutton = 'Z'
	else:
		Zbutton = '-'

	print("Joystick: (%3d, %3d) %6s \t| Accelerometre XYZ: (%3d, %3d, %3d) \t| Boutons: %s %s" %(wii.joy_x, wii.joy_y, direction, wii.accel_x, wii.accel_y, wii.accel_z, Cbouton, Zbouton))

	wii.update()
	sleep_ms(100)
