# -*- coding: utf-8 -*-
import sys
import sip
import os
from PyQt4 import QtGui, QtCore, Qt, phonon
from cursor import Cursor
from messagebox import MessageBox
from spfreader import SPFReader
from ldtreader import LDTReader
from talkoption import TalkOption
from PyQt4.phonon import Phonon
import pickle

try:
	_fromUtf8 = QtCore.QString.fromUtf8
except AttributeError:
	def _fromUtf8(s):
		return s


class TypeEffect(QtGui.QWidget):

	def __init__(self, text, textedit, position, parent = None):
		super(TypeEffect, self).__init__(parent)

		self.setFocus()

		self.setGeometry(position)
		#self.setStyleSheet('background-color: rgb(255,255,255)')
		self.index = 0	
		self.lenth = len(text)
		self.text = text
		self.textedit = textedit

		self.timer = QtCore.QTimer()
		self.timer.setInterval(50)
		self.timer_in_mouse = QtCore.QTimer()
		self.timer_in_mouse.setInterval(150)

		self.mouse = QtGui.QWidget(self)
		
		self.mouse.setStyleSheet(_fromUtf8("border-image: url(./ui/mouse1.png);"))
		self.mouse.hide()

		self.tpye_over = False
		self.beclicked = False
		self.mouse_status = True
		self.fetchnexttalk = False

		self.show()

	def typing(self, position):
		self.mouse.setGeometry(position)
		QtCore.QObject.connect(self.timer, QtCore.SIGNAL('timeout()'), self.typeEffect)
		QtCore.QObject.connect(self.timer_in_mouse, QtCore.SIGNAL('timeout()'), self.changeMouse)
		self.timer.start()
		while not self.tpye_over and self.isVisible():
			QtCore.QThread.msleep(50)
			QtCore.QCoreApplication.processEvents(QtCore.QEventLoop.AllEvents, 100)
		self.timer_in_mouse.start()
		while not self.fetchnexttalk and self.isVisible():
			QtCore.QThread.msleep(50)
			QtCore.QCoreApplication.processEvents(QtCore.QEventLoop.AllEvents, 100)

	def typeEffect(self):
		if self.index < self.lenth:
			self.textedit.moveCursor(QtGui.QTextCursor.End)
			self.textedit.insertPlainText(self.text[self.index])
			self.index += 1
		else:
			self.tpye_over = True
			self.showMouse()
			self.timer.stop()

	def mousePressEvent(self, event):
		if not self.tpye_over and event.button() == QtCore.Qt.LeftButton:
			self.showMouse()
			self.tpye_over = True
			self.timer.stop()
			self.textedit.setText(self.text)

		elif self.tpye_over and event.button() == QtCore.Qt.LeftButton:
			self.timer_in_mouse.stop()
			self.textedit.setText('')
			self.mouse.hide()
			self.fetchnexttalk = True

	def showMouse(self):
		if self.isVisible():
			self.mouse.show()

	def changeMouse(self):
		if self.isVisible():
			if self.mouse_status:
				self.mouse.setStyleSheet(_fromUtf8("border-image: url(./ui/mouse1.png);"))
				self.mouse_status = False
			else:
				self.mouse.setStyleSheet(_fromUtf8("border-image: url(./ui/mouse2.png);"))
				self.mouse_status = True

	def keyPressEvent(self, event):
		if not self.tpye_over and event.key() == QtCore.Qt.Key_Space:
				self.showMouse()
				self.tpye_over = True
				self.timer.stop()
				self.textedit.setText(self.text)
		elif self.tpye_over and event.key() == QtCore.Qt.Key_Space:
				self.timer_in_mouse.stop()
				self.textedit.setText('')
				self.mouse.hide()
				self.fetchnexttalk = True

