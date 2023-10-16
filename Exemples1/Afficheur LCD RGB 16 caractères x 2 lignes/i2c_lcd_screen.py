# modif fs

# test OK avec :
# Cible : MicroPython v1.12-510-g1e6d18c91 on 2020-06-08; NUCLEO-WB55 with STM32WB55RGV6
""" shield grove
afficheur i2c (adresse 0x3e) Grove 16x2 LCD
!/usr/bin/python
# -*- coding: utf-8 -*-
# This is a port of https://github.com/Seeed-Studio/Grove_LCD_RGB_Backlight
# (c) 2017 Alex Bucknall <alex.bucknall@gmail.com>
"""
from machine import I2C
import time

# commands
LCD_CLEARDISPLAY = const(0x01)
LCD_RETURNHOME = const(0x02)
LCD_ENTRYMODESET = const(0x04)
LCD_DISPLAYCONTROL = const(0x08)
LCD_CURSORSHIFT = const(0x10)
LCD_FUNCTIONSET = const(0x20)
LCD_SETCGRAMADDR = const(0x40)
LCD_SETDDRAMADDR = const(0x80)

# flags for display entry mode
LCD_ENTRYRIGHT = const(0x00)
LCD_ENTRYLEFT = const(0x02)
LCD_ENTRYSHIFTINCREMENT = const(0x01)
LCD_ENTRYSHIFTDECREMENT = const(0x00)

# flags for display on/off control
LCD_DISPLAYON = const(0x04)
LCD_DISPLAYOFF = const(0x00)
LCD_CURSORON = const(0x02)
LCD_CURSOROFF = const(0x00)
LCD_BLINKON = const(0x01)
LCD_BLINKOFF = const(0x00)

# flags for display/cursor shift
LCD_DISPLAYMOVE = const(0x08)
LCD_CURSORMOVE = const(0x00)
LCD_MOVERIGHT = const(0x04)
LCD_MOVELEFT = const(0x00)

# flags for function set
LCD_8BITMODE = const(0x10)
LCD_4BITMODE = const(0x00)
LCD_2LINE = const(0x08)
LCD_1LINE = const(0x00)
LCD_5x10DOTS = const(0x04)
LCD_5x8DOTS = const(0x00)

class Screen(object):

	def __init__(self, i2c, address, oneline=False, charsize=LCD_5x8DOTS):

		self.i2c = i2c
		self.i2c.scan()
		self.address = address

		self.disp_func = LCD_DISPLAYON
		if not oneline:
			self.disp_func |= LCD_2LINE
		elif charsize != 0:
			# for 1-line displays you can choose another dotsize
			self.disp_func |= LCD_5x10DOTS

		# wait for display init after power-on
		time.sleep_ms(50) # 50ms

		# send function set
		self.cmd(LCD_FUNCTIONSET | self.disp_func)
		time.sleep_us(4500) ##time.sleep(0.0045) # 4.5ms
		self.cmd(LCD_FUNCTIONSET | self.disp_func)
		time.sleep_us(150) ##time.sleep(0.000150) # 150µs = 0.15ms
		self.cmd(LCD_FUNCTIONSET | self.disp_func)

		# turn on the display
		self.disp_ctrl = LCD_DISPLAYON | LCD_CURSOROFF | LCD_BLINKOFF
		self.display(True)

		# clear it
		self.clear()

		# set default text direction (left-to-right)
		self.disp_mode = LCD_ENTRYLEFT | LCD_ENTRYSHIFTDECREMENT
		self.cmd(LCD_ENTRYMODESET | self.disp_mode)

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
			self.disp_ctrl |= LCD_CURSORON
			self.cmd(LCD_DISPLAYCONTROL  | self.disp_ctrl)
		else:
			self.disp_ctrl &= ~LCD_CURSORON
			self.cmd(LCD_DISPLAYCONTROL  | self.disp_ctrl)

	def setCursor(self, col, row):
		col = (col | 0x80) if row == 0 else (col | 0xc0)
		self.cmd(col)

	def autoscroll(self, state):
		if state:
			self.disp_ctrl |= LCD_ENTRYSHIFTINCREMENT
			self.cmd(LCD_DISPLAYCONTROL  | self.disp_ctrl)
		else:
			self.disp_ctrl &= ~LCD_ENTRYSHIFTINCREMENT
			self.cmd(LCD_DISPLAYCONTROL  | self.disp_ctrl)

	def blink(self, state):
		if state:
			self.disp_ctrl |= LCD_BLINKON
			self.cmd(LCD_DISPLAYCONTROL  | self.disp_ctrl)
		else:
			self.disp_ctrl &= ~LCD_BLINKON
			self.cmd(LCD_DISPLAYCONTROL  | self.disp_ctrl)

	def display(self, state):
		if state:
			self.disp_ctrl |= LCD_DISPLAYON
			self.cmd(LCD_DISPLAYCONTROL  | self.disp_ctrl)
		else:
			self.disp_ctrl &= ~LCD_DISPLAYON
			self.cmd(LCD_DISPLAYCONTROL  | self.disp_ctrl)

	def clear(self):
		self.cmd(LCD_CLEARDISPLAY)
		time.sleep_ms(2) # 2ms

	def home(self):
		self.cmd(LCD_RETURNHOME)
		time.sleep_ms(2) # 2m
