#!/usr/bin/env python3
# -*- coding: utf-8 -*-

# cLx 2020 - http://clx.freeshell.org/
# I never managed to learn radio "NATO" alphabet, so i made this... still a WIP !

import sys, os, fnmatch, random, time

try:
	# sudo apt-get install python3-pyqt5
	#raise("We want to use PyQt4")
	from PyQt5.QtGui import *
	from PyQt5.QtCore import *
	from PyQt5.QtWidgets import *
	print("Using PyQt5")
except:
	# sudo apt-get install python-qtpy python3-qtpy
	from PyQt4.QtGui import *
	from PyQt4.QtCore import *
	print("Using PyQt4")

class Game():
	words = {'a':("Alfa", "Alpha"), 'b':"Bravo", 'c':("Charlie", "Charly"), 'd':"Delta", 'e':"Echo", 'f':("Foxtrot", "Fox-trot"), 'g':"Golf", 'h':"Hotel", 'i':"India",
         'j':("Juliett", "Juliet"), 'k':"Kilo", 'l':"Lima", 'm':"Mike", 'n':"November", 'o':"Oscar", 'p':"Papa", 'q':"Quebec", 'r':"Romeo",
         's':"Sierra", 't':"Tango", 'u':"Uniform", 'v':"Victor", 'w':("Whiskey", "Whisky"), 'x':"Xray", 'y':"Yankee", 'z':("Zulu", "Zoulou")}

	def __init__(self):
		self.initial = ""
		self.inputstring = ""
		self.started = False
		self.time_max = float("nan")
		self.time_start = float("nan")
		self.time_remaining = float("nan")
		pass

	def start(self):
		self.guessList = list(self.words.keys())
		random.shuffle(self.guessList)
		self.newWord()

	def newWord(self):
		if len(self.guessList) == 0:
			return False
		self.initial = self.guessList[0].upper(); del self.guessList[0]
		self.validWords = self.words[self.initial.lower()]
		self.inputstring = ""
		self.time_max = 10
		self.time_remaining = self.time_max
		self.time_start = time.time()
		self.started = True
		return True

	def getSolution(self, failed=False):
		self.time_max = float("nan")
		self.time_start = float("nan")
		self.time_remaining = float("nan")
		self.started = False

		if failed:
			self.guessList.insert(3, self.initial)
			if len(self.guessList[-1]) > 1 and self.guessList[-1] != self.initial:
				self.guessList.insert(-1, self.initial)

		if type(self.validWords) is str:
			return self.validWords
		return self.validWords[0]

	def getRemainingTime(self):
		self.time_remaining = self.time_start + self.time_max - time.time()
		return self.time_remaining, self.time_max

	def addCharacter(self, character):
		if self.inputstring == "":
			if character != self.initial:
				self.inputstring += self.initial
		self.inputstring += character

	def delCharacter(self):
		self.inputstring = self.inputstring[:-1]

	def checkValidity(self):
		if type(self.validWords) is str:
			s = [self.validWords]
		else:
			s = self.validWords

		for w in s:
			if self.inputstring.lower() == w.lower():
				self.started = False
				return True
		return False

	def getWhatToDisplay(self):
		if self.inputstring != "":
			return self.inputstring
		return self.initial

class GUI(QWidget):
	def __init__(self):
		super(GUI, self).__init__()
		self.game = Game()
		self.initUI()

	def initUI(self):
		self.setStyleSheet("\
			QWidget { background-color: #000000; color: #ffffff; } \
			QLabel { margin: 0px; padding: 0px; } \
			QSplitter::handle:vertical   { image: none; } \
			QSplitter::handle:horizontal { width:  2px; image: none; } \
			QPushButton { background-color: #404040; background: #404040; } \
			QLabel#label { font-size: 30pt; } \
		");

		layout = QVBoxLayout(self)

		def mkQLabel(objectName, text='', alignment=Qt.AlignLeft):
			o = QLabel()
			o.setObjectName(objectName)
			o.setAlignment(alignment)
			o.setText(text)
			return o

		def mkButton(text, function):
			btn = QPushButton(text)
			btn.setFocusPolicy(Qt.TabFocus)
			if function:
				btn.clicked.connect(function)
			return btn

		self.text = mkQLabel('label', "Press Start", Qt.AlignCenter | Qt.AlignTop)
		self.text.setMinimumSize(330, 20)
		layout.addWidget(self.text)

		self.progressbar = QProgressBar()
		self.progressbar.setOrientation(Qt.Horizontal)
		self.progressbar.setValue(0)
		self.progressbar.setMaximum(100)
		self.progressbar.setTextVisible(False)
		self.progressbar.setVisible(False)
		layout.addWidget(self.progressbar)

		self.pushButton = mkButton("Start", self.pushButtonPressed)
		layout.addWidget(self.pushButton)

		self.refreshTimer = QTimer()
		self.refreshTimer.timeout.connect(self.refreshTimerTimeout)

		self.pauseTimer = QTimer()
		self.pauseTimer.timeout.connect(self.pauseTimerTimeout)

		self.setWindowTitle(u"Radio Alphabet")
		self.show()

	def pushButtonPressed(self):
		self.game.start()
		self.text.setText(self.game.getWhatToDisplay())
		self.pushButton.setDisabled(True)
		self.pushButton.setVisible(False)
		self.progressbar.setVisible(True)
		self.refreshTimer.start(100)
		self.blinkingState = False

	def pauseTimerTimeout(self):
		self.pauseTimer.stop()
		self.progressbar.setValue(0)
		if self.game.newWord():
			self.text.setText(self.game.getWhatToDisplay())
			self.refreshTimer.start(100)
			self.blinkingState = False
		else:
			self.text.setText("Finished!")
			self.pushButton.setDisabled(False)
			self.pushButton.setVisible(True)
			self.progressbar.setVisible(False)
		self.text.setStyleSheet("");

	def refreshTimerTimeout(self):
		remainingTime, maxTime = self.game.getRemainingTime()
		a = int(maxTime*10)
		b = int((maxTime-remainingTime)*10)
		if a != self.progressbar.maximum():
			self.progressbar.setMaximum(a)
		self.progressbar.setValue(b)
		self.progressbar.repaint()

		if remainingTime <= 0:
			self.refreshTimer.stop()
			self.text.setText(self.game.getSolution(failed=True))
			self.pauseTimer.start(2000)
			self.text.setStyleSheet("QLabel { color: red; }");
		elif remainingTime < 1:
			if self.blinkingState:
				self.text.setStyleSheet("QLabel { background-color: red; color: black; }");
			else:
				self.text.setStyleSheet("QLabel { color: red; }");
			self.blinkingState = not self.blinkingState


	def keyPressEvent(self, event):
		if self.game.started:
			key = event.key()
			if key == Qt.Key_Backspace:
				self.game.delCharacter()
			elif key >= Qt.Key_A and key <= Qt.Key_Z:
				self.game.addCharacter(chr(key))
				if self.game.checkValidity():
					self.refreshTimer.stop()
					self.text.setText(self.game.getSolution())
					self.pauseTimer.start(2000)
					self.text.setStyleSheet("QLabel { color: green; }");

			else:
				return

			self.text.setText(self.game.getWhatToDisplay())

def main():
	global m1
	app = QApplication(sys.argv)
	m1 = GUI()
	app.installEventFilter(m1)
	ret = app.exec_()
	sys.exit(ret)

if __name__ == '__main__':
	main()
