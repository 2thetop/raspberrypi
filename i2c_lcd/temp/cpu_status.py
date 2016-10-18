#!/usr/bin/python
# Original code found at:
# https://gist.github.com/DenisFromHR/cc863375a6e19dce359d
# edited by zzeromin
# requires I2C_LCD_driver.py

import I2C_LCD_driver
import os
from time import *

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

old_Temp = new_Temp = get_cpu_temp()
old_Speed = new_Speed = get_cpu_speed()

while 1:
   new_Temp = get_cpu_temp()
   new_Speed = get_cpu_speed()

   if old_Temp != new_Temp or old_Speed != new_Speed :
      old_Temp = new_Temp
      old_Speed = new_Speed
      print "CPU Temp: " + str( new_Temp )
      print "CPU Speed: " + str( new_Speed )
      mylcd.lcd_display_string("CPU Temp: " + str( new_Temp ), 1)
      mylcd.lcd_display_string("CPU Speed: " + str( round( get_cpu_speed() ) ), 2)
      sleep(1)
