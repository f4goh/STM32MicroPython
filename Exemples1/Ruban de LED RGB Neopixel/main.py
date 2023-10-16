# Objet du script : Jeux de lumière avec un ruban Neopixel étanche de Grove (60 LED RGB)
# Nécessite également une NUCLEO-WB55 et un Grove Base Shield.
# Source : Christophe PRIOUZEAU, STMicroelectronics

import machine
import time

# Pour gérer le ruban de LED
import neopixel

class StripLED:
	def __init__(self, pin_number, ledNumber, intensity=0.5):
		self._pin = pin_number
		self._ledNumber = ledNumber
		self._intensity = intensity
		self._strip = neopixel.NeoPixel(machine.Pin(self._pin), self._ledNumber)

		self.french_flag = [
					(0,0,250), (0,0,250), (0,0,250),
					(250,250,250), (250,250,250), (250,250,250),
					(250,0,0), (250,0,0), (250,0,0)]
		self.italian_flag = [
					(0,250,0), (0,250,0), (0,250,0),
					(250,250,250), (250,250,250), (250,250,250),
					(250,0,0), (250,0,0), (250,0,0)]

	def _set_to_zero(self, addr):
		if addr < self._ledNumber:
			self._strip[addr] = (0,0,0)
	def _color_intensity(self, color):
		#print("[debug] [%d, %.2f] %d" % (color,  self._intensity, int(color * self._intensity) ))
		return int(color * self._intensity)
	def set_led(self, addr, red, green, blue):
		if addr < self._ledNumber:
			self._strip[addr] = (self._color_intensity(red), self._color_intensity(green), self._color_intensity(blue))

	def _flag_move(self, data, num_led, t):
		i = 0
		while i < (num_led+1):
			if (i + len(data)) < (num_led+1):
				if i != 0:
					self._set_to_zero(i-1)
				j = i
				for d in data:
					self.set_led(j, d[0], d[1], d[2])
					j+=1
				self._strip.write()
				time.sleep_ms(t)
				i+=1
			else:
				break

	def clear(self):
		for i in range(0, self._ledNumber):
			self._set_to_zero(i)
		self._strip.write()

	def get_max_led(self):
		return self._ledNumber

	def french_flag_move(self, t):
		self._flag_move(self.french_flag, self._ledNumber, t)

	def italian_flag_move(self, t):
		self._flag_move(self.italian_flag, self._ledNumber, t)

	def move_dual(self, t):
		self._dual_flag(self.french_flag, self.italian_flag, t)

	def _dual_flag(self, data0, data1, t):
		i = 0
		while i < (self._ledNumber+1):
			if (i + len(data0)) < (self._ledNumber+1):
				for d in data0:
					self.set_led(i, d[0], d[1], d[2])
					self._strip.write()
					time.sleep_ms(t)
					i+=1
				i+=1
			else:
				break
			if (i + len(data1)) < (self._ledNumber+1):
				for d in data1:
					self.set_led(i, d[0], d[1], d[2])
					self._strip.write()
					time.sleep_ms(t)
					i+=1
				i+=1
			else:
				break

# -------------------------------------
#				 MAIN
# -------------------------------------

_NB_LED_RGB = const(60) # Nombre de LED RGB sur le ruban
_INTENSITE_LED = 0.1 # Luminosité des LED (entre 0 et 1)

if __name__ == '__main__':

	# Ruban de LED connecté à D2 sur le Grove Base Shield
	strip_led = StripLED(pin_number='D2', ledNumber = _NB_LED_RGB, intensity= _INTENSITE_LED)

	# Fait défiler un drapeau français au long du ruban
	strip_led.clear()
	strip_led.french_flag_move(500)

	# Fait défiler un drapeau italien au long du ruban
	strip_led.clear()
	strip_led.italian_flag_move(500)
	
	# "Mappe" selon un cycle le ruban en alternant un drapeau français et un drapeau italien
	while True:
		strip_led.clear()
		strip_led.move_dual(100)
		time.sleep(4)
