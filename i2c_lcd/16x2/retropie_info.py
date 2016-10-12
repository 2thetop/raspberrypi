#!/usr/bin/python
# reference:  https://github.com/retropie/retropie-setup/wiki/runcommand
# written by zzeromin, member of Raspberrypi Village
# http://www.rasplay.org, http://forums.rasplay.org/
# requires I2C_LCD_driver.py
#
#    Small script written in Python for Retropie project (https://retropie.org.uk/) 
#    running on Raspberry Pi 2,3, upper Retropie V4.0.2, which displays all neccessary info on a 16x2 LCD display
#    Features
#    - Emulation amd ROM information

import I2C_LCD_driver
from time import *

mylcd = I2C_LCD_driver.lcd()
mylcd.lcd_clear()

while 1:
   sec = 0
   while ( sec < 5 ) :
      # show system & rom file information

      try:
         f = open('/dev/shm/runcommand.log', 'r')
#      except FileNotFoundError:
      except IOError:
         mylcd.lcd_display_string( "You should play", 1 )
         mylcd.lcd_display_string( "a game first!!", 2 )
         sleep(3)
         break
         pass
      else:
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

         mylcd.lcd_display_string( "%s" %(system), 1 )
         mylcd.lcd_display_string( "%s" %(rom), 2 )
         sec = sec + 1
         sleep(1)
         
