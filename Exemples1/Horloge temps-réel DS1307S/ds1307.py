# Pilote adapté à partir de la source à l'adresse suivante :
# https://github.com/mcauser/micropython-tinyrtc-i2c/blob/master/ds1307.py
# ATTENTION, pour fonctionner correctement ce module doit être alimenté en 5V

# Adresse I2C du module
_RTC_ADDRESS = const(0x68)
_DATETIME_REG = const(0) # 0x00-0x06
_CHIP_HALT = const(128)
_CONTROL_REG = const(7) # 0x07

class DS1307():
	def __init__(self, i2c, addr= _RTC_ADDRESS):
		self.i2c = i2c
		self.i2c.scan()
		self.addr = addr
		self.weekday_start = 1
		self._halt = False
		self.buf = bytearray(7)

	def _dec2bcd(self, value):
		return (value // 10) << 4 | (value % 10)

	def _bcd2dec(self, value):
		return ((value >> 4) * 10) + (value & 0x0F)

	def readDateTime(self):
		self.buf = self.i2c.readfrom_mem(self.addr, _DATETIME_REG, 7)
		return (
			self._bcd2dec(self.buf[6]) + 2000, # year
			self._bcd2dec(self.buf[5]), # month
			self._bcd2dec(self.buf[4]), # day
			self._bcd2dec(self.buf[3] - self.weekday_start), # weekday
			self._bcd2dec(self.buf[2]), # hour
			self._bcd2dec(self.buf[1]), # minute
			self._bcd2dec(self.buf[0] & 0x7F) # second
		)

	def setDateTime(self, datetime):
		buf=[0,0,0,0,0,0,0]
		buf[0] = self._dec2bcd(datetime[6]) & 0x7F # second, msb = CH, 1=halt, 0=go
		buf[1] = self._dec2bcd(datetime[5]) # minute
		buf[2] = self._dec2bcd(datetime[4]) # hour
		buf[3] = self._dec2bcd(datetime[3]) + self.weekday_start # weekday
		buf[4] = self._dec2bcd(datetime[2]) # day
		buf[5] = self._dec2bcd(datetime[1]) # month
		buf[6] = self._dec2bcd(datetime[0] - 2000) # year
		if (self._halt):
			buf[0] |= (1 << 7)
		self.i2c.writeto_mem(self.addr, _DATETIME_REG, bytearray(buf))

	def halt(self, val=None):
		if val is None:
			return self._halt
		reg = self.i2c.readfrom_mem(self.addr, _DATETIME_REG, 1)[0]
		if val:
			reg |= _CHIP_HALT
		else:
			reg &= ~_CHIP_HALT
		self._halt = bool(val)
		self.i2c.writeto_mem(self.addr, _DATETIME_REG, bytearray([reg]))