class TalkWindow(QtGui.QWidget):

	def __init__(self, parent = None):
		super(TalkWindow, self).__init__(parent)

		self.bgmpath = ''
		self.player = phonon.Phonon.VideoPlayer(phonon.Phonon.VideoCategory, self)

		self.char_name = ''
		with open('./history/configure', 'r') as configure:
			getback_history = pickle.load(configure)
			self.char_name = getback_history[1]

		self.setGeometry(QtCore.QRect(0, 0, 800, 600))
		self.setObjectName(_fromUtf8("talkwindow"))
		self.topLevelWidget()

		self.shadow = QtGui.QWidget(self)
		self.shadow.setGeometry(QtCore.QRect(0, 0, 800, 600))
		self.shadow.setObjectName(_fromUtf8("shadow"))
		self.setStyleSheet('#shadow{background-color: rgba(0, 0, 0, 30);}')

		self.chardialog = QtGui.QWidget(self)
		self.chardialog.setObjectName(_fromUtf8("chardialog"))
		self.chardialog.setStyleSheet(_fromUtf8("#chardialog{border-image: \
									url(./ui/chardialog.png);}"))
		self.chardialog.hide()

		self.npcdialog = QtGui.QWidget(self)
		self.npcdialog.setObjectName(_fromUtf8("npcdialog"))
		self.npcdialog.setStyleSheet(_fromUtf8("#npcdialog{border-image: \
									url(./ui/npcdialog.png);}"))
		self.npcdialog.hide()


		self.dialogclosebutton = QtGui.QPushButton(self)
		self.dialogclosebutton.setFocusPolicy(QtCore.Qt.NoFocus)
		self.dialogclosebutton.setObjectName('dialogclosebutton')
		self.dialogclosebutton.setGeometry(QtCore.QRect(505, 50, 38, 34))
		self.dialogclosebutton.hide()
		self.dialogclosebutton.setStyleSheet(_fromUtf8('\
										QPushButton{background-image: \
										url(./ui/dialog_close.png); \
										width:38px;height:34px;padding-top:0px;border:0px;} \
										QPushButton:hover{background-image: \
										url(./ui/dialog_close_hover.png); \
										width:38px;height:34px;padding-top:0px;border:0px;} \
										QPushButton:pressed{background-image: \
										url(./ui/dialog_close.png); \
										width:38px;height:34px;padding-top:0px;border:0px;}'))

		self.npcimg = QtGui.QWidget(self)
		self.npcimg.hide()

		self.npcname = QtGui.QLabel(self.npcdialog)
		self.npcname.setGeometry(QtCore.QRect(65, 50, 141, 31))
		self.npcname.setStyleSheet(_fromUtf8("background-color: rgba(255, 255, 255, 0); border: 0px; color : rgb(116, 66, 73); font : 125 12pt"))
		self.npcname.setObjectName(_fromUtf8("npcname"))
		self.npcname.hide()

		self.npctext = QtGui.QTextEdit(self.npcdialog)
		self.npctext.setGeometry(QtCore.QRect(60, 90, 291, 121))
		self.npctext.setStyleSheet(_fromUtf8('background-color: rgba(255, 255, 255, 0); \
												border: 0px; color: rgb(116, 66, 73); font : 125 11pt'))
		self.npctext.setReadOnly(True)
		self.npctext.setObjectName(_fromUtf8("npctext"))
		self.npctext.setTextInteractionFlags(QtCore.Qt.NoTextInteraction)
		self.npctext.viewport().setProperty("cursor", Cursor().arrow)
		self.npctext.hide()

		self.charname = QtGui.QLabel(self.chardialog)
		self.charname.setGeometry(QtCore.QRect(15, 45, 141, 31))
		self.charname.setStyleSheet(_fromUtf8("background-color: rgba(255, 255, 255, 0); border: 0px; color : rgb(116, 66, 73); font : 125 12pt"))
		self.charname.setObjectName(_fromUtf8("charname"))
		self.charname.hide()

		self.chartext = QtGui.QTextBrowser(self.chardialog)
		self.chartext.setGeometry(QtCore.QRect(10, 90, 290, 120))
		self.chartext.setStyleSheet(_fromUtf8("background-color: rgba(255, 255, 255, 0); \
												border: 0px; color :rgb(116, 66, 73); font : 125 11pt "))
		self.chartext.setReadOnly(True)
		self.chartext.setObjectName(_fromUtf8("chartext"))
		self.chartext.setTextInteractionFlags(QtCore.Qt.NoTextInteraction)
		self.chartext.viewport().setProperty("cursor", Cursor().arrow)
		self.chartext.hide()



		self.npctext_buffer = ''	
		self.chartext_buffer = ''

		self.npcdialog_open = False
		self.chardialog_open = False

		self.eventid = []

		self.hide()

	def cutinNPC(self):

		self.show()
		self.npcimg.show()

		timer = QtCore.QTimer()
		timer.start()

		self.npcmoveanimation = QtCore.QPropertyAnimation(self.npcimg, "geometry")
		self.npcmoveanimation.setDuration(700)
		self.npcmoveanimation.setStartValue(QtCore.QRect(800, 88, 256, 512))
		self.npcmoveanimation.setEndValue(QtCore.QRect(544, 88, 256, 512))
		self.npcmoveanimation.start()
		self.connect(self.npcmoveanimation, QtCore.SIGNAL("finished()"), timer.stop)
		while timer.isActive():
			QtGui.QApplication.processEvents(QtCore.QEventLoop.AllEvents, 100)
			QtCore.QCoreApplication.processEvents(QtCore.QEventLoop.AllEvents, 100)

	def opencharDialog(self):
		self.chardialog.show()
		self.chardialog_open = True
		timer = QtCore.QTimer()
		timer.start()
		self.chardialoganimation = QtCore.QPropertyAnimation(self.chardialog, "geometry")
		self.chardialoganimation.setDuration(100)
		self.chardialoganimation.setStartValue(QtCore.QRect(0, 550, 0, 0))
		self.chardialoganimation.setEndValue(QtCore.QRect(0, 250, 325, 260))
		self.chardialoganimation.start()

		self.connect(self.chardialoganimation, QtCore.SIGNAL("finished()"), timer.stop)
		while timer.isActive():
			QtGui.QApplication.processEvents(QtCore.QEventLoop.AllEvents, 100)
			QtCore.QCoreApplication.processEvents(QtCore.QEventLoop.AllEvents, 100)

	def openNPCDialog(self):
		self.npcdialog.show()
		self.npcdialog_open = True
		timer = QtCore.QTimer()
		timer.start()
		self.npcdialoganimation = QtCore.QPropertyAnimation(self.npcdialog, "geometry")
		self.npcdialoganimation.setDuration(100)
		self.npcdialoganimation.setStartValue(QtCore.QRect(500, 280, 0, 0))
		self.npcdialoganimation.setEndValue(QtCore.QRect(200, 0, 410, 280))
		self.npcdialoganimation.start()

		self.connect(self.npcdialoganimation, QtCore.SIGNAL("finished()"), timer.stop)
		while timer.isActive():
			QtGui.QApplication.processEvents(QtCore.QEventLoop.AllEvents, 100)
			QtCore.QCoreApplication.processEvents(QtCore.QEventLoop.AllEvents, 100)

	def processTalk(self, No, parent):
		try:
			data = parent.npctalkldt.getNo(No)
		except Exception as e:
			parent.showDialog(_fromUtf8('輸入編碼錯誤'), 1, (200, 80))
			raise e

		self.BGM_played = False
		if data['_BGM'] != '':
			self.bgmpath = data['_BGM'].upper()
			if not os.path.exists(data['_BGM'].upper()):
				SPFReader().getFile('DALBONG.SPF', self.bgmpath)
				self.player.load(phonon.Phonon.MediaSource(self.bgmpath))
				self.player.play()
				self.connect(self.player, QtCore.SIGNAL("finished()"), self.playAgain)
				self.BGM_played = True
			else:
				self.player = phonon.Phonon.VideoPlayer(phonon.Phonon.VideoCategory, self)
				self.player.load(phonon.Phonon.MediaSource(self.bgmpath))
				self.player.play()
				self.connect(self.player, QtCore.SIGNAL("finished()"), self.playAgain)
				self.BGM_played = True


		#获取NPC立绘
		npcimgpath = parent.globalresldt.getNo(int(data['_CutInImage']))['_FILENAME'].upper()
		SPFReader().getFile('BANX.SPF', npcimgpath)

		parent.menubar.hide()
		self.talkwindow = TalkWindow(self)
		self.npcimg.setStyleSheet('background-image: ' + 'url(./' + npcimgpath + ')')
		self.cutinNPC()

		while data['_EventTypeID1'] != 0:
			if self.BGM_played == False:
				if data['_BGM'] != '':
					if not os.path.exists(data['_BGM'].upper()):
						SPFReader().getFile('DALBONG.SPF', self.bgmpath)
						self.player.load(phonon.Phonon.MediaSource(self.bgmpath))
						self.player.play()
						self.connect(self.player, QtCore.SIGNAL("finished()"), self.playAgain)
						self.BGM_played = True
					else:
						self.player.load(phonon.Phonon.MediaSource(self.bgmpath))
						self.player.play()
						self.connect(self.player, QtCore.SIGNAL("finished()"), self.playAgain)
						self.BGM_played = True
			npcimgpath = parent.globalresldt.getNo(int(data['_CutInImage']))['_FILENAME'].upper()
			SPFReader().getFile('BANX.SPF', npcimgpath)
			self.npcimg.setStyleSheet('background-image: ' + 'url(./' + npcimgpath + ')')

			if data['_BoxPosition'] == 1:
				self.chardialog.lower()
				self.npcdialog.raise_()
				if not self.npcdialog_open:
					self.npcname.show()
					self.npctext.show()
					self.openNPCDialog()
				self.dialogclosebutton.show()
				self.dialogclosebutton.raise_()
				self.npcname.setText(data['_NpcName'].decode('Big5'))
				self.npctext_buffer = data['_Message'].decode('Big5').replace(r'%s', self.char_name)
				if data['_TalkType'] == 1:
					t = TypeEffect(self.npctext_buffer, self.npctext, QtCore.QRect(260, 90, 291, 121), self)
					t.typing(QtCore.QRect(130, 100, 56, 22))
					sip.delete(t)
					data = parent.npctalkldt.getNo(data['_EventTypeID1'])
					
			if data['_BoxPosition'] == 2:
				self.npcdialog.lower()
				self.chardialog.raise_()
				if not self.chardialog_open:
					self.charname.show()
					self.chartext.show()			
					self.opencharDialog()
				self.dialogclosebutton.show()
				self.dialogclosebutton.raise_()
				self.charname.setText(_fromUtf8(self.char_name))
				self.chartext_buffer = data['_Message'].decode('Big5')
				self.chartext.setText('')
				if data['_TalkType'] == 1:
					self.chartext.show()
					t = TypeEffect(self.chartext_buffer, self.chartext, QtCore.QRect(0, 340, 291, 121), self)
					t.typing(QtCore.QRect(120, 100, 56, 22))
					sip.delete(t)
					self.chartext.setText('')
					data = parent.npctalkldt.getNo(data['_EventTypeID1'])
				elif  data['_TalkType'] == 2:
					t = TypeEffect(self.chartext_buffer, self.chartext, QtCore.QRect(0, 340, 291, 121), self)
					t.typing(QtCore.QRect(120, 100, 56, 22))
					sip.delete(t)
					if not self.chardialog_open:
						self.charname.show()
						self.opencharDialog()					
					talkoption = TalkOption(self.chardialog)
					talkoption.setGeometry(QtCore.QRect(10, 95, 290, 120))
					self.chartext.hide()
					for index, event in enumerate(self.eventid):
						if data[event] != 0:
							question = '_Question' + str(index+1)
							talkoption.addOption(data[event], data[question].decode('Big5'))
					talkoption.show()
					No = talkoption.fetchNextNo()
					data = parent.npctalkldt.getNo(No)
					sip.delete(talkoption)

		if data['_EventTypeID1'] == 0:
			if data['_BoxPosition'] == 1:
				self.chardialog.lower()
				self.npcdialog.raise_()
				if not self.npcdialog_open:
					self.npcname.show()
					self.npctext.show()
					self.openNPCDialog()
				self.dialogclosebutton.show()
				self.dialogclosebutton.raise_()
				self.npcname.setText(data['_NpcName'].decode('Big5'))
				self.npctext_buffer = data['_Message'].decode('Big5')
				if data['_TalkType'] == 1:
					t = TypeEffect(self.npctext_buffer, self.npctext,QtCore.QRect(260, 90, 291, 121), self)
					t.typing(QtCore.QRect(130, 100, 56, 22))
					sip.delete(t)
					self.npctext.setText('')
			if data['_BoxPosition'] == 2:
				self.npcdialog.lower()
				self.chardialog.raise_()
				if not self.chardialog_open:
					self.charname.show()
					self.chartext.show()
					self.opencharDialog()
				self.dialogclosebutton.show()
				self.dialogclosebutton.raise_()
				self.charname.setText(_fromUtf8(self.char_name))
				self.chartext_buffer = data['_Message'].decode('Big5')
				self.chartext.setText('')
				if data['_TalkType'] == 1:
					t = TypeEffect(self.chartext_buffer, self.chartext, QtCore.QRect(260, 90, 291, 121), self)
					t.typing(QtCore.QRect(120, 100, 56, 22))
					sip.delete(t)
					self.chartext.setText('')

				elif  data['_TalkType'] == 2:
					t = TypeEffect(self.chartext_buffer, self.chartext, QtCore.QRect(260, 90, 291, 121), self)
					t.typing(QtCore.QRect(120, 100, 56, 22))
					sip.delete(t)
					if not self.chardialog_open:
						self.charname.show()
						self.opencharDialog()
					talkoption = TalkOption(self.chardialog)
					talkoption.setGeometry(QtCore.QRect(120, 430, 56, 22))
					self.chartext.hide()
					for index, event in enumerate(self.eventid):
						if data[event] != 0:
							question = '_Question' + str(index+1)
							talkoption.addOption(data[event], data[question].decode('Big5'))
					#talkoption.topLevelWidget()
					talkoption.show()
					No = talkoption.fetchNextNo()
					sip.delete(talkoption)
		sip.delete(self.talkwindow.player)
		self.npcdialog_open = False
		self.chardialog_open = False
		self.npcname.clear()
		self.charname.clear()
		self.chartext.clear()
		self.npctext.clear()
		self.dialogclosebutton.close()
		self.npcimg.close()
		self.npcdialog.close()
		self.chardialog.close()
		self.npctext.close()
		self.npcname.close()
		self.charname.close()
		self.chartext.close()
		self.hide()
		parent.menubar.show()

	def keyPressEvent(self,event):
		if event.key()==QtCore.Qt.Key_F1:
			print 1

	def delay(self, msec):
		self.time = QtCore.QTime.currentTime().addMSecs(msec)
		while QtCore.QTime.currentTime() < self.time:
			QtGui.QApplication.processEvents(QtCore.QEventLoop.AllEvents, 100)
			QtCore.QCoreApplication.processEvents(QtCore.QEventLoop.AllEvents, 100)

	def getEventID(self, eventid):
		self.eventid = eventid

	def playAgain(self):
		self.player.load(phonon.Phonon.MediaSource(self.bgmpath))
		self.player.play()
		self.connect(self.player, QtCore.SIGNAL("finished()"), self.playAgain)
		self.BGM_played = True

