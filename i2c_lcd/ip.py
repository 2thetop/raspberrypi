#!/usr/bin/python
# Original code found at:
# https://gist.github.com/DenisFromHR/cc863375a6e19dce359d
# IP_Script Developed by: AndyPi (http://andypi.co.uk/), modified by zzeromin

# requires I2C_LCD_driver.py

import I2C_LCD_driver
from sys import exit
from time import *
from subprocess import *

def run_cmd(cmd):
        # runs whatever is in the cmd variable in the terminal
        p = Popen(cmd, shell=True, stdout=PIPE)
        output = p.communicate()[0]
        return output

# get ip address of eth0 connection (use wlan0 for wireless)
cmd = "ip addr show eth0 | grep 'inet ' | awk '{print $2}' | cut -d/ -f1"
ipaddr = run_cmd(cmd)[:-1] # set output of command into ipaddr variable

mylcd = I2C_LCD_driver.lcd()
mylcd.lcd_display_string("IP address:", 1)
mylcd.lcd_display_string(ipaddr, 2)
sleep(2) # 2 sec delay
