#!/usr/bin/python
# Original code found at:
# https://github.com/zzeromin/raspberrypi/tree/master/i2c_lcd
# requires I2C_LCD_driver.py

import I2C_LCD_driver
from time import *

mylcd = I2C_LCD_driver.lcd()
mylcd.lcd_display_string("PI ALL IN ONE", 1)
mylcd.lcd_display_string("www.rasplay.org", 2)
sleep(2) # 2 sec delay