class MenuBar(QtGui.QFrame):
	def __init__(self, parent = None):
		super(MenuBar, self).__init__(parent)

		self.setGeometry(QtCore.QRect(205, 572, 390, 28))
		self.setObjectName(_fromUtf8("menubar"))
		self.setStyleSheet(_fromUtf8("#menubar{border-image: \
							url(./ui/menubar.png);}"))
		self.optionbutton = QtGui.QPushButton(self)
		self.optionbutton.setFocusPolicy(QtCore.Qt.NoFocus)
		self.optionbutton.setGeometry(QtCore.QRect(300, 0, 75, 28))
		self.optionbutton.setObjectName(_fromUtf8("optionbutton"))
		self.optionbutton.setStyleSheet(_fromUtf8("\
										QPushButton{background-image: \
										url(./ui/menu_normal.png); \
										border:0px;} \
										QPushButton:hover{background-image: \
										url(./ui/menu_hover.png); \
										border:0px;} \
										QPushButton:pressed{background-image: \
										url(./ui/menu_pressed.png); \
										border:0px;} \
										QPushButton:released{background-image: \
										url(./ui/menu_released.png); \
										border:0px;}"))

class OptionBar(QtGui.QFrame):
	def __init__(self, parent = None):
		super(OptionBar, self).__init__(parent)

		self.setGeometry(QtCore.QRect(459, 500, 136, 69))
		self.setStyleSheet(_fromUtf8("#optionbar{background-image: \
							url(./ui/optionbar.png);}"))
		self.setObjectName(_fromUtf8("optionbar"))

		self.centralwidget = QtGui.QWidget(self)
		self.setGeometry(QtCore.QRect(459, 500, 136, 69))

		self.Noinputbutton = QtGui.QPushButton(self.centralwidget)
		self.Noinputbutton.setFocusPolicy(QtCore.Qt.NoFocus)
		self.Noinputbutton.setGeometry(QtCore.QRect(10, 10, 116, 18))
		self.Noinputbutton.setObjectName(_fromUtf8("Noinputbutton"))
		self.Noinputbutton.setStyleSheet(_fromUtf8("\
										QPushButton{background-color: rgba(255, 255, 255, 0); \
										border : 0px } \
										QPushButton:hover{background-image: \
										url(./ui/option_hover.png); \
										border : 0px } \
										QPushButton:pressed{background-image: \
										url(./ui/option_pressed.png); \
										border : 0px }"))
		
		self.quitbutton = QtGui.QPushButton(self.centralwidget)
		self.quitbutton.setFocusPolicy(QtCore.Qt.NoFocus)
		self.quitbutton.setGeometry(QtCore.QRect(10, 40, 116, 18))
		self.quitbutton.setObjectName(_fromUtf8("Quitbutton"))
		self.quitbutton.setStyleSheet(_fromUtf8("\
										QPushButton{background-color: rgba(255, 255, 255, 0); \
										border : 0px } \
										QPushButton:hover{background-image: \
										url(./ui/option_hover.png); \
										border : 0px } \
										QPushButton:pressed{background-image: \
										url(./ui/option_pressed.png); \
										border : 0px }"))
		self.hide()

