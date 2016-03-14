#!/usr/bin/python
# Original code found at:
# https://gist.github.com/DenisFromHR/cc863375a6e19dce359d
# IP_Script Developed by: AndyPi (http://andypi.co.uk/), xplod(https://github.com/RandyCupic/RuneAudioLCD)
# edited by zzeromin
# requires I2C_LCD_driver.py

import I2C_LCD_driver
import os
import socket, fcntl, struct
from sys import exit
from subprocess import *
from time import *
from datetime import datetime

LCD_COLUMNS = 20
LCD_ROWS = 4

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

# Get IP addresses to show on screen: ifname = eth0 | ifname = wlan0
def get_ip_address(ifname):
   s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
   try:
      return socket.inet_ntoa(fcntl.ioctl(
         s.fileno(),
         0x8915,  # SIOCGIFADDR
         struct.pack('256s', ifname)
      )[20:24])
   except IOError:
      return ''

mylcd = I2C_LCD_driver.lcd()
mylcd.lcd_clear()

# Ethernet: 'eth0', Wireless: 'wlan0'
ethip = get_ip_address('eth0')
wifiip = get_ip_address('wlan0')
temp = ''

if ( ethip == '' ):
   if ( wifiip == '' ):
      ipaddr = 'disconnected'
   else:
      ipaddr = chr(4) + ' ' + wifiip
else:
   ipaddr = chr(3) + ' ' + ethip

old_Temp = new_Temp = get_cpu_temp()
old_Speed = new_Speed = get_cpu_speed()

# Will remaining space with ' '
ipspace = ''
ip = "IP"
for i in range( len(ip), LCD_COLUMNS - len(ipaddr) ):
   ipspace += ' '


while 1:
###IP & DATE information
#   print datetime.now().strftime( "%Y %b %d %H:%M:%S" )
#   print "IP " + str( ipaddr )
   mylcd.lcd_display_string( datetime.now().strftime( "%Y %b %d %H:%M:%S" ), 1 )
   mylcd.lcd_display_string( ip + ipspace + str( ipaddr ), 2 ) # ethip or wifiip

###cpu Temp & Speed information
   new_Temp = int( round( get_cpu_temp() ) )
   new_Speed = int( get_cpu_speed() )

   # Will remaining space with ' '
   tempspace = ''
   cpuTemp = "CPU TEMP"
   for i in range( len(cpuTemp), LCD_COLUMNS - 2 - len(str(new_Temp)) ):
      tempspace += ' '

   # Will remaining space with ' '
   speedspace = ''
   cpuSpeed = "CPU SPEED"
   for i in range( len(cpuSpeed), LCD_COLUMNS - len(str(new_Speed)) ):
      speedspace += ' '

   if old_Temp != new_Temp or old_Speed != new_Speed :
      old_Temp = new_Temp
      old_Speed = new_Speed
#      print "CPU Temp: " + str( new_Temp )
#      print "CPU Speed: " + str( new_Speed )
      mylcd.lcd_display_string( cpuTemp + tempspace+ str( new_Temp ) + chr(223) + 'C', 3 )
      mylcd.lcd_display_string( cpuSpeed + speedspace+ str( new_Speed ),4 )
