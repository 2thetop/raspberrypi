# -*- coding: utf-8 -*-

#########      I2C LCD DISPLAY FOR RUNE AUDIO    #########
# Origionally Written by: Randy Cupic (XploD)            #
# Hacked by Ken Robson (Hairybiker) to include i2c       #
##########################################################

##########  IMPORTS  ##########
import RPi_I2C_driver as LCD
from mpd import (MPDClient, CommandError)
from socket import error as SocketError
import sys
import time
import threading
import urllib2
import subprocess
import re
import os
import string
from datetime import datetime
###############################


# Specify LCD size
# WARNING: This script works with lcd_columnsx2 LCD, using any other may not work
lcd_columns = 16
lcd_rows = 2

# WARNING: By decreasing scrolling_period, CPU usage increases fast
scrolling_period = 25 # x10, scroll every 20x10 = 200 ms

# When the song changes, how much time will pass before start scrolling
scrolling_start = 100 # x10, start after 100x10 = 1000 ms (1 second)

# If you don't want to scroll web radio station name, put to false
webradio_scroll = True

# How much the volume status screen will last before returning to displaying current song
volume_screen_duration = 300 # x10, it will last for 300x10 = 3000 ms (3 seconds)

#########################################################################################

#########  MPD PARAMETERS  ##############
# Only if you know what you're doing! 	#
HOST = 'localhost'						#
PORT = '6600'							#
PASSWORD = False						#
CON_ID = {'host':HOST, 'port':PORT}		#
#########################################

# Initialize LCD
lcd = LCD.lcd()
lcd.setWidth(lcd_columns)
							
# MPD client object instance2
client = MPDClient()
client_cntrl = MPDClient()

# Current data
# state: 0 (for stopped), 1 (for playing), 2 (for paused)
# artist: artist name (for files), radio name (for radio stations)
# song: song name (for files), ARTIST - SONG (for radio stations, if available)
# type: 0 (for files), 1 (for radio)
data = {'state': 0, 'artist': '', 'title': '', 'type': 0, 'volume': 0}

data_changed = False; # Used to indicate that data has changed to LCD display thread
data_changed_vol = False; # Used to indicate that volume has changed to LCD display thread

#################### DECODING STRING for non unicode-characters ###########################
# Currently, only ë will be replaced by e, all others will be replaced by space           #
# You can enable desired ones by removing the # character in front of it                  #
def char_decode(string):
	# string = string.replace('À', 'A')
	# string = string.replace('Á', 'A')
	# string = string.replace('Â', 'A')
	# string = string.replace('Ã', 'A')
	# string = string.replace('Ä', 'A')
	# string = string.replace('Å', 'A')
	# string = string.replace('Æ', 'A')
	# string = string.replace('Ç', 'C')
	# string = string.replace('È', 'E')
	# string = string.replace('É', 'E')
	# string = string.replace('Ê', 'E')
	# string = string.replace('Ë', 'E')
	# string = string.replace('Ì', 'I')
	# string = string.replace('Í', 'I')
	# string = string.replace('Î', 'I')
	# string = string.replace('Ï', 'I')
	# string = string.replace('Ð', 'D')
	# string = string.replace('Ñ', 'N')
	# string = string.replace('Ò', 'O')
	# string = string.replace('Ó', 'O')
	# string = string.replace('Ô', 'O')
	# string = string.replace('Õ', 'O')
	# string = string.replace('Ö', 'O')
	# string = string.replace('×', 'X')
	# string = string.replace('Ø', 'O')
	# string = string.replace('Ù', 'U')
	# string = string.replace('Ú', 'U')
	# string = string.replace('Û', 'U')
	# string = string.replace('Ü', 'U')
	# string = string.replace('Ý', 'Y')
	# string = string.replace('à', 'a')
	# string = string.replace('á', 'a')
	# string = string.replace('â', 'a')
	# string = string.replace('ã', 'a')
	# string = string.replace('ä', 'a')
	# string = string.replace('å', 'a')
	# string = string.replace('æ', 'a')
	# string = string.replace('ç', 'c')
	# string = string.replace('è', 'e')
	# string = string.replace('é', 'e')
	# string = string.replace('ê', 'e')
	string = string.replace('ë', 'e')
	# string = string.replace('ì', 'i')
	# string = string.replace('í', 'i')
	# string = string.replace('î', 'i')
	# string = string.replace('ï', 'i')
	# string = string.replace('ð', 'd')
	# string = string.replace('ñ', 'n')
	# string = string.replace('ò', 'o')
	# string = string.replace('ó', 'o')
	# string = string.replace('ô', 'o')
	# string = string.replace('õ', 'o')
	# string = string.replace('ö', 'o')
	# string = string.replace('ø', 'o')
	# string = string.replace('ù', 'u')
	# string = string.replace('ú', 'u')
	# string = string.replace('û', 'u')
	# string = string.replace('ü', 'u')
	# string = string.replace('ý', 'y')
	# string = string.replace('þ', 'p')
	# string = string.replace('ÿ', 'y')
	
	strip_unicode = re.compile("([^-_a-zA-Z0-9!@#%&=,/'\";:~`\$\^\*\(\)\+\[\]\.\{\}\|\?\<\>\\]+|[^\s]+)")
	return strip_unicode.sub('', string.decode('unicode-escape'))

	
