# -*- coding: utf-8 -*-
import sys
from PyQt4 import QtGui, QtCore

try:
    _fromUtf8 = QtCore.QString.fromUtf8
except AttributeError:
    def _fromUtf8(s):
        return s

class TalkOption(QtGui.QFrame):

	def __init__(self, parent = None):
		super(TalkOption, self).__init__(parent)
		self.option_number = 0

		self.nextNo = 0
		self.option_selected = False
		
	def addOption(self, id ,text):
		option = QtGui.QPushButton(self)
		option.setFocusPolicy(QtCore.Qt.NoFocus)
		option.setGeometry(0, 20 * self.option_number, 230, 17)
		option.setObjectName(str(id))
		option.setText(str(id))
		option.setStyleSheet(_fromUtf8("QPushButton{background-image: url(./ui/dialog_option.png); \
										padding-top:0px; border:0px; color : rgba(255, 255, 255, 0);} \
										QPushButton:hover{background-image: url(./ui/dialog_option_hover.png); \
										padding-top:0px; border:0px;  color : rgba(255, 255, 255, 0);} "))
		QtCore.QObject.connect(option, QtCore.SIGNAL(_fromUtf8("clicked()")), self.setNextNo)
		option.show()
		label = QtGui.QLabel(option)
		label.setText(text)
		label.setIndent(25)
		label.setStyleSheet(_fromUtf8("border: 0px; color : rgb(116, 66, 73); font : 125 10pt; "))
		label.show()

		self.option_number += 1

	def setNextNo(self):
		sender = self.sender()
		self.nextNo = int(sender.objectName())
		self.option_selected = True

	def fetchNextNo(self):

		while not self.option_selected and self.isVisible():
			QtCore.QThread.msleep(100)
			QtGui.QApplication.processEvents(QtCore.QEventLoop.AllEvents, 1)
			QtCore.QCoreApplication.processEvents(QtCore.QEventLoop.AllEvents, 1)
		self.option_selected = False
			
		return self.nextNo
'''
app = QtGui.QApplication(sys.argv)

window = QtGui.QMainWindow()
window.setGeometry(100,100, 800,600)
window.show()
mainwindow = TalkOption(window)
mainwindow.show()
mainwindow.addOption(21312, 'sdasdas')
print mainwindow.fetchNextNo()

app.exec_()
#sip.delete(mainwindow.talkwindow)
sip.delete(app)
sys.exit()
'''



