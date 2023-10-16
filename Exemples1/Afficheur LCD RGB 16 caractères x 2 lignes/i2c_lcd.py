# RESSOURCES: https://github.com/Bucknalla/micropython-i2c-lcd
# (c) 2017 Alex Bucknall <alex.bucknall@gmail.com>

from machine import I2C
import i2c_lcd_backlight
import i2c_lcd_screen

class Display(object):
	backlight = None
	screen = None

	def __init__(self, i2c):
		self_lcd_addr=0x3e
		self_rgb_addr=0x62
		self.backlight = i2c_lcd_backlight.Backlight(i2c, self_rgb_addr) # fs
		self.screen = i2c_lcd_screen.Screen(i2c, self_lcd_addr)

	def write(self, text):
		self.screen.write(text)

	def cursor(self, state):
		self.screen.cursor(state)

	def blink(self, state):
		self.screen.blink(state)

	def blinkLed(self):
		self.backlight.blinkLed()

	def autoscroll(self, state):
		self.screen.autoscroll(state)

	def display(self, state):
		self.screen.display(state)

	def clear(self):
		self.screen.clear()

	def home(self):
		self.screen.home()

	def color(self, r, g, b):
		self.backlight.set_color(r, g, b)

	def move(self, col, row):
		self.screen.setCursor(col, row)