# Function used by LCD thread to update the LCD
def update_lcd():
	global data
	global data_changed
	global data_changed_vol
	framebuffer = ['','']
	direction = [0, 0]
	counter = [0, 0]
	vol_count = 0
	vol_screen = False
	counters = [0, 0]
	
	# Create a square to print for volume
	block = chr(255) # block character, built-in
	
	# For the first run, data has definitely changed
	old_data = data
	
	while True:
		time.sleep(0.01) # One quant of time (10 ms)
	
		# Check if data has changed
		if (data_changed == True):
			direction = [0, 0] # Reset directions
			counter = [0, 0] # Reset counters
			old_data = data # Update data
			
			# If artist length is less than lcd_columns ...
			if (len(old_data['artist']) < lcd_columns):
				framebuffer[0] = old_data['artist']
			
				# ... fill empty places with spaces
				for i in range(lcd_columns - len(old_data['artist'])):
					framebuffer[0] += ' '
			
			# Else if it's lcd_columns, take it as it is
			elif (len(old_data['artist']) == lcd_columns):
				framebuffer[0] = old_data['artist']
			
			# Else use only first lcd_columns characters
			else:
				framebuffer[0] = old_data['artist'][0:lcd_columns]
			
			# If title length is less than lcd_columns ...
			if (len(old_data['title']) < lcd_columns):
				framebuffer[1] = old_data['title']
			
				# Fill empty places with spaces
				for i in range(lcd_columns - len(old_data['title'])):
					framebuffer[1] += ' '
			
			# Else if it's lcd_columns, take it as it is
			elif (len(old_data['title']) == lcd_columns):
				framebuffer[1] = old_data['title']
			
			# Else use only first lcd_columns characters			
			else:
				framebuffer[1] = old_data['title'][0:lcd_columns]
			
			# Write data to LCD
			lcd.line1(framebuffer[0])
			lcd.line2(framebuffer[1])	
			
			data_changed = False
			vol_screen = False
			vol_count = 0
			counters[1] = scrolling_start # Wait a while before start scrolling
			continue				

		# Check if volume has changed
		if (data_changed_vol == True):
			vol_screen = True
			vol_count = volume_screen_duration
			data_changed_vol = False
			
			# Prepare strings to write to LCD
			vol_string = "Volume"
			if (data['volume'] == 100):
				vol_string += "       MAX"
			elif (data['volume'] >= 10):
				vol_string += "      "
				vol_string += `data['volume']`
				vol_string += " %"
			elif (data['volume'] == 0):
				vol_string += "       MIN"
			else:
				vol_string += "       "
				vol_string += `data['volume']`
				vol_string += " %"
				
			if (data['volume'] == 0):
				vol_string2 = "                "
			elif (data['volume'] == 100):
				vol_string2 = ""
				for i in range (0,lcd_columns):
					vol_string2 += block
			else:
				vol_string2 = ""
				pom_num = (data['volume']/7)+1
				for i in range (0,pom_num):
					vol_string2 += block
					
				for i in range (0, (lcd_columns-pom_num)):
					vol_string2 += " "
				
			# Write to LCD
			lcd.line1(vol_string)
			lcd.line2(vol_string2)
			continue
		
		
		if (vol_screen == True):
			if (vol_count == 0):
				vol_screen = False
				vol_count = 0
				direction = [0, 0] # Reset directions
				counter = [0, 0] # Reset counters
				counters[1] = 0
			else:
				vol_count -= 1
			continue
		
		# If it's stopped, just display it
		if (old_data['state'] == 0):
			framebuffer[0] = '    STOPPED     '
			framebuffer[1] = '                '
			
			lcd.line1(framebuffer[0])
			lcd.line2(framebuffer[1])			
			continue;
			
			
		# Same for paused
		elif (old_data['state'] == 2):
			framebuffer[0] = '     PAUSED     '
			framebuffer[1] = '                '
			
			lcd.line1(framebuffer[0])
			lcd.line2(framebuffer[1])
			continue;
			
		# Jay, it's playing
		elif (old_data['state'] == 1):
			if (counters[1] > 0):
				counters[1] -= 1
				continue;
	
			# Our artist name is too long, let it scroll
			if (len(old_data['artist']) > lcd_columns):
				if (old_data['type'] == 0 or (old_data['type'] == 1 and webradio_scroll == True)):
					framebuffer[0] = old_data['artist'][counter[0]:counter[0]+lcd_columns]
					
					# First, we scroll upwards
					if (direction[0] == 0):
						# If we've reached the end, let us go backwards
						if (counter[0] == (len(old_data['artist']) - lcd_columns)):
							direction[0]= 1
						else:
							counter[0] += 1
					
					# Scroll backwards
					else:
						# If we've reached the beginning, let us go forwards
						if (counter[0] == 0):
							direction[0]= 0
						else:
							counter[0] -= 1
						
				# It's a radio, no need to scroll it (if it's disabled)
				elif (old_data['type'] == 1 and webradio_scroll == False):
					framebuffer[0] = old_data['artist'][0:lcd_columns] # Took first lcd_columns chars
			
			# Our artist name fits screen length
			elif (len(old_data['artist']) == lcd_columns):
				framebuffer[0] = old_data['artist']
			
			# Else it's smaller than screen length
			else:
				framebuffer[0] = old_data['artist']
				
				# Fill empty places with spaces
				for i in range(lcd_columns - len(old_data['artist'])):
					framebuffer[0] += ' '
					
			# Our song title is too long, let it scroll		
			if (len(old_data['title']) > lcd_columns):
				framebuffer[1] = old_data['title'][counter[1]:counter[1]+lcd_columns]
				
				# First, we scroll upwards
				if (direction[1] == 0):
					# If we've reached the end, let us go backwards
					if (counter[1] == (len(old_data['title']) - lcd_columns)):
						direction[1]= 1
					else:
						counter[1] += 1
				
				# Scroll backwards
				else:
					# If we've reached the beginning, let us go forwards
					if (counter[1] == 0):
						direction[1]= 0
					else:
						counter[1] -= 1
			
			# Our song title fits screen length
			elif (len(old_data['title']) == lcd_columns):
				framebuffer[1] = old_data['title']
			
			# Else it's smaller than screen length			
			else:
				framebuffer[1] = old_data['title']
				
				# Fill empty places with spaces
				for i in range(lcd_columns - len(old_data['title'])):
					framebuffer[1] += ' '
		
			# Time to write our information on the screen
			lcd.line1(framebuffer[0])
			lcd.line2(framebuffer[1])
			counters[1] = scrolling_period # Let it sleep, we don't want to scroll it too fast

