# Cube 3D en rotation
# basé on MicroViewCube.ino de Jim Lindblom @ SparkFun Electronics
# https://github.com/sparkfun/SparkFun_MicroView_Arduino_Library/blob/master/examples/MicroViewCube/MicroViewCube.ino
# Conversion en MicroPython par Mike Causer :
# https://github.com/mcauser/micropython-ssd1327/blob/master/examples/rotating_3d_cube.py

from machine import I2C # Pour piloter l'I2C
from time import sleep # pour temporiser
import ssd1327 # Pilote de l'afficheur Grove - OLED Display 1.12" (96 x 96)
import math

# On utilise l'I2C n°1 de la carte NUCLEO-WB55 
i2c1 = I2C(1)

# Pause d'une seconde pour laisser à l'I2C le temps de s'initialiser
sleep(1)

# Initialisation de l'afficheur
display = ssd1327.SEEED_OLED_96X96(i2c1) 
display.clear() # On efface l'écran

pi = math.pi

size = 700
width = display.width
height = display.height

# Données pour la matrice de rotation
d = 3
px = [-d,  d,  d, -d, -d,  d,  d, -d]
py = [-d, -d,  d,  d, -d, -d,  d,  d]
pz = [-d, -d, -d, -d,  d,  d,  d,  d]

p2x = [0,0,0,0,0,0,0,0]
p2y = [0,0,0,0,0,0,0,0]
r = [0,0,0]

# Optimisation du bytecode pour l'architecture STM32
@micropython.native
def drawCube():

	# Calcul des nouvelles coordonnées des sommets du cube après rotation
	r[0] = r[0] + pi / 180.0
	r[1] = r[1] + pi / 180.0
	r[2] = r[2] + pi / 180.0
	if (r[0] >= 360.0 * pi / 180.0):
		r[0] = 0
	if (r[1] >= 360.0 * pi / 180.0):
		r[1] = 0
	if (r[2] >= 360.0 * pi / 180.0):
		r[2] = 0

	for i in range(8):
		px2 = px[i]
		py2 = math.cos(r[0]) * py[i] - math.sin(r[0]) * pz[i]
		pz2 = math.sin(r[0]) * py[i] + math.cos(r[0]) * pz[i]

		px3 = math.cos(r[1]) * px2 + math.sin(r[1]) * pz2
		py3 = py2
		pz3 = -math.sin(r[1]) * px2 + math.cos(r[1]) * pz2

		ax = math.cos(r[2]) * px3 - math.sin(r[2]) * py3
		ay = math.sin(r[2]) * px3 + math.cos(r[2]) * py3
		az = pz3 - 150

		p2x[i] = width / 2 + ax * size / az
		p2y[i] = height / 2 + ay * size / az

	# Affichage du nouveau cube
	display.fill(0)

	for i in range(3):
		display.framebuf.line(int(p2x[i]),   int(p2y[i]),   int(p2x[i+1]), int(p2y[i+1]), 1)
		display.framebuf.line(int(p2x[i+4]), int(p2y[i+4]), int(p2x[i+5]), int(p2y[i+5]), 1)
		display.framebuf.line(int(p2x[i]),   int(p2y[i]),   int(p2x[i+4]), int(p2y[i+4]), 1)

	display.framebuf.line(int(p2x[3]), int(p2y[3]), int(p2x[0]), int(p2y[0]), 1)
	display.framebuf.line(int(p2x[7]), int(p2y[7]), int(p2x[4]), int(p2y[4]), 1)
	display.framebuf.line(int(p2x[3]), int(p2y[3]), int(p2x[7]), int(p2y[7]), 1)
	display.show()

while True:
	drawCube()