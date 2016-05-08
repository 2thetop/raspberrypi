#!/usr/bin/python
# Original code found at:
# https://github.com/zzeromin/raspberrypi/tree/master/i2c_lcd
# requires I2C_LCD_driver.py

import I2C_LCD_driver
from time import *
import os

mylcd = I2C_LCD_driver.lcd()
mylcd.lcd_clear()

mylcd.lcd_display_string("", 1)
mylcd.lcd_display_string("Your RAS Hi-Pi will", 2)
mylcd.lcd_display_string("restart in 1 minute", 3)
mylcd.lcd_display_string("", 4)
sleep(3) # 3 sec delay

os.system("shutdown now -r")