######  MPD CLIENT FUNCTIONS  #######			
def mpdConnect(client, con_id):		#
    """								#
    Simple wrapper to connect MPD.	#
    """								#
    try:							#
        client.connect(**con_id)	#
    except SocketError:				#
        return False				#
    return True						#
									#
def mpdAuth(client, secret):		#
    """								#
    Authenticate					#
    """								#
    try:							#
        client.password(secret)		#
    except CommandError:			#
        return False				#
    return True						#
#####################################


'''
#########################################################################
#########################################################################
===================== MAIN PROGRAM ======================================
#########################################################################
#########################################################################
'''

# First MPD client (for status) connection
if mpdConnect(client, CON_ID):
	print('MPD Client Connected!')
else:
	print('Fail to connect to MPD server!')
	sys.exit(1)

# Auth if password is set non False
if PASSWORD:
	if mpdAuth(client, PASSWORD):
		print('Pass auth!')
	else:
		print('Error trying to pass auth.')
		client.disconnect()
		sys.exit(2)

# Second MPD client (for control) connection		
if mpdConnect(client_cntrl, CON_ID):
	print('MPD Client_Cntrl Connected!')
else:
	print('Fail to connect to MPD server!')
	sys.exit(1)

# Auth if password is set non False
if PASSWORD:
	if mpdAuth(client_cntrl, PASSWORD):
		print('Pass auth!')
	else:
		print('Error trying to pass auth.')
		client_cntrl.disconnect()
		sys.exit(2)

