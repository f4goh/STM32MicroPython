from pyb import Pin
import time

class Keypad(object):
	def __init__(self, lines, cols, debounce_ms=300 ):
		self.lines = [ Pin(pin_name, Pin.OUT, value=True) for pin_name in lines ]
		self.line_count = len( lines )
		self.cols = [ Pin(pin_name, Pin.IN, Pin.PULL_UP) for pin_name in cols ]
		self.col_count = len( cols )

		self.debounce_ms  = debounce_ms
		self.last_release = time.ticks_ms()
		self.last_index   = -1

	def scan( self ):
		r = []
		for i in range(self.line_count):
			self.lines[i].value( 0 )
			for j in range(self.col_count):
				if self.cols[j].value()<=0:
					r.append( i*self.col_count + j )
			self.lines[i].value( 1 )
		return r

	def read( self, timeout=None ):
		ctime = time.time()
		pressed = []
		while( (timeout==None) or ((time.time()-ctime)<timeout) ):
			scan = self.scan()
			pressed.extend( [x for x in scan if x not in pressed] )
			release = [ x for x in pressed if x not in scan ]
			if len(release)>0:
				if ((time.ticks_ms()-self.last_release)<self.debounce_ms) and (self.last_index==release[0]):
					continue
				else:
					self.last_release = time.ticks_ms() # Now
					self.last_index   = release[0]
					return self.last_index
		return None

class Keypad4x4( Keypad ):
	def __init__( self, lines=["D11","D10","D9","D8"], cols=["D7","D6","D5","D4"], map="123A456B789C*0#D" ):
		self.map = map
		super().__init__( lines, cols )

	def read_key( self, timeout=None ):
		idx = self.read( timeout=timeout )
		if idx!=None:
			return( self.map[idx] )
		else:
			return None

class Keypad3x4( Keypad ):
	def __init__( self, lines=["D9","D4","D5","D7"], cols=["D8","D10","D6"], map="123456789*0#" ):
		self.map = map
		super().__init__( lines, cols )

	def read_key( self, timeout=None ):
		idx = self.read( timeout=timeout )
		if idx!=None:
			return( self.map[idx] )
		else:
			return None
