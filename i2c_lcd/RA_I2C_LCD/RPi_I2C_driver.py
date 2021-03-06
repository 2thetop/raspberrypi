# -*- coding: utf-8 -*-
"""
Compiled, mashed and generally mutilated 2014-2015 by Denis Pleic
Made available under GNU GENERAL PUBLIC LICENSE

# Modified Python I2C library for Raspberry Pi
# as found on http://www.recantha.co.uk/blog/?p=4849
# Joined existing 'i2c_lib.py' and 'lcddriver.py' into a single library
# added bits and pieces from various sources
# By DenisFromHR (Denis Pleic)
# 2015-02-10, ver 0.1
# hacked about by Ken Robson (Hairybiker)
# 2015/07/01 ver 0.3
"""
#
#
import smbus
from time import *

class i2c_device:
   def __init__(self, addr, port=1):
      self.addr = addr
      self.bus = smbus.SMBus(port)

# Write a single command
   def write_cmd(self, cmd):
      self.bus.write_byte(self.addr, cmd)
      sleep(0.0001)

# Write a command and argument
   def write_cmd_arg(self, cmd, data):
      self.bus.write_byte_data(self.addr, cmd, data)
      sleep(0.0001)

# Write a block of data
   def write_block_data(self, cmd, data):
      self.bus.write_block_data(self.addr, cmd, data)
      sleep(0.0001)

# Read a single byte
   def read(self):
      return self.bus.read_byte(self.addr)

# Read
   def read_data(self, cmd):
      return self.bus.read_byte_data(self.addr, cmd)

# Read a block of data
   def read_block_data(self, cmd):
      return self.bus.read_block_data(self.addr, cmd)



# LCD Address
ADDRESS = 0x27

# commands
LCD_CLEARDISPLAY = 0x01
LCD_RETURNHOME = 0x02
LCD_ENTRYMODESET = 0x04
LCD_DISPLAYCONTROL = 0x08
LCD_CURSORSHIFT = 0x10
LCD_FUNCTIONSET = 0x20
LCD_SETCGRAMADDR = 0x40
LCD_SETDDRAMADDR = 0x80

# flags for display entry mode
LCD_ENTRYRIGHT = 0x00
LCD_ENTRYLEFT = 0x02
LCD_ENTRYSHIFTINCREMENT = 0x01
LCD_ENTRYSHIFTDECREMENT = 0x00

# flags for display on/off control
LCD_DISPLAYON = 0x04
LCD_DISPLAYOFF = 0x00
LCD_CURSORON = 0x02
LCD_CURSOROFF = 0x00
LCD_BLINKON = 0x01
LCD_BLINKOFF = 0x00

# flags for display/cursor shift
LCD_DISPLAYMOVE = 0x08
LCD_CURSORMOVE = 0x00
LCD_MOVERIGHT = 0x04
LCD_MOVELEFT = 0x00

# flags for function set
LCD_8BITMODE = 0x10
LCD_4BITMODE = 0x00
LCD_2LINE = 0x08
LCD_1LINE = 0x00
LCD_5x10DOTS = 0x04
LCD_5x8DOTS = 0x00

# Define LCD device constants
LCD_WIDTH = 16    # Default characters per line
LCD_CHR = True
LCD_CMD = False

LCD_LINE_1 = 0x80 # LCD RAM address for the 1st line
LCD_LINE_2 = 0xC0 # LCD RAM address for the 2nd line
LCD_LINE_3 = 0x94 # LCD RAM address for the 3rd line
LCD_LINE_4 = 0xD4 # LCD RAM address for the 4th line

# flags for backlight control
LCD_BACKLIGHT = 0x08
LCD_NOBACKLIGHT = 0x00

En = 0b00000100 # Enable bit
Rw = 0b00000010 # Read/Write bit
Rs = 0b00000001 # Register select bit

class lcd:
   #initializes objects and lcd
   def __init__(self):
      self.lcd_device = i2c_device(ADDRESS)

      self.lcd_write(0x03)
      self.lcd_write(0x03)
      self.lcd_write(0x03)
      self.lcd_write(0x02)

      self.lcd_write(LCD_FUNCTIONSET | LCD_2LINE | LCD_5x8DOTS | LCD_4BITMODE)
      self.lcd_write(LCD_DISPLAYCONTROL | LCD_DISPLAYON)
      self.lcd_write(LCD_CLEARDISPLAY)
      self.lcd_write(LCD_ENTRYMODESET | LCD_ENTRYLEFT)

      self._displaycontrol = LCD_DISPLAYCONTROL | LCD_DISPLAYON | LCD_CURSORON | LCD_BLINKON

      sleep(0.2)
      self.width = LCD_WIDTH
      self.ScrollSpeed = 0.3       # Default scroll speed


   # clocks EN to latch command
   def lcd_strobe(self, data):
      self.lcd_device.write_cmd(data | En | LCD_BACKLIGHT)
      sleep(.0005)
      self.lcd_device.write_cmd(((data & ~En) | LCD_BACKLIGHT))
      sleep(.0001)

   def lcd_write_four_bits(self, data):
      self.lcd_device.write_cmd(data | LCD_BACKLIGHT)
      self.lcd_strobe(data)

   # write a command to lcd
   def lcd_write(self, cmd, mode=0):
      self.lcd_write_four_bits(mode | (cmd & 0xF0))
      self.lcd_write_four_bits(mode | ((cmd << 4) & 0xF0))

   # write a character to lcd (or character rom) 0x09: backlight | RS=DR<
   # works!
   def lcd_write_char(self, charvalue, mode=1):
      self.lcd_write_four_bits(mode | (charvalue & 0xF0))
      self.lcd_write_four_bits(mode | ((charvalue << 4) & 0xF0))

