import machine
import pyb

# Servomoteur sur D6
d6 = pyb.Pin('D6', pyb.Pin.OUT_PP)
tim_d6 = pyb.Timer(1, freq=50)
pwm_d6 = tim_d6.channel(1, pyb.Timer.PWM, pin=d6)

# Potentiomètre sur A0
a0 = pyb.ADC('A0')

# Convertit l'ange de rotation (en entrée) en une valeur de PWM puis l'envoie au servo.
def setServoAngle(timer, angle):
	if (angle >= 0 and angle <= 180):
		pw_percent = 3 + angle * (12.5 - 3) / 180
		timer.pulse_width_percent(pw_percent)
	else:
		raise ValueError("La commande d'angle du servomoteur doit être comprise entre 0° et 180°")

# Fonction pour remapper un intervalle de valeurs dans un autre
def map (value, from_min, from_max, to_min, to_max):
  return (value-from_min) * (to_max-to_min) / (from_max-from_min) + to_min

# Initialise le servo sur un angle de 90° 
setServoAngle(pwm_d6, 90)

while True:
	
	# Convertit la lecture analogique du potentiomètre en un angle entre 0° et 180°
	angle = int(map(a0.read(), 0, 4095, 0, 180))
	
	# Applique cet angle au servomoteur
	setServoAngle(pwm_d6, angle)
