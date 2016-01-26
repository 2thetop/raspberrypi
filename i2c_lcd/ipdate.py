#!/usr/bin/python
# Original code found at:
# https://gist.github.com/DenisFromHR/cc863375a6e19dce359d
# IP_Script Developed by: AndyPi (http://andypi.co.uk/), modified by zzeromin

# requires I2C_LCD_driver.py

import I2C_LCD_driver
from sys import exit
from subprocess import *
from time import sleep, strftime
from datetime import datetime

def run_cmd(cmd):
  # runs whatever is in the cmd variable in the terminal
  p = Popen(cmd, shell=True, stdout=PIPE)
  output = p.communicate()[0]
  return output

# get ip address of eth0 connection (use wlan0 for wireless)
cmd = "ip addr show eth0 | grep 'inet ' | awk '{print $2}' | cut -d/ -f1"

mylcd = I2C_LCD_driver.lcd()

mylcd.lcd_clear()


while 1:
  ipaddr = run_cmd(cmd)
  mylcd.lcd_display_string(datetime.now().strftime('%b %d  %H:%M:%S\n'), 1)
  mylcd.lcd_display_string('IP  %s' %(ipaddr), 2)
  sleep(2)

