#! /usr/bin/env python2.6
#
# $Author: ee364c03 $
# $Date: 2014-04-26 03:10:27 -0400 (Sat, 26 Apr 2014) $
# $HeadURL: svn+ssh://ece364sv@ecegrid-lnx/home/ecegrid/a/ece364sv/svn/S14/students/ee364c03/Lab11/cypher.py $
# $Revision: 67334 $

import os,sys,string

def is_valid_password(s):
	""" This function checks if the password provided is valid or not. 
	    The password should contain only uppercase letter, lowercase letters and digits
	"""
	if(len(s) == 0):
		return False
	for i in s:
		#print(i)
		if i in string.uppercase:
			continue
		if i in string.lowercase:
			continue
		if i in string.digits:
			continue
		if i == " ":
			continue
		return False
		#if (s.uppercase == 0 and s.lowercase == 0 and s.digits == 0):
			#return False

def vign_encrypt(message, password):
	""" This function implements the vignere cypher encryption. It takes in a message and the password and returns a new encrypted string
	"""
	if(len(password) == 0):
		return message
	if(is_valid_password(password) == False):
		raise ValueError("The key provided to encrypt using Vignere Cypher is invalid")
	message = "!@!@" + message
	rept = len(message) / len(password)
	rem = len(message) % len(password)
	newstr = password
	#print(len(message))
	#print(len(password))
	for i in range(0, rept):
		newstr = newstr + password
		#print(newstr)	
	for i in range(0, rem):
		newstr = newstr + password[i]
 		#print(newstr)
	count = 0
	mapd = {}
	for i in string.uppercase:
		mapd[i] = count
		count = count + 1
	for i in string.lowercase:
		mapd[i] = count
		count = count + 1
	for i in string.digits:
		mapd[i] = count
		count = count + 1
	mapd[' '] = count
	count = count + 1
	for i in "`~!@#$%^&*()_-+={[}]|\"':;?/>.<,\n\r":
		mapd[i] = count
		count = count + 1
	a =  '\\'
	mapd[a] = count
	count = 0
	invmapd = {}
	for i in string.uppercase:
		invmapd[count] = i
		count = count + 1
	for i in string.lowercase:
		invmapd[count] = i
		count = count + 1
	for i in string.digits:
		invmapd[count] = i
		count = count + 1
	invmapd[count] = ' '
	count = count + 1
	for i in "`~!@#$%^&*()_-+={[}]|\"':;?/>.<,\n\r":
		invmapd[count] = i
		count = count + 1
	a =  '\\'
	invmapd[count] = a

	#print(invmapd)
	#print(mapd)	
	newstr2 = ""	
	for i in range(0, len(message)):
		num1 = mapd[message[i]]
		num2 = mapd[newstr[i]]
		#print(num1)
		#print(num2)
		tot = (num1 + num2) % 97
		#print tot
		let = invmapd[tot]
		newstr2 = newstr2 + let
		#print newstr2
	#newstr2 = "!@!@" + newstr2
	return newstr2

def vign_decrypt(message, password):
	""" This function decrypts using the Vignere cypher. It takes in a message and the password that was initially used to encyrpt the message and then returns the unencrypted message
	"""
	if(len(password) == 0):
		return message
	if(is_valid_password(password) == False):
		raise ValueError("The key provided to encrypt using Vignere Cypher is invalid")
	rept = len(message) / len(password)
	rem = len(message) % len(password)
	newstr = password
	#print(len(message))
	#print(len(password))
	for i in range(0, rept):
		newstr = newstr + password
		#print(newstr)	
	for i in range(0, rem):
		newstr = newstr + password[i]
 		#print(newstr)
	count = 0
	mapd = {}
	for i in string.uppercase:
		mapd[i] = count
		count = count + 1
	for i in string.lowercase:
		mapd[i] = count
		count = count + 1
	for i in string.digits:
		mapd[i] = count
		count = count + 1
	mapd[' '] = count
	count = count + 1
	for i in "`~!@#$%^&*()_-+={[}]|\"':;?/>.<,\n\r":
		mapd[i] = count
		count = count + 1
	a =  '\\'
	mapd[a] = count	
	count = 0
	invmapd = {}
	for i in string.uppercase:
		invmapd[count] = i
		count = count + 1
	for i in string.lowercase:
		invmapd[count] = i
		count = count + 1
	for i in string.digits:
		invmapd[count] = i
		count = count + 1
	invmapd[count] = ' '
	count = count + 1
	for i in "`~!@#$%^&*()_-+={[}]|\"':;?/>.<,\n\r":
		invmapd[count] = i
		count = count + 1
	#print mapd
	a =  '\\'
	invmapd[count] = a
	#print(invmapd)
	#print(mapd)	
	newstr2 =""	
	for i in range(0, len(message)):
		num1 = mapd[message[i]]
		num2 = mapd[newstr[i]]
		##print(num1)
		#print(num2)
		tot = (num1 - num2) % 97
		#print tot
		let = invmapd[tot]
		newstr2 = newstr2 + let
		#print newstr2
	newstr = ""
	passwordcheck = "!@!@"
	for i in range(0, 4):
		newstr = newstr + newstr2[i]
	if(newstr != passwordcheck):
		raise ValueError("The password provided is wrong!")
	newstr = ""
	for i in range(4, len(newstr2)):
		newstr = newstr + newstr2[i]
	#message = newstr
	
	return newstr


