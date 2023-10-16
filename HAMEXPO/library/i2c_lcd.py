from machine import I2C
import time

_I2CADDR = const(0x3E)

# commands
_LCD_CLEARDISPLAY = const(0x01)
_LCD_RETURNHOME = const(0x02)
_LCD_ENTRYMODESET = const(0x04)
_LCD_DISPLAYCONTROL = const(0x08)
_LCD_CURSORSHIFT = const(0x10)
_LCD_FUNCTIONSET = const(0x20)
_LCD_SETCGRAMADDR = const(0x40)
_LCD_SETDDRAMADDR = const(0x80)

# flags for display entry mode
_LCD_ENTRYRIGHT = const(0x00)
_LCD_ENTRYLEFT = const(0x02)
_LCD_ENTRYSHIFTINCREMENT = const(0x01)
_LCD_ENTRYSHIFTDECREMENT = const(0x00)

# flags for display on/off control
_LCD_DISPLAYON = const(0x04)
_LCD_DISPLAYOFF = const(0x00)
_LCD_CURSORON = const(0x02)
_LCD_CURSOROFF = const(0x00)
_LCD_BLINKON = const(0x01)
_LCD_BLINKOFF = const(0x00)

# flags for display/cursor shift
_LCD_DISPLAYMOVE = const(0x08)
_LCD_CURSORMOVE = const(0x00)
_LCD_MOVERIGHT = const(0x04)
_LCD_MOVELEFT = const(0x00)

# flags for function set
_LCD_8BITMODE = const(0x10)
_LCD_4BITMODE = const(0x00)
_LCD_2LINE = const(0x08)
_LCD_1LINE = const(0x00)
_LCD_5x10DOTS = const(0x04)
_LCD_5x8DOTS = const(0x00)

class lcd:

	def __init__(self, i2c, address = _I2CADDR, oneline = False, charsize = _LCD_5x8DOTS):
		self.i2c = i2c
		self.i2c.scan()
		self.address = address
		self.disp_func = _LCD_DISPLAYON
		if not oneline:
			self.disp_func |= _LCD_2LINE
		elif charsize != 0:
			# for 1-line displays you can choose another dotsize
			self.disp_func |= _LCD_5x10DOTS

		# wait for display init after power-on
		time.sleep_ms(50) # 50ms

		# send function set
		self.cmd(_LCD_FUNCTIONSET | self.disp_func)
		time.sleep_us(5000) #time.sleep(0.0045) # 4.5ms
		self.cmd(_LCD_FUNCTIONSET | self.disp_func)
		time.sleep_us(200) #time.sleep(0.000150) # 150µs = 0.15ms
		self.cmd(_LCD_FUNCTIONSET | self.disp_func)
		time.sleep_us(5000) #time.sleep(0.0045) # 4.5ms
		
		# turn on the display
		self.disp_ctrl = _LCD_DISPLAYON | _LCD_CURSOROFF | _LCD_BLINKOFF
		self.display(True)

		# clear it
		self.clear()

		# set default text direction (left-to-right)
		self.disp_mode = _LCD_ENTRYLEFT | _LCD_ENTRYSHIFTDECREMENT
		self.cmd(_LCD_ENTRYMODESET | self.disp_mode)

	def cmd(self, command):
		assert command >= 0 and command < 256
		command = bytearray([command])
		self.i2c.writeto_mem(self.address, 0x80, command)

	def write_char(self, c):
		assert c >= 0 and c < 256
		c = bytearray([c])
		self.i2c.writeto_mem(self.address, 0x40, c)

	def write(self, text):
		for char in text:
			self.write_char(ord(char))

	def cursor(self, state):
		if state:
			self.disp_ctrl |= _LCD_CURSORON
			self.cmd(_LCD_DISPLAYCONTROL | self.disp_ctrl)
		else:
			self.disp_ctrl &= ~_LCD_CURSORON
			self.cmd(_LCD_DISPLAYCONTROL | self.disp_ctrl)

	def setCursor(self, col, row):
		col = (col | 0x80) if row == 0 else (col | 0xc0)
		self.cmd(col)

	def autoscroll(self, state):
		if state:
			self.disp_ctrl |= _LCD_ENTRYSHIFTINCREMENT
			self.cmd(_LCD_DISPLAYCONTROL | self.disp_ctrl)
		else:
			self.disp_ctrl &= ~_LCD_ENTRYSHIFTINCREMENT
			self.cmd(_LCD_DISPLAYCONTROL | self.disp_ctrl)

	def blink(self, state):
		if state:
			self.disp_ctrl |= _LCD_BLINKON
			self.cmd(_LCD_DISPLAYCONTROL | self.disp_ctrl)
		else:
			self.disp_ctrl &= ~_LCD_BLINKON
			self.cmd(_LCD_DISPLAYCONTROL | self.disp_ctrl)

	def display(self, state):
		if state:
			self.disp_ctrl |= _LCD_DISPLAYON
			self.cmd(_LCD_DISPLAYCONTROL | self.disp_ctrl)
		else:
			self.disp_ctrl &= ~_LCD_DISPLAYON
			self.cmd(_LCD_DISPLAYCONTROL | self.disp_ctrl)

	def clear(self):
		self.cmd(_LCD_CLEARDISPLAY)
		time.sleep_ms(2) # 2ms

	def home(self):
		self.cmd(_LCD_RETURNHOME)
		time.sleep_ms(2) # 2m
