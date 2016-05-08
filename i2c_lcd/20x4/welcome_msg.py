#!/usr/bin/python
# Original code found at:
# https://github.com/zzeromin/raspberrypi/tree/master/i2c_lcd
# requires I2C_LCD_driver.py

import I2C_LCD_driver
from time import *

mylcd = I2C_LCD_driver.lcd()
mylcd.lcd_display_string(" Welcome RAS Hi-Pi", 1)
mylcd.lcd_display_string(" Mutimedia System", 2)
mylcd.lcd_display_string("Made by rasplay.org", 3)
mylcd.lcd_display_string("RaspberryPi Village", 4)
sleep(2) # 2 sec delay