class MainWindow(QtGui.QMainWindow):

	def __init__(self, parent = None):
		super(MainWindow, self).__init__(parent)

		icon = QtGui.QIcon()
		icon.addPixmap(QtGui.QPixmap("./ui/icon.ico"),QtGui.QIcon.Normal)
		self.setWindowIcon(icon)
		self.setWindowTitle('LaTale Talk Emulator')
		self.setObjectName(_fromUtf8("MainWindow"))
		self.setGeometry(QtCore.QRect(0, 0, 800, 600))
		self.setFixedSize(800, 600)

		self.screen = QtGui.QDesktopWidget().screenGeometry()		
		self.size = self.geometry()
		self.move((self.screen.width()-self.size.width())/2, (self.screen.height()-self.size.height())/2)
		
		#设置鼠标样式
		self.setCursor(Cursor().arrow)

		self.option_bar_opend = False
		self.optionbar = OptionBar(self)
		self.menubar = MenuBar(self)

		self.talkwindow = TalkWindow(self)
		self.npctalkldt = LDTReader(self)
		self.npctalkldt.readLDT('./DATA/LDT/NPCTALK.LDT')

		self.globalresldt = LDTReader()
		self.globalresldt.readLDT('./DATA/LDT/GLOBAL_RES.LDT')
		
		self.eventid = []

		self.analyseProperty()
		self.talkwindow.getEventID(self.eventid)

		self.connect(self.menubar.optionbutton, \
								QtCore.SIGNAL(_fromUtf8("clicked()")), self.openOptionBar)
		self.connect(self.optionbar.Noinputbutton, \
								QtCore.SIGNAL(_fromUtf8("clicked()")), self.optionbar.hide)
		self.connect(self.optionbar.Noinputbutton, \
								QtCore.SIGNAL(_fromUtf8("clicked()")), self.openOptionBar)
		self.connect(self.optionbar.Noinputbutton, \
								QtCore.SIGNAL(_fromUtf8("clicked()")), self.openInputWindow)
		self.connect(self.optionbar.quitbutton, \
								QtCore.SIGNAL(_fromUtf8("clicked()")), self.quitbuttonEvent)
		self.connect(self.talkwindow.dialogclosebutton, \
								QtCore.SIGNAL("clicked()"), self.closeTalkWindow)

	def closeTalkWindow(self):

		sip.delete(self.talkwindow.player)
		self.talkwindow.npcdialog_open = False
		self.talkwindow.chardialog_open = False
		self.talkwindow.npcname.clear()
		self.talkwindow.charname.clear()
		self.talkwindow.chartext.clear()
		self.talkwindow.npctext.clear()
		self.talkwindow.dialogclosebutton.close()
		self.talkwindow.npcimg.close()
		self.talkwindow.npcdialog.close()
		self.talkwindow.chardialog.close()
		self.talkwindow.npctext.close()
		self.talkwindow.npcname.close()
		self.talkwindow.charname.close()
		self.talkwindow.chartext.close()
		self.talkwindow.close()
		self.menubar.show()

	def openOptionBar(self):
		if self.option_bar_opend == False:
			self.optionbar.show()
			self.option_bar_opend = True	
		else:
			self.optionbar.hide()
			self.option_bar_opend = False

	def quitbuttonEvent(self):
		sys.exit()

	def keyPressEvent(self, event):
		if event.key() == QtCore.Qt.Key_Escape:
			if self.option_bar_opend == True:
				self.optionbar.hide()
				self.option_bar_opend = False

	def openInputWindow(self):
		self.optionbar.Noinputbutton.setDisabled(True)
		No = self.showDialog(_fromUtf8('請輸入對話編號:'), 3, (200, 90))
		self.optionbar.Noinputbutton.setDisabled(False)
		if No != '':
			self.talkwindow.processTalk(No, self)

	def analyseProperty(self):
		for i in self.npctalkldt.property_name:
			if '_EventTypeID' in i:
				self.eventid.append(i)

	def showDialog(self, string, mode, size):
		messagebox = MessageBox(self)
		messagebox.setGeometry(0, 0, size[0], size[1])
		messagebox.move((self.size.width()-size[0])/2, (self.size.height()-size[1])/2)
		if mode == 1:
			messagebox.tip(string)
		if mode == 2:
			messagebox.imformation(string)
		if mode == 3:
			messagebox.inputwindow(string)
			return str(_fromUtf8(messagebox.inputline.text()))


