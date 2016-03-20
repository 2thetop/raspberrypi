#!/usr/bin/python
# Original code found at:
# https://gist.github.com/DenisFromHR/cc863375a6e19dce359d
# IP_Script Developed by: AndyPi (http://andypi.co.uk/)
# edited by zzeromin
# requires I2C_LCD_driver.py

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
   while ( sec<4 ) :
	   # ip & date information
	   ipaddr = run_cmd(cmd)
	   print datetime.now().strftime( "%b %d  %H:%M:%S" )
	   print "IP " + str( ipaddr )
	   mylcd.lcd_display_string( datetime.now().strftime( "%b %d  %H:%M:%S" ), 1 )
	   mylcd.lcd_display_string( "IP  %s" %(ipaddr), 2 )
       sec++;
	   sleep(1)

   # cpu Temp & Speed information
   new_Temp = get_cpu_temp()
   new_Speed = get_cpu_speed()

   if old_Temp != new_Temp or old_Speed != new_Speed :
      old_Temp = new_Temp
      old_Speed = new_Speed
      print "CPU Temp: " + str( new_Temp )
      print "CPU Speed: " + str( new_Speed )
      mylcd.lcd_display_string( "CPU Temp: " + str( new_Temp ), 1 )
      mylcd.lcd_display_string( "CPU Speed: " + str( new_Speed ), 2 )
      sleep(5)
