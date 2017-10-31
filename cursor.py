# -*- coding: utf-8 -*-

from PyQt4 import QtGui

cursor_img = "./ui/cursor.png"
cursor_load = "./ui/cursor_load.png"

class Cursor(QtGui.QWidget):


	def __init__(self, parent = None):
		super(Cursor, self).__init__(parent)
		#
		self.arrow_pix =  QtGui.QPixmap(cursor_img)
		self.arrow = QtGui.QCursor(self.arrow_pix, 0, 0)
		self.arrow.shape()
		#
		self.load_pix =  QtGui.QPixmap(cursor_load)
		self.load = QtGui.QCursor(self.load_pix, 0, 0)
		self.load.shape()
		#
