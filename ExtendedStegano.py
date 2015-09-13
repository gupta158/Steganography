#! /usr/bin/env python2.6
#
# $Author: ee364c03 $
# $Date: 2014-04-27 07:23:56 -0400 (Sun, 27 Apr 2014) $
# $HeadURL: svn+ssh://ece364sv@ecegrid-lnx/home/ecegrid/a/ece364sv/svn/S14/students/ee364c03/Lab11/ExtendedStegano.py $
# $Revision: 67446 $

from PIL import Image, ImageFilter
import os,sys,re
import cypher 
from pythongui import Ui_MainWindow

try:
	from BitVector import *
except:
	pass
from Steganography import Steganography
from PySide import QtCore, QtGui

class ExtendedStegano(Steganography):
	def __init__(self, imgname):
		Steganography.__init__(self, imgname)

	def encrypt(self,inputname,scandir='H',cypherkey="VignereCypher", fname="encrypted.tif"):
		""" This is one of the main functions that a user can use. It inherits some functionality from the Steganography encrypt. The user passes a file and we check if the file is a text file, it just calls the parent class encrypt function and that does the embedding. If it is an image that we need to embed, it converts the grayscale value to a character and then embeds it, the functionality could not be invoked from the parents class as in the initial class, all characters have to have an ascii value under 128 but in this case it can go uptil 255. A file name can be given to store the new image
		Examples: a.encrypt((textfile), a.encrypt(imgf, "V"), a.encrypt(img, "H", ""), a.encrypt(textfile, "V", "SECURITYKEY", "newimg.tif")"""
		try:
			fh = open(inputname)
		except:
			raise ValueError("Source file path provided was wrong.")
		itype = 1
		if(re.search(".txt$", inputname)):
			itype = 2
			try:
				all = fh.readlines()
				new = "".join(all)
			except:
				raise ValueError("Text File doesn not exist")
			message = "msg" + new	
			Steganography.encrypt(self, message, scandir, cypherkey, fname)

		#Checks what file is given
		elif(re.search(".tif$", inputname)):
			if(scandir == 'H'):
				typeofscan = 1
			elif(scandir == 'V'):
				typeofscan = 2
			else:
				raise ValueError("Scan Direction can only be 'H' or 'V', where H is horizontal and V is vertical")
			try:
				inimg = Image.open(inputname)
				inpic = inimg.load()
				imgarr = inimg.size
			except:
				raise ValueError("Image does not exist")
			lensi = 0
			for i in imgarr:
				lensi = lensi + len(str(i))

			init = "$a$a$"
			if not(type(inpic[0,0]) is int):
				raise ValueError("File provided is a color image.")
			message = init + "img"
			newstr = ""
			message = message + str(imgarr)
			for i in range(len(message)):
				newstr = newstr + '{0:08b}'.format(ord(message[i]))
			message = newstr
			grysc = 0
			if(type(self.pic[0,0]) is int):
				grysc = 1
			for y in range(0, imgarr[0]):
				for x in range(0, imgarr[1]):
					new = '{0:08b}'.format(inpic[x,y])
					message = message + new
			#Converts the grayscale value to a character and then to its binary value
			for i in range(len(init)):
				message = message + '{0:08b}'.format(ord(init[i]))
			imgarr = self.img.size
			if(grysc == 1):
				msgsize1 = ((imgarr[0] * imgarr[1] * 1))
			else:
				msgsize1 = ((imgarr[0] * imgarr[1] * 3))
			if(msgsize1 < len(message)):
				raise ValueError("Image can not be embedded as it is too big")
			newstr = message	
			noftimes = len(newstr)
			count = 0
			if(typeofscan == 1):
				for y in range(0, imgarr[1]):
					for x in range(0, imgarr[0]):
						if(count != (noftimes)):
							count = ExtendedStegano._valchange(self,x,y,newstr,grysc,count,noftimes)
						else:
							self.img.save(fname)
							return True
			elif(typeofscan == 2):
				for x in range(0, imgarr[0]):
					for y in range(0,imgarr[1]):
						if(count != (noftimes)):
							count = ExtendedStegano._valchange(self,x,y,newstr,grysc,count, noftimes)
						else:
							self.img.save(fname)
							return True
		else:
			raise ValueError("The file provided isn't one of the acceptable input types.")


	def _valchange(self,x,y,newstr,grysc,count,noftimes):
		
		""" This function is quite similar to the parents class _valchange, just a small change was made but the rest is the same."""

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
					

	def decrypt(self,scandir,outfile, msgtype, cypherkey='VignereCypher'):	
		""" Decrypts the message stores in the file. It inherits most of its functionality from the parents class. It checks if we are storing an image or a text file. It appends .txt or .tif to the file accordingly. It just returns the message if its a text file. If its an image, grayscale value are appended to the array and image is then saved in the output files. The user also sends the file type, "I" for image and "T" for text.

Examples: a.decrypt("H", outfile, "I"), a.decrypt("V", outfile, "T", "KEY"),

 """	
		embedata = Steganography.decrypt(self, scandir, cypherkey)
		ftype = ""
		for i in range(0, 3):
			ftype = ftype + embedata[i]
		if((ftype == "msg" and msgtype != 'T') or (ftype == "img" and msgtype != 'I')):
			raise ValueError("The type of file that was provided does not match the data embedded")
		if ftype == "msg":
			data = ''
			for i in range(3, len(embedata)):
				data = data + embedata[i]
			if not(re.search(".txt$", outfile)):
				outfile = outfile + ".txt"
			try:
				fh = open(outfile,"w")
				fh.write(data)
				fh.close()
				
			except:
				raise ValueError("Path provided to the output file does not exist.")

		if ftype == "img":
			a = re.search("[(](?P<hor>[\d]+), (?P<ver>[\d]+)[)]", embedata)
			hor = a.group("hor")
			ver = a.group("ver")
			omitstrlen = 4 + 3 + len(hor) + len(ver)
			newstr = ""
			for i in range(omitstrlen, len(embedata)):
				newstr = newstr + embedata[i]
			hor = int(hor)
			ver = int(ver)
			count = 0

			picarray = []
			for x in range(0, hor):
				for y in range(0, ver):
					picarray.append(ord(newstr[count]))		
					count += 1
			im = Image.new('L', (hor,ver))
			im.putdata(picarray)
			if not(re.search(".tif$", outfile)):
				outfile = outfile + ".tif"
			try:
				im.save(outfile)
			except:
				raise ValueError("Path provided to the output file does not exist.")

		return True		

	def wipealldata(self):
		Steganography.wipealldata(self)	

