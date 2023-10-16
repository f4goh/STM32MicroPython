# Code adapté de la source ci-dessous :
# https://github.com/blaa/th02-sensor/blob/master/

from time import ticks_us, ticks_diff

class TH02:
	"""
	Interface to the TH02 temp/humidity sensor.
	"""
	CHECK_DELAY = 25000 # delay in microseconds

	CONVERSION_TEMP = 0x11
	# Convert without the built-in heater
	CONVERSION_HUMIDITY = 0x01

	REGISTER_STATUS = const(0x00)
	REGISTER_DATAH = const(0x01)
#	REGISTER_DATAL = const(0x02)
	REGISTER_CONFIG = const(0x03)
	I2C_ADDRESS = const(0x40)

	def __init__(self, i2c):
		self.i2c = i2c
		self.i2c.scan()
		self.buf = bytearray(2)

	def init_temp(self):
		"""Send command to TH02 for convert temperature"""

	def init_humidity(self):
		"""Send command to TH02 for convert humidity"""
		self.i2c.writeto_mem(self.I2C_ADDRESS, self.REGISTER_CONFIG, bytearray([self.CONVERSION_HUMIDITY]))

	def is_ready(self):
		"""Is sensor done with conversion"""
		self.buf = self.i2c.readfrom_mem(self.I2C_ADDRESS, self.REGISTER_STATUS, 1)
		# Extract ready bit
		ready = not (self.buf[0] and 0x01)
		return bool(ready)

	def wait_until_ready(self):
		"Wait until conversion completes"
		self.delay_us(self.CHECK_DELAY )
		for _ in range(8):
			if self.is_ready():
				return True
			self.delay_us(self.CHECK_DELAY)
		return False

	def read_data(self):
		"""Read the DATA registers"""
#		self.buf = self.i2c.readfrom_mem(self.I2C_ADDRESS, self.REGISTER_DATAH, 1)
#		data = self.buf[0] << 8
#		self.buf = self.i2c.readfrom_mem(self.I2C_ADDRESS, self.REGISTER_DATAL, 1)
#		data |= self.buf[0]
		self.buf = self.i2c.readfrom_mem(self.I2C_ADDRESS, self.REGISTER_DATAH, 2)
		data = self.buf[0] << 8 | self.buf[1]
		return data

	def calculate_temp(self, data):
		"""Calculate temperature from register value"""
		temp = data >> 2
		temp /= 32.0
		temp -= 50.0
		return temp

	def calculate_humidity(self, data):
		"""Calculate humidity from register value"""
		humidity = data >> 4
		humidity /= 16.0
		humidity -= 24.0
		return humidity

	def get_temperature(self):
		"""Return temperature or -60 if there is an error"""
		self.i2c.writeto_mem(self.I2C_ADDRESS, self.REGISTER_CONFIG, bytearray([self.CONVERSION_TEMP]))
		if self.wait_until_ready():
			data = self.read_data()
			return self.calculate_temp(data)

		# Error
		return -60

	def get_humidity(self):
		"""Return relative humidity or -60 if there is an error"""
		self.i2c.writeto_mem(self.I2C_ADDRESS, self.REGISTER_CONFIG, bytearray([self.CONVERSION_HUMIDITY]))

		if self.wait_until_ready():
			data = self.read_data()
			return self.calculate_humidity(data)

		# Error
		return -60
		
	# Non blocking delay in microseconds
	def delay_us(self, us):
		start = ticks_us()
		while ticks_diff(ticks_us(),start) < us:
			pass
