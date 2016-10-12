#!/usr/bin/python
#    Reference:  https://github.com/retropie/retropie-setup/wiki/runcommand
#    https://gist.github.com/DenisFromHR/cc863375a6e19dce359d
#    IP_Script Developed by: AndyPi (http://andypi.co.uk/)
#    written by zzeromin, member of Raspberrypi Village
#    http://www.rasplay.org, http://forums.rasplay.org/
#    requires I2C_LCD_driver.py
#
#    Small script written in Python for Retropie project (https://retropie.org.uk/) 
#    running on Raspberry Pi 2,3, which displays all neccessary info on a 16x2 LCD display
#    Features
#    1. Current date and time, IP address of eth0, wlan0
#    2. CPU temperature and speed
#    3. Emulation amd ROM information

import I2C_LCD_driver
import os
from sys import exit
from subprocess import *
from time import *
from datetime import datetime

def run_cmd(cmd):
   # runs whatever is in the cmd variable in the terminal
   p = Popen(cmd, shell=True, stdout=PIPE)
   output = p.communicate()[0]
   return output

def get_cpu_temp():
   tempFile = open("/sys/class/thermal/thermal_zone0/temp")
   cpu_temp = tempFile.read()
   tempFile.close()
   return float(cpu_temp)/1000

def get_cpu_speed():
   tempFile = open("/sys/devices/system/cpu/cpu0/cpufreq/scaling_cur_freq")
   cpu_speed = tempFile.read()
   tempFile.close()
   return float(cpu_speed)/1000

mylcd = I2C_LCD_driver.lcd()
mylcd.lcd_clear()

#get ip address of eth0 connection
cmd = "ip addr show eth0 | grep 'inet ' | awk '{print $2}' | cut -d/ -f1"
#get ip address of wlan0 connection
#cmd = "ip addr show wlan0 | grep 'inet ' | awk '{print $2}' | cut -d/ -f1"

old_Temp = new_Temp = get_cpu_temp()
old_Speed = new_Speed = get_cpu_speed()

while 1:
   mylcd.lcd_clear()
   sec = 0
   while ( sec < 5 ) :
      # ip & date information
      ipaddr = run_cmd(cmd)
      ipaddr = ipaddr.replace("\n","")
      #print datetime.now().strftime( "%b %d  %H:%M:%S" )
      #print "IP " + str( ipaddr )
      mylcd.lcd_display_string( datetime.now().strftime( "%b %d  %H:%M:%S" ), 1 )
      mylcd.lcd_display_string( "IP %s" %(ipaddr), 2 )
      sec = sec + 1
      sleep(1)

   mylcd.lcd_clear()
   sec = 0
   while ( sec < 5 ) :
      # cpu Temp & Speed information
      new_Temp = get_cpu_temp()
      new_Speed = int( get_cpu_speed() )

      if old_Temp != new_Temp or old_Speed != new_Speed :
         old_Temp = new_Temp
         old_Speed = new_Speed
         #print "CPU Temp: " + str( new_Temp )
         #print "CPU Speed: " + str( new_Speed )
         mylcd.lcd_display_string( "CPU Temp: " + str( new_Temp ), 1 )
         mylcd.lcd_display_string( "CPU Speed: " + str( new_Speed ), 2 )
         sec = sec + 1  
         sleep(1)

   mylcd.lcd_clear()
   sec = 0
   while ( sec < 5 ) :
      # show system & rom file information

      try:
         f = open('/dev/shm/runcommand.log', 'r')
#      except FileNotFoundError:
      except IOError:
         mylcd.lcd_display_string( "nothing to show", 1 )
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
