#!/usr/bin/python
# Original code found at:
# https://gist.github.com/DenisFromHR/cc863375a6e19dce359d
# IP_Script Developed by: AndyPi (http://andypi.co.uk/)
# modified by zzeromin
# requires I2C_LCD_driver.py

import I2C_LCD_driver
from sys import exit
from time import *
from subprocess import *

mylcd = I2C_LCD_driver.lcd()

# String 1
mylcd.lcd_display_string("Date & Time", 1)
sleep(1) # 1 sec delay
mylcd.lcd_clear()

# String 2
mylcd.lcd_display_string("Date:", 1)
mylcd.lcd_display_string("Time:", 2)

old_datetime = datetime = strftime('%Y.%m.%d %H:%M:%S')

while True:
    try:
        while old_datetime == datetime:
            sleep(0.0001)
            datetime = strftime('%Y.%m.%d %H:%M:%S')
        old_datetime = datetime
        print datetime
        mylcd.lcd_display_string(datetime[:-9], 1, 6)
        mylcd.lcd_display_string(datetime[11:], 2, 6)
    except KeyboardInterrupt:
        mylcd.backlight(0)
        print
        exit()
