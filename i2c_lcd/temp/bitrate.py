#!/usr/bin/python
# Original code found at:
# http://cafe.naver.com/audiostudy/25100 
# IP_Script Developed by: tlsrudak, modified by zzeromin

# requires I2C_LCD_driver.py
from mpd import MPDClient
import I2C_LCD_driver
from sys import exit
from time import *
from subprocess import *

client = MPDClient()               # create client object
client.timeout = 10                # network timeout in seconds (floats allowed), default: None
client.idletimeout = None          # timeout for fetching the result of the idle command is handled seperately, default:$
client.connect("localhost", 6600)  # connect to localhost:6600
currentsong = client.currentsong()

mylcd = I2C_LCD_driver.lcd()

status = client.status()
bitrate = "bitrate"
audio = "audio"

for text in status:
	if text == bitrate:
		mylcd.lcd_display_string("bitrate:", 1)
		mylcd.lcd_display_string(str(status.get(text))+"kbps", 1, 9)

for text in status:
	if text == audio:
		mylcd.lcd_display_string("audio:", 2)
		mylcd.lcd_display_string(str(status.get(text)), 2, 7)
		sleep(2) # 2 sec delay
#    print text + ": " + str(status.get(text))

client.close()                     # send the close command
client.disconnect()                # disconnect from the server
