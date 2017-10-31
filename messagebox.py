# -*- coding: utf-8 -*-

from cursor import Cursor
from PyQt4 import QtGui, QtCore


try:
	_fromUtf8 = QtCore.QString.fromUtf8
except AttributeError:
	def _fromUtf8(s):
		return s

class MessageBox(QtGui.QDialog):

	def __init__(self, parent = None):
		super(MessageBox, self).__init__(parent)
		self.setObjectName("messagebox")

		self.setWindowFlags(QtCore.Qt.FramelessWindowHint)
		self.setStyleSheet(_fromUtf8("#messagebox \
									{background-color: \
									rgba(22, 47, 61, 250); \
									border-color: rgb(255, 255, 255); \
									border : 5px; \
									border-radius:10px}"))

		self.Ok = QtGui.QPushButton(self)
		self.Ok.setFocusPolicy(QtCore.Qt.NoFocus)
		self.Ok.setGeometry(QtCore.QRect(0, 0, 70, 18))
		self.Ok.setObjectName("Yes")

		self.Ok.setStyleSheet(_fromUtf8("\
										QPushButton{background-image: \
										url(./ui/verify_normal.png); \
										border:0px;} \
										QPushButton:hover{background-image: \
										url(./ui/verify_hover.png); \
										border:0px;} \
										QPushButton:pressed{background-image: \
										url(./ui/verify_pressed.png); \
										border:0px;} \
										QPushButton:released{background-image: \
										url(./ui/verify_released.png); \
										border:0px;}"))
		self.Ok.hide()

		self.No = QtGui.QPushButton(self)
		self.No.setFocusPolicy(QtCore.Qt.NoFocus)
		self.No.setGeometry(QtCore.QRect(0, 0, 70, 18))
		self.No.setObjectName("No")


		self.No.setStyleSheet(_fromUtf8("\
										QPushButton{background-image: \
										url(./ui/cancel_normal.png); \
										border:0px;} \
										QPushButton:hover{background-image: \
										url(./ui/cancel_hover.png); \
										border:0px;} \
										QPushButton:pressed{background-image: \
										url(./ui/cancel_pressed.png); \
										border:0px;} \
										QPushButton:released{background-image: \
										url(./ui/cancel_released.png); \
										border:0px;}"))
		QtCore.QObject.connect(self.No, QtCore.SIGNAL("clicked()"), self.close)
		self.No.hide()

		self.message = QtGui.QTextBrowser(self)
		self.message.setObjectName("message")
		self.message.setStyleSheet(_fromUtf8("border :0px ; \
								background-color: rgba(255, 255, 255, 0); \
								color: white; \
								font: 9pt \"Microsoft JhengHei\";"))
		self.message.setTextInteractionFlags(QtCore.Qt.NoTextInteraction)
		self.message.viewport().setProperty("cursor", Cursor().arrow)
		
		self.inputline = QtGui.QLineEdit(self)
		self.inputline.setObjectName("inputline")
		self.inputline.setStyleSheet("border: 0px ; \
									background-color: rgba(91, 181, 189, 250); \
									color: white; \
									font: 9pt \"Microsoft JhengHei\"; \
									border-radius: 5px")
		self.inputline.setCursor(Cursor().arrow)
		
	def tip(self, tip):
		width = self.width()
		height = self.height()

		self.Ok.move(width-90, height-28)
		self.Ok.show()
		self.message.setGeometry(QtCore.QRect(20, 10, width-40, height-40))
		self.message.setAlignment(QtCore.Qt.AlignLeft|QtCore.Qt.AlignTop)
		self.message.setText(tip)

		QtCore.QObject.connect(self.Ok, QtCore.SIGNAL("clicked()"), self.close)

		self.inputline.hide()
		self.show()

	def imformation(self, imformation):

		width = self.width()
		height = self.height()

		self.message.setGeometry(QtCore.QRect(20, 10, width-40, height-40))
		self.message.setAlignment(QtCore.Qt.AlignHCenter|QtCore.Qt.AlignVCenter)
		self.message.setText(imformation)
		QtCore.QObject.connect(self.Ok, QtCore.SIGNAL("clicked()"), self.close)

		self.inputline.hide()
		self.show()

	def inputwindow(self, instruction):

		width = self.width()
		height = self.height()

		self.inputline.setGeometry(QtCore.QRect(20, 30, width-40, 20))
		self.inputline.setAlignment(QtCore.Qt.AlignLeft|QtCore.Qt.AlignTop)

		self.message.setGeometry(QtCore.QRect(18, 5, width-40, 25))
		self.message.setAlignment(QtCore.Qt.AlignLeft|QtCore.Qt.AlignTop)
		self.message.setText(instruction)
		self.Ok.move(width/2 - 80, height-28)
		self.Ok.show()
		self.No.move(width/2 + 10, height-28)
		self.No.show()
		QtCore.QObject.connect(self.No, QtCore.SIGNAL("clicked()"), self.close)
		QtCore.QObject.connect(self.No, QtCore.SIGNAL("clicked()"), self.cleanText)
		QtCore.QObject.connect(self.Ok, QtCore.SIGNAL("clicked()"), self.close)
		self.exec_()

	def cleanText(self):
		self.inputline.setText('')