# LCD Thread		
lcd_t = threading.Thread(target=update_lcd, args = ()) # Create thread for updating LCD
lcd_t.daemon = True # Yep, it's a daemon, when main thread finish, this one will finish too
lcd_t.start() # Start it!

''' FIRST STATUS FETCH '''
data['volume'] = int(client.status()['volume']) # Get volume

# Get station
try:
	station = client.currentsong()['name']
except KeyError:
	station = ''

# Get title
try:
	title = client.currentsong()['title']
except KeyError:
	title = ''

# Get artist
try:
	artist = client.currentsong()['artist']
except KeyError:
	artist = ''

# Check if web radio is playing (radio station)
if(station != ''):    # webradio
	data['type'] = 1 # Set data type to radio
	
	# Get station name and current song, all first letter to uppercase
	lst = [word[0].upper() + word[1:] for word in station.split()]
	data['artist'] = " ".join(lst)
	
	lst = [word[0].upper() + word[1:] for word in title.split()]
	data['title'] = " ".join(lst)

# Else, it's a file playing
else:                 # file
	data['type'] = 0 # Set data type to file
	
	# Get artist name and current song title, all first letter to uppercase
	lst = [word[0].upper() + word[1:] for word in artist.split()]
	data['artist'] = " ".join(lst)
	
	lst = [word[0].upper() + word[1:] for word in title.split()]
	data['title'] = " ".join(lst)

# Check whether it's playing, paused or stopped and update status accordingly
if (client.status()['state'] == 'play'):
	data['state'] = 1

elif (client.status()['state'] == 'stop'):
	data['state'] = 0
	
elif (client.status()['state'] == 'pause'):
	data['state'] = 2
	
data_changed = True # Notify LCD thread about change



# Wait for any changes on MPD
while(1):				
	client.send_idle()
	state = client.fetch_idle()
	
	# Volume has changed
	if (state[0] == 'mixer'):
		data['volume'] = int(client.status()['volume']) # Update volume
		data_changed_vol = True # Notify LCD thread about change
	
	# Something other has changed (song/station or state)
	if (state[0] == 'player'):
		# Get station
		try:
			station = client.currentsong()['name']
		except KeyError:
			station = ''
		
		# Get title
		try:
			title = client.currentsong()['title']
		except KeyError:
			title = ''
	
		# Get artist
		try:
			artist = client.currentsong()['artist']
		except KeyError:
			artist = ''
		
		
		# Check if web radio is playing (radio station)
		if(station != ''):    # webradio
			data['type'] = 1 # Set data type to radio
			
			# Get station name and current song, all first letter to uppercase
			lst = [word[0].upper() + word[1:] for word in station.split()]
			data['artist'] = " ".join(lst)
			
			lst = [word[0].upper() + word[1:] for word in title.split()]
			data['title'] = " ".join(lst)

		# Else, it's a file playing
		else:                 # file
			data['type'] = 0 # Set data type to file
			
			# Get artist name and current song title, all first letter to uppercase
			lst = [word[0].upper() + word[1:] for word in artist.split()]
			data['artist'] = " ".join(lst)
			
			lst = [word[0].upper() + word[1:] for word in title.split()]
			data['title'] = " ".join(lst)

		# Check whether it's playing, paused or stopped and update status accordingly
		if (client.status()['state'] == 'play'):
			data['state'] = 1

		elif (client.status()['state'] == 'stop'):
			data['state'] = 0
			
		elif (client.status()['state'] == 'pause'):
			data['state'] = 2
			
		data_changed = True # Notify LCD thread about change

# Disconnect MPD client
client.disconnect()

# Wait for LCD thread to finish
lcd_t.join()

# Exit
sys.exit(0)
