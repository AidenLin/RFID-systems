### add-new-user.py -- Andrew R Gross -- 2019-03-13
### This program allows users to associate their name with an RFID code

### Header
import sys
import csv
import datetime
import os
import subprocess
from gpiozero import LED
from time import sleep

led = LED(17)

### Import whitelist

with open('/home/pi/RFID/keyed-members') as whitelist:
	csv_reader = csv.reader(whitelist, delimiter=',')
	line_count = 0
	ID_list = []
	names_list = []
	for row in csv_reader:
		ID = row[0]
		first_name = row[2]
		last_name = row[1]
		full_name = first_name+' '+last_name
		ID_list.append(ID)
		names_list.append(full_name)

### Request name

print('Please enter your first name:')
name_first = raw_input()

print('Please enter your last name:')
name_last = raw_input()

print('Please swipe your new RFID tag across the door RFID reader.')


### Read RFID input

hid = { 4: 'a', 5: 'b', 6: 'c', 7: 'd', 8: 'e', 9: 'f', 10: 'g', 11: 'h', 12: 'i', 13: 'j', 14: 'k', 15: 'l', 16: 'm', 17: 'n', 18: 'o', 19: 'p', 20: 'q', 21: 'r', 22: 's', 23: 't', 24: 'u', 25: 'v', 26: 'w', 27: 'x', 28: 'y', 29: 'z', 30: '1', 31: '2', 32: '3', 33: '4', 34: '5', 35: '6', 36: '7', 37: '8', 38: '9', 39: '0', 44: ' ', 45: '-', 46: '=', 47: '[', 48: ']', 49: '\\', 51: ';' , 52: '\'', 53: '~', 54: ',', 55: '.', 56: '/'  }
hid2 = { 4: 'A', 5: 'B', 6: 'C', 7: 'D', 8: 'E', 9: 'F', 10: 'G', 11: 'H', 12: 'I', 13: 'J', 14: 'K', 15: 'L', 16: 'M', 17: 'N', 18: 'O', 19: 'P', 20: 'Q', 21: 'R', 22: 'S', 23: 'T', 24: 'U', 25: 'V', 26: 'W', 27: 'X', 28: 'Y', 29: 'Z', 30: '!', 31: '@', 32: '#', 33: '$', 34: '%', 35: '^', 36: '&', 37: '*', 38: '(', 39: ')', 44: ' ', 45: '_', 46: '+', 47: '{', 48: '}', 49: '|', 51: ':' , 52: '"', 53: '~', 54: '<', 55: '>', 56: '?'  }
fp = open('/dev/hidraw0', 'rb')
ss = ""
shift = False
done = False
program_done = False

while not program_done:
	while not done:		## Get the character from the HID
		buffer = fp.read(8)
		for c in buffer:
			if ord(c) > 0:	##  40 is carriage return which signifies we are done looking for characters
				if int(ord(c)) == 40:
					done = True
					break;	##  If we are shifted then we have to  use the hid2 characters.
				if shift: 	## If it is a '2' then it is the shift key
					if int(ord(c)) == 2 :
						shift = True	## if not a 2 then lookup the mapping
					else:
						ss += hid2[ int(ord(c)) ]
						shift = False	##  If we are not shifted then use the hid characters
				else:				## If it is a '2' then it is the shift key
					if int(ord(c)) == 2 :
						shift = True	## if not a 2 then lookup the mapping
					else:
						ss += hid[ int(ord(c)) ]
		
	print ss
	time = datetime.datetime.now()

### Check whitelist
	door_whitelist = open('/home/pi/RFID/keyed-members','a')
	door_whitelist.write(ss + ',' + name_last + ',' + name_first)
	#time.strftime('%Y-%m-%d %H:%M:%S') + ',' + ss + ',' + names_list[pos] + ',Approved \n')
	door_whitelist.close()

	print(name_first+ ' '+ name_last + ' added to user list!')
	#break()
#	if ID_list.count(ss) == 0:
#		print('User not found.  Access Denied')
#
#		log_file = open('/home/pi/RFID/log-door.csv', 'a')
#		log_file.write(time.strftime('%Y-%m-%d %H:%M:%S') + ',' + ss + ', Unknown (ACCESS DENIED) \n')
#		log_file.close()


	program_done = True