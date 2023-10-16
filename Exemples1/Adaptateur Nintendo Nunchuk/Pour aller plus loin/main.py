# Objet du script : Mise en œuvre de l'adaptateur Nintendo Nunchuk
# Pour aller plus loins : contrôler un servomoteur avec la manette WiiMote.

import pyb
from machine import I2C
from time import sleep_ms
from wiichuck import WiiChuck
from pyb import Pin, Timer
import math

# Initalisation servomoteur (Timer 1 channel 1, fréquence = 50 Hz)
servo = pyb.Pin('D6')
tim_servo = pyb.Timer(1, freq=50)

# Driver moteur ("enable" + "input 1" et "input 2" en sorties)
motor_enable = pyb.Pin('D1')
motor_pin1 = pyb.Pin('D0', Pin.OUT_PP)
motor_pin2 = pyb.Pin('D2', Pin.OUT_PP)
motor_pin1.low()
motor_pin2.low()

# PWM pour le moteur (Timer 2 channel 3, fréquence = 1kHz et sur "enable")
tim2 = Timer(2, freq=1000)
ch3 = tim2.channel(3, Timer.PWM, pin=motor_enable)

# PWM pour régler la tension du moteur
ch3.pulse_width_percent(0)

# Initialisation Nunchuk en I2C
i2c = I2C(1)
sleep_ms(1000)
wii = WiiChuck(i2c)

while True:

	# Si mouvement sur l'axe X alors fait tourner le servo
	joystick_x = (wii.joy_x + 200)/27
	tim_servo.channel(1, pyb.Timer.PWM, pin=servo, pulse_width_percent=joystick_x)

		# Si mouvement sur l'axe Y 
	if(wii.joy_y < -5):			#Vers le bas
		motor_pin1.high()
		motor_pin2.low()
		ch3.pulse_width_percent(abs(wii.joy_y))
	elif(wii.joy_y > 5):		#Vers le haut
		motor_pin1.low()
		motor_pin2.high()
		ch3.pulse_width_percent(wii.joy_y)
	else:						#Au repos
		motor_pin1.low()
		motor_pin2.low()
		ch3.pulse_width_percent(0)

	wii.update()