#! /usr/bin/env python2.6
#
# $Author: ee364c03 $
# $Date: 2014-04-13 02:26:34 -0400 (Sun, 13 Apr 2014) $
# $HeadURL: svn+ssh://ece364sv@ecegrid-lnx/home/ecegrid/a/ece364sv/svn/S14/students/ee364c03/Lab11/Steganography.py $
# $Revision: 67251 $

from PIL import Image, ImageFilter
import os,sys
import cypher 
try:
	from BitVector import *
except:
	pass

class Steganography: 
	""" This class deals with encrypting a message in an image by changing the least significant bit in the image.
It can also decrypt the image and get the message that was encoded. 

The main functions which the user can use are "encrypt", "decrypt", "wipealldata"
"""


	def __init__(self, imgname):
	
		""" The __init__ function initializes the Steganography class, and takes the image name as the only arguments
	    	It opens the image using the PIL module and the arguments that the object has are the "imgname", which is the image name,
	    	"pic" which is the 2D array containing the RGB/Grayscale Values (the pixels) and "img", the img itself. 
		Example: a = Steganography(imagelocation)"""
		try:
			img = Image.open(imgname)
		except IOError:
			raise ValueError('Image does not exist')
		img = Image.open(imgname)
		pic = img.load()
		self.img = img
		self.pic = pic
		self.imgname = imgname
		

	def __msgcheck(self,msg,typeofscan="H"):
		""" The __msgcheck function is a function that will primarily used by other functions that a user can call. Its main functionalty 
	 	   is to check if the message is valid. It checks if its within the size bounds, and also confirms that the msg is a string and
		    not an integer or some other random type. If the message is not valid, it raises a ValueError.
		Example: a.__msgcheck(message)"""

		""" It first checks if the message is a string, longer than 0 but is within the max length that we are providing. It also checks that only valid data is provided. If its greyscale, only 1 bit per location can be changed and if its color, there are 3 values that can be changed per location."""
		if type(msg) is not str:
			raise ValueError('The message must be a string')
		if (len(msg) == 0):
			raise ValueError("No Message provided")
		imgarr = self.img.size
		grysc = 0
		if(type(self.pic[0,0]) is int):
			grysc = 1
		if(grysc == 1):
			msgsize1 = ((imgarr[0] * imgarr[1] * 1) / 8) - 14
		else:
			msgsize1 = ((imgarr[0] * imgarr[1] * 3) / 8) - 14
		
		if(len(msg) > msgsize1):	
			raise ValueError("Message is longer than the maximum usable size")

		for i in msg:
			if(ord(i) > 128):
				raise ValueError("The message contains some non-ascii characters")



	def encrypt(self,msg,scandir='H',cypherkey="VignereCypher", fname="encrypted.tif"):
		""" This is one of the main functions that a user can use. It encrypts the message in the image in the specified direction.
	  	  The message is the only argument that must be provided. The other 3 arguments are optional. The first optional argument
 	  	  is "scandir" which is the direction in which you want the message to be embedded in. This can either be 'H' or 'V'. The second
	  	  optional argument is "cypherkey" which is the key that you want to used to encrypt the message before embedding, this adds extra
	  	  security.The additional security uses the Vignere cypher.
	  	  The 3rd argument is the name you want to save the file with the embedded image, default name is "encrypted.tif" 
		  Examples: a.encrypt((message), a.encrypt(message, "V"), a.encrypt(message, "H", "SECURITYKEY"), a.encrypt(message, "V", "SECURITYKEY", "newimg.tif")"""
		
		try:
			newvec = BitVector(size = 0)
		except:
			newvec = ""
		if(scandir == 'H'):
				typeofscan = 1
		elif(scandir == 'V'):
				typeofscan = 2
		else:
			raise ValueError("Scan Direction can only be 'H' or 'V', where H is horizontal and V is vertical")
	
		""" It first checks if the message is valid and then encrypts using Vignere Cypher and also adds in a beginning a null string and an ending null string"""
		Steganography.__msgcheck(self,msg,typeofscan)
		init = "$a$a$"
		final = "$a$a$"
		msg = cypher.vign_encrypt(msg, cypherkey)
		msg = init + msg + final
		byterep = bytearray(msg)
		""" Converts the message into binary numbers, using bitvector as well as a longer method which involves converting it to binary, getting the binary numbers and padding it with zeros as a backup"""
		for i in byterep:
			try:
				nvar = BitVector(intVal=i, size = 8)	
				newvec = newvec+ nvar
			except:
				nvar = bin(i)
				var = ""
				if(len(nvar) != 10):	
					nofzeros = 10 - len(nvar)
					for l in range(0, nofzeros):
						var = var + "0"
					for z in range(2, len(nvar)):
						var = var + nvar[z]
				newvec = newvec + var
		newstr = str(newvec)
		noftimes = len(newstr)
		count = 0
		imgarr = self.img.size
		hor = 0
		grysc = 0
		if(type(self.pic[0,0]) is int):
			grysc = 1
		newrgb = []
		""" Scans the message according the scan provided and embeds the message accordingly, the order of the 2 for loops is the only difference between the 2 scans"""
		if(typeofscan == 1):
			for y in range(0, imgarr[1]):
				for x in range(0,imgarr[0]):
					if(count != (noftimes)):
						count = Steganography.__valchange(self,x,y,newstr,grysc,count,noftimes)
					else:
						self.img.save(fname)
						return True
		elif(typeofscan == 2):
			for x in range(0, imgarr[0]):
				for y in range(0,imgarr[1]):
					if(count != (noftimes)):
						count = Steganography.__valchange(self,x,y,newstr,grysc,count, noftimes)
					else:
						self.img.save(fname)
						return True
	

	def __valchange(self,x,y,newstr,grysc,count,noftimes):
		
		""" The __valchange function is used to change a specific bit of a pixel and
         	   is a function that is only called by the encrypt function and should not
    	 	   be called by the user. If called by the user,it can embed 1 bit in the data
    	 	   It takes in 6 arguments. The first 2 arguments are the position in the
         	   image that you want to change, the 'x' and 'y' coordinate. 'newstr' is
    	 	   the data being embedded and 'grysc' is the variable that shows whether the
    	 	   image is grayscale or not. 'count' is the variable that confirms whether
    		   all the bits have been embedded and finally 'noftimes' is the total number
    	    	   of bits being embedded."""

		""" Appends the pixel values to a list, changes the values according to the bits which we are embedding and then puts it back into the picture array. If its a greyscale value, a list is created with its value added in, otherwise it converts the tuple to a list. Theres another for loop that runs through the list changing the last bit aaccordingly"""
		if(grysc == 1):
			newrgb = []
			dig = []
			dig.append(self.pic[x,y])
			newrgb.append(self.pic[x,y])
		else:
			newrgb = list(self.pic[x,y])
			dig = self.pic[x, y]
		for z in range(0, len(newrgb)):
			if(count == (noftimes)):
				if(grysc == 1):
					self.pic[x,y] = newrgb[0]
					del newrgb
				else:
					self.pic[x,y] = tuple(newrgb)
					del newrgb
				return count
			if(int(newstr[count]) == 1):
				if(dig[z] % 2 == 0):
					newrgb[z] += 1
			if(int(newstr[count]) == 0):
				if(dig[z] % 2 == 1):
					newrgb[z] =  newrgb[z] - 1
			count = count + 1
		if(grysc == 1):
			self.pic[x,y] = newrgb[0]
		else:
			self.pic[x,y] = tuple(newrgb)
		del newrgb
		del dig
		return count
					

	def decrypt(self,scandir,cypherkey='VignereCypher'):
		""" The decrypt function extracts the message from the image. It takes in the
	   	 'scandir' as one of the arguments which is the direction in which you
	   	 scan the image, it could either be 'H' or 'V'. The second argument is
	  	  optional, it takes in the 'cypherkey' which is used to decrypt the message
	  	  once extracted from the image. The function also confirms if it is reading
	  	  the message in the right direction.
		  Examples: a.decrypt("V"), a.decrypt("H", "SECURITYKEY")"""

		imgarr = self.img.size
		if(scandir == 'H'):
			typeofscan = 1
		elif(scandir == 'V'):
			typeofscan = 2
		else:
			raise ValueError("Scan Direction can only be 'H' or 'V', where H is horizontal and V is vertical")
		init = '$a$a$'
		initlist = list(init)
		initcheck = 0
		final = '$a$a$'
		finalist = list(final)
		finalcheck = 0
		listread = []
		msgencoded = []
		count = 0
		noftimes = 0
		grysc = 0
		endcheck = []
		""" Checks the type of image and scans in the direction provided and extracts the message. It also checks if it reads the start string and reads the end string. Once the number of characters read are 5, it compares it with the initstring. If its correct, it continues, otherwise it raises an error. It then continues to scan the data and once it finds the null string it stops reading. """
		if(type(self.pic[0,0]) is int):
			grysc = 1
		if(typeofscan == 1):
			for y in range(0, imgarr[1]):
				for x in range(0,imgarr[0]):
					(count,listread,endcheck) = Steganography.__decryptvalchange(self,x,y,listread,grysc,count,msgencoded,endcheck,initcheck)
					if(endcheck == finalist):	
						newst = ""
						for c in range(5,len(msgencoded)-5):
							newst = newst + msgencoded[c]
						msgenc = cypher.vign_decrypt(newst,cypherkey)
						return msgenc
					if(len(msgencoded) == 5):	
						if(initlist != msgencoded):
							raise ValueError("The direction provided to decrypt does not contain any data")
						initcheck = 1
			raise ValueError("This file has been changed after the image was embedded and is corrupted")
		elif(typeofscan == 2):
			for x in range(0, imgarr[0]):
				for y in range(0,imgarr[1]):
					(count,listread,endcheck) = Steganography.__decryptvalchange(self,x,y,listread,grysc,count,msgencoded,endcheck,initcheck)
					if(endcheck == finalist):	
						newst = ""
						for c in range(5,len(msgencoded)-5):
							newst = newst + msgencoded[c]
						msgenc = cypher.vign_decrypt(newst,cypherkey)
						return msgenc
					if(len(msgencoded) == 5):	
						if(initlist != msgencoded):
							raise ValueError("The direction provided to decrypt does not contain any data")
						initcheck = 1
			raise ValueError("This file has been changed after the image was embedded and is corrupted")

	
	
	def __decryptvalchange(self,x,y,listread,grysc,count,msgencoded,endcheck,initcheck):
		""" The __decryptvalchange function is used to extract a specific bit of a pixel and
      	   	   is a function that is only called by the decrypt function and should not
    	 	   be called by the user. If called by the user,it can extract 1 bit from the image
     	 	   It takes in 8 arguments. The first 2 arguments are the position in the
    	  	   image that you want to extract from, the 'x' and 'y' coordinate. 'listread' is
    	 	   the list of bits that have been extracted and 'grysc' is the variable that shows whether the
    	  	   image is grayscale or not. 'count' is the number of bits that have been read 
    	   	   'msgencoded' is the message that has been extracted after converting it to a
	  	   character. 'endcheck' is a variable that checks if the end of the message has been
	   	   reached and initcheck is used to confirm whether it read the correct starting bits. """

		""" If its a greyscale value, it creates a list and appends the greyscale value, otherwise it just converts the tuple to a list. It then reads the LSB and adds it to another list, once its read 8 bits it converts it to a character and apppends it to a new list of characters"""
		init = '$a$a$'
		initlist = list(init)
		final = '$a$a$'
		finalist = list(final)
		if(grysc == 1):
			newrgb = []
			dig = []
			dig.append(self.pic[x,y])
			newrgb.append(self.pic[x,y])
		else:
			newrgb = list(self.pic[x, y])
			dig = self.pic[x, y]
		
		""" Gets a pixel and gets the LSB, once 8 bits are got, it adds it to the message list"""
		for z in range(0, len(newrgb)):
			if(count % 8 == 0) and (count != 0):
				asciival = 0
				power = 7
				for l in listread:
					asciival = asciival + l*(2**power)
					power -= 1
				charread = chr(asciival)
				del listread
				listread = []
				msgencoded.append(charread)
				if(len(msgencoded) == 5):
					if(initlist != msgencoded):
						raise ValueError("The direction provided to decrypt does not contain any data")
				if(len(endcheck) != 0):	
					endcheck.append(charread)
					if(len(endcheck) == 5):
						if(endcheck!=finalist):
							del endcheck
							endcheck = []
						elif(initcheck == 1):
							return count, listread,endcheck
				if (charread == '$' and len(endcheck) == 0 and initcheck == 1):	
					endcheck.append(charread)
			listread.append((newrgb[z] % 2))
			count = count + 1
		del newrgb
		del dig
		return count,listread,endcheck	

	def wipealldata(self):
		""" The wipealldata resets the value of the Least Significan bit for each pixel. 
 		    It takes in no arguments.
		    Examples: a.wipealldata() """

		""" Goes through all the pixels and makes the LSB 0. It runs through 2 for loops, and just does the changes accordingly using the same methods for encrypting and decrypting"""
		imgarr = self.img.size
		grysc = 0
		if(type(self.pic[0,0]) is int):
			grysc = 1
		for x in range(0, imgarr[0]):
			for y in range(0,imgarr[1]):
				if(grysc == 1):
					newrgb = []
					dig = []
					dig.append(self.pic[x,y])
					newrgb.append(self.pic[x,y])
				else:
					newrgb = list(self.pic[x, y])
					dig = self.pic[x, y]
				for z in range(0, len(newrgb)):
					if((dig[z] % 2) == 1):
						newrgb[z] -= 1
				if(grysc == 1):
					self.pic[x,y] = newrgb[0]
					del dig
					del newrgb
				else:
					self.pic[x,y] = tuple(newrgb)
					del dig
					del newrgb
		self.img.save(self.imgname)


