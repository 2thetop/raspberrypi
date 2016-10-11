#!/usr/bin/python
# reference:  https://github.com/retropie/retropie-setup/wiki/runcommand
# written by zzeromin, member of Raspberrypi Village
# http://www.rasplay.org, http://forums.rasplay.org/
# requires I2C_LCD_driver.py

import I2C_LCD_driver
from time import *

mylcd = I2C_LCD_driver.lcd()
mylcd.lcd_clear()

while 1:
   sec = 0
   while ( sec < 5 ) :
       f = open('/dev/shm/runcommand.log', 'r')

       system = f.readline()
       system = system.replace("\n","")
       systemMap = {
          "gba":"GameBoy Advance",
          "mame-libretro":"MAME",
          "msx":"MSX",
          "fba":"FinalBurn Alpha",
          "nes":"Nintendo NES",
          "snes":"Super Nintendo",
       }
       system = systemMap.get(system)

       rom = f.readline()
       rom = rom.replace("\n","")

       f.close()
       
       # show system & rom file information
       mylcd.lcd_display_string( "%s" %(system), 1 )
       mylcd.lcd_display_string( "%s" %(rom), 2 )
       sec = sec + 1
       sleep(1)

   mylcd.lcd_clear()