# Set the display width
   def setWidth(self,width):
	self.width = width
	return
  
   def setPosition(self, line, pos):
	pos=pos-1
	if pos<0:
		pos=0
	address=0
	if line == 1:
		address = pos
	elif line == 2:
		address = 0x40 + pos
	elif line == 3:
		address = 0x14 + pos
	elif line == 4:
		address = 0x54 + pos
	self.lcd_write(0x80 + address)

   # put string function
   def lcd_display_string(self, string, line):
      if line == 1:
         self.lcd_write(0x80)
      if line == 2:
         self.lcd_write(0xC0)
      if line == 3:
         self.lcd_write(0x94)
      if line == 4:
         self.lcd_write(0xD4)

      for char in string:
         self.lcd_write(ord(char), Rs)

   def writeString(self, string):
      for char in string:
         self.lcd_write(ord(char), Rs)

   # clear lcd and set to home
   def lcd_clear(self):
      self.lcd_write(LCD_CLEARDISPLAY)
      self.lcd_write(LCD_RETURNHOME)

   def home(self):
      self.lcd_write(LCD_RETURNHOME)
      sleep(0.1)

   # define backlight on/off (lcd.backlight(1); off= lcd.backlight(0)
   def backlight(self, state): # for state, 1 = on, 0 = off
      if state == 1:
         self.lcd_device.write_cmd(LCD_BACKLIGHT)
      elif state == 0:
         self.lcd_device.write_cmd(LCD_NOBACKLIGHT)

   # add custom characters (0 - 7)
   def lcd_load_custom_chars(self, fontdata):
      self.lcd_write(0x40);
      for char in fontdata:
         for line in char:
            self.lcd_write_char(line)         
         
   # define precise positioning (addition from the forum)
   def lcd_display_string_pos(self, string, line, pos =0):
    """
    if line == 1:
      pos_new = pos
    elif line == 2:
      pos_new = 0x40 + pos
    elif line == 3:
      pos_new = 0x14 + pos
    elif line == 4:
      pos_new = 0x54 + pos
    self.lcd_write(0x80 + pos_new)
    """
    self.setPosition(line,pos)

    for char in string:
	self.lcd_write(ord(char), Rs)

   def message(self, text):
	for char in text:
		if char == '\n':
			self.lcd_write(0xC0)
		else:
			self.lcd_write_char(ord(char))

# Write a single line to the LCD
   def _writeLine(self,line,text):
	self.setPosition(line,0)
	if len(text) < self.width:
		text = text.ljust(self.width, ' ')
	self.message(text[:self.width])
	return

# Display Line 1 on LCD
   def line1(self,text):
	self.lcd_display_string_pos(text, 1)
	return

# Display Line 2 on LCD
   def line2(self,text):
	self.lcd_display_string_pos(text, 2)
	return

# Display Line 3 on LCD
   def line3(self,text):
	self.lcd_display_string_pos(text, 3)
	return

# Display Line 4 on LCD
   def line4(self,text):
	self.lcd_display_string_pos(text, 4)
	return

# Write a single line to the LCD
   def _writeLine(self,line,text):
	self.lcd_write(line)
	if len(text) < self.width:
		text = text.ljust(self.width, ' ')
	self.message(text[:self.width])
	return

# Set Scroll line speed - Best values are 0.2 and 0.3
# Limit to between 0.05 and 1.0
   def setScrollSpeed(self,speed):
	if speed < 0.05:
		speed = 0.2
	elif speed > 1.0:
		speed = 0.3
	self.ScrollSpeed = speed
	return

# Scroll message on line 1
   def scroll1(self,mytext,interrupt = 0):
	self._scroll(mytext,LCD_LINE_1,interrupt)
	return

	# Scroll message on line 2
   def scroll2(self,mytext,interrupt = 0):
	self._scroll(mytext,LCD_LINE_2,interrupt)
	return

	# Scroll message on line 3
   def scroll3(self,mytext,interrupt = 0):
	self._scroll(mytext,LCD_LINE_3,interrupt)
	return

	# Scroll message on line 4
   def scroll4(self,mytext,interrupt = 0):
	self._scroll(mytext,LCD_LINE_4,interrupt)
	return


# Scroll line - interrupt() breaks out routine if True
   def _scroll(self,mytext,line,interrupt = 0):
	ilen = len(mytext)
	skip = False

	self._writeLine(line,mytext[0:self.width + 1])
	if (ilen <= self.width):
		skip = True
	if not skip:
		for i in range(0, 5):
			sleep(0.2)

	if not skip:
		for i in range(0, ilen - self.width + 1 ):
			self._writeLine(line,mytext[i:i+self.width])
			sleep(self.ScrollSpeed)

	if not skip:
		for i in range(0, 5):
			sleep(0.2)
	return

	# Set the display width
   def setWidth(self,width):
	self.width = width
	return


# Blink cursor
   def blink(self, on):
	if on:
		self._displaycontrol |= LCD_BLINKON
	else:
		self._displaycontrol &= ~LCD_BLINKON
	self.lcd_write(self._displaycontrol)

   def noCursor(self):
	self._displaycontrol &= ~LCD_CURSORON
	self.lcd_write(self._displaycontrol)

   def cursor(self, on):
	if on:
		self._displaycontrol |= LCD_CURSORON
	else:
		self._displaycontrol &= ~LCD_CURSORON
	self.lcd_write(self._displaycontrol)

