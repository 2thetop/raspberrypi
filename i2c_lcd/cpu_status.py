#!/usr/bin/python
# Original code found at:
# https://gist.github.com/DenisFromHR/cc863375a6e19dce359d
# modified by zzeromin

# requires I2C_LCD_driver.py


import I2C_LCD_driver
import os
from time import sleep

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

while 1:
	mylcd.lcd_display_string("CPU Temp: " + str( round( get_cpu_temp() ) ), 1)
	mylcd.lcd_display_string("CPU Speed: " + str( round( get_cpu_speed() ) ), 2)
	sleep(2)