#This just tests the ExtendedStegano class
def embtest():
	grayscaletest = ExtendedStegano('photo.tif')
	grayscaletest.encrypt("letter.txt", "V", "", "new122.tif")
	outputdectxt = ExtendedStegano('encrypted.tif')
	outputdectxt.decrypt("H", "new.tif", "I", "")


class myGUI(Ui_MainWindow):
	""" This is the class that deals with making the GUI. It inherits from the python file that was generated using the ui file that was created using qt designer. It connects all the buttons, toggles, etc. to the correct functions."""
	def __init__(self):
		#Initializes the class
		super(myGUI, self).__init__()
		
	def initUI(self, MainWindow):
		""" Sets up the GUI from the other class and then connects the buttons and radio buttons and text changed to the functions"""
		Ui_MainWindow.setupUi(self, MainWindow)
		self.successdisp.setText("")
		self.load.clicked.connect(self.openmed)
		self.embpush.clicked.connect(self.embeddata)	
		self.embencno.toggled.connect(self.noembenc)
		self.embencyes.toggled.connect(self.yesembenc)
		self.extpush.clicked.connect(self.extractdata)	
		self.extencno.toggled.connect(self.noextenc)
		self.extencyes.toggled.connect(self.yesextenc)
		self.extkey.setEnabled(False)
		self.extencyes.setEnabled(False)
		self.extencno.setEnabled(False)
		self.extmsgtyp.activated[str].connect(self.extonActivated)  
		self.embsource.editingFinished.connect(self.embonActivated)
		#self.medpath.editingFinished.connect(self.openmed)

	def extonActivated(self):
		""" This is activated when the combo box is activated and disables decryption if its an image and enables it if its a text file. It does this for extract tab"""
		if(self.extmsgtyp.currentText() == "Image"):
			self.extkey.setEnabled(False)
			self.extencyes.setEnabled(False)
			self.extencno.setEnabled(False)
		elif(self.extmsgtyp.currentText() == "Text"):
			self.extkey.setEnabled(True)
			self.extencyes.setEnabled(True)
			self.extencno.setEnabled(True)

	def embonActivated(self):
		""" This is activated when the combo box is activated and disables decryption if its an image and enables it if its a text file. It does this for the embed data."""
		if(re.search(".tif$", self.embsource.text())):
			self.embkey.setEnabled(False)
			self.embencyes.setEnabled(False)
			self.embencno.setEnabled(False)
		elif(re.search(".txt$", self.embsource.text())):
			self.embkey.setEnabled(True)
			self.embencyes.setEnabled(True)
			self.embencno.setEnabled(True)
		
	def noextenc(self):
		""" If there is no encryption, then it deactivates the Enter Key Box"""
		self.extkey.clear()
		self.extkey.setEnabled(False)
	def yesextenc(self):
		""" If there is encryption, then it activates the Enter Key Box"""
		self.extkey.clear()
		self.extkey.setEnabled(True)

	def extractdata(self):
		""" This function is toggled when the extract button is clicked, it checks if all the info is entered and entered correctly, if it is it extracts the message to the given target otherwise it creats a message box to show the error"""
		medium = self.medpath.text()
		msgtype = self.extmsgtyp.currentText()
		exttarget = self.exttarget.text()
		extscan = self.extscan.currentText()
		if(medium == "" or exttarget == ""):
			msg = QtGui.QMessageBox()
			msg.setMinimumHeight(20)
			msg.setMinimumWidth(300)
			msg.setFixedWidth(500)
			msg.setText("Error!")
			msg.setInformativeText("Please fill all necessary fields")
			msg.setWindowTitle("ERROR")
			msg.exec_()	
			self.successdisp.setText("FAIL! Not Extracted")
		else:
	
			if(extscan == "Horizontal"):
				scandir = 'H'
			elif(extscan == "Vertical"):
				scandir = 'V'
			else:
				scandir = 'H'
			if(msgtype == "Image"):
				msgt = 'I'
				cyphkey = ""
				if not(re.search(".tif$", exttarget)):
					exttarget = exttarget + ".tif"
			elif(msgtype == "Text"):
				msgt = 'T'
				if not(re.search(".txt$", exttarget)):
					exttarget = exttarget + ".txt"

			else:
				msgt = 'I'
				cyphkey = ""
				if not(re.search(".tif$", outfile)):
					exttarget = exttarget + ".tif"
			check = 0
			self.exttarget.setText(exttarget)
			cyphkey = ''
			if(self.extencyes.isEnabled() == False):
				cyphkey = ""
			elif(self.extencyes.isChecked()):	
				cyphkey = self.extkey.text()
			elif(self.extencno.isChecked()):
				cyphkey = ""
			else:	
				msg = QtGui.QMessageBox()
				msg.setMinimumHeight(20)
				msg.setMinimumWidth(300)
				msg.setFixedWidth(500)
				msg.setText("Error!")
				msg.setInformativeText("Please fill all necessary fields")
				msg.setWindowTitle("ERROR")
				msg.exec_()
				check = 1

			if not (check == 1):		
				try:
					medium = ExtendedStegano(medium)
					medium.decrypt(scandir,exttarget, msgt, cyphkey)	
					self.successdisp.setText("SUCCESS! Extracted")
				except ValueError as m:
					msg = QtGui.QMessageBox()
					msg.setMinimumHeight(20)
					msg.setMinimumWidth(300)
					msg.setFixedWidth(500)
					msg.setText("Error!")
					msg.setInformativeText(str(m))
					msg.setWindowTitle("ERROR")
					msg.exec_()							
					self.successdisp.setText("FAIL! Not Extracted")

	def noembenc(self):
		""" If there is no encryption, the key box is diabled"""
		self.embkey.clear()
		self.embkey.setEnabled(False)
	def yesembenc(self):
		""" If there is encryption, the key box is enabled"""
		self.embkey.clear()
		self.embkey.setEnabled(True)

	def embeddata(self):
		""" Checks if all data for embedding is provided and is provided correctly otherwises creates a message box with the error stated in the box."""
		medium = self.medpath.text()
		source = self.embsource.text()
		target = self.embtarget.text()
		embscan = self.embscan.currentText()
		if(medium == "" or source == "" or target == ""):
			msg = QtGui.QMessageBox()
			msg.setMinimumHeight(20)
			msg.setMinimumWidth(300)
			msg.setFixedWidth(500)
			msg.setText("Error!")
			msg.setInformativeText("Please fill all necessary fields")
			msg.setWindowTitle("ERROR")
			msg.exec_()
			self.successdisp.setText("FAIL! Not Embedded")	
		else:
	
			if(embscan == "Horizontal"):
				scandir = 'H'
			elif(embscan == "Vertical"):
				scandir = 'V'
			else:
				scandir = 'H'
			check = 0
			if not(self.embencyes.isEnabled()):
				cyphkey = ""
			elif(self.embencyes.isChecked()):	
				cyphkey = self.embkey.text()
			elif(self.embencno.isChecked()):
				cyphkey = ""
			
			else:	
				msg = QtGui.QMessageBox()
				msg.setMinimumHeight(20)
				msg.setMinimumWidth(300)
				msg.setFixedWidth(500)
				msg.setText("Error!")
				msg.setInformativeText("Please fill all necessary fields")
				msg.setWindowTitle("ERROR")
				msg.exec_()
				check = 1
		
			if not (check == 1):
				try:
					medium = ExtendedStegano(medium)
					medium.encrypt(source,scandir,cyphkey, target)	
					self.successdisp.setText("SUCCESS! Embedded")
				except ValueError as m:
					msg = QtGui.QMessageBox()
					msg.setMinimumHeight(20)
					msg.setMinimumWidth(300)
					msg.setFixedWidth(500)
					msg.setText("Error!")
					msg.setInformativeText(str(m))
					msg.setWindowTitle("ERROR")
					msg.exec_()							
					self.successdisp.setText("FAIL! Not Embedded ")
				except KeyError as n:
					msg = QtGui.QMessageBox()
					msg.setMinimumHeight(20)
					msg.setMinimumWidth(300)
					msg.setFixedWidth(500)
					msg.setText("Error!")
					msg.setInformativeText("Target Filename Provided is not correct")
					msg.setWindowTitle("ERROR")
					msg.exec_()							
					self.successdisp.setText("FAIL! Not Embedded ")


		
	def openmed(self):
		""" When the Load button is presses, it trysloads the image and raises an error if it fails"""
		try:
			self.scene = QtGui.QGraphicsScene()
			img = Image.open(self.medpath.text())
			pic = img.load()
			b = (QtGui.QPixmap(self.medpath.text())) 

			b = b.scaled(self.graphicsView.size(), QtCore.Qt.KeepAspectRatio)	
			self.scene.addPixmap(b)
			self.graphicsView.setScene(self.scene)
			medium = self.medpath.text()
			self.successdisp.setText((medium + " loaded"))
		except IOError as m:	
			msg = QtGui.QMessageBox()
			msg.setMinimumHeight(20)
			msg.setMinimumWidth(300)
			msg.setFixedWidth(500)
			msg.setText("Error!")
			msg.setInformativeText("Medium Image does not Exist")
			msg.setWindowTitle("ERROR")
			msg.exec_()
			self.successdisp.setText("FAIL! Medium DNE")			
	
if __name__=="__main__":
	""" Calls the GUI and sets it up"""
	app = QtGui.QApplication(sys.argv)
	MainWindow = QtGui.QMainWindow()
	ex = myGUI()
	ex.initUI(MainWindow)
	MainWindow.show()
	app.exec_()
