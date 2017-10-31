# -*- coding: utf-8 -*-
import sys
reload(sys)
sys.setdefaultencoding('utf-8')
import ctypes  
ctypes.windll.shell32.SetCurrentProcessExplicitAppUserModelID("LaTale Talk Emulator")  
import sip
import os, shutil
import pickle
from spfreader import SPFReader
from PyQt4 import QtGui, QtCore, Qt
from cursor import Cursor
from messagebox import MessageBox
import UI

try:
	_fromUtf8 = QtCore.QString.fromUtf8
except AttributeError:
	def _fromUtf8(s):
		return s

class Launcher(QtGui.QMainWindow):

	def __init__(self, parent = None):
		super(Launcher, self).__init__(parent)

		icon = QtGui.QIcon()
		icon.addPixmap(QtGui.QPixmap("./ui/icon.ico"),QtGui.QIcon.Normal)
		self.setWindowIcon(icon)
		
		self.setWindowTitle('LaTale Talk Emulator')

		self.absolute_path = ''
		self.history_path = ''
		self.history_name = ''
		self.spf_name = ['ROWID.SPF', 'BANX.SPF', 'DALBONG.SPF']
		self.spf_path = {}
		self.path_selectd = False
		self.name_verified = False

		self.setAttribute(QtCore.Qt.WA_TranslucentBackground, True)
		self.setWindowFlags(Qt.Qt.FramelessWindowHint | Qt.Qt.WindowStaysOnTopHint)
		self.screen = QtGui.QDesktopWidget().screenGeometry()
		self.setGeometry(QtCore.QRect(0, 0, 292, 134))
		self.setObjectName('launcher')
		self.size = self.geometry()
		self.move((self.screen.width()-self.size.width())/2, (self.screen.height()-self.size.height())/2)
		#登录界面图
		self.background = QtGui.QWidget(self)
		self.background.setGeometry(0, 0, 294, 169)
		self.background.setObjectName('background')
		self.background.setStyleSheet(_fromUtf8('#background{ background-image: \
							url(./ui/launcher_cut.png);}'))
		self.cursor = Cursor()
		self.setCursor(self.cursor.arrow)
		#路径文本框
		self.path_text = QtGui.QLineEdit(self)
		self.path_text.setReadOnly(True)
		self.path_text.setStyleSheet(_fromUtf8('border :0px ; \
								background-color: rgba(255, 255, 255, 0); \
								color: white; \
								font : Timers'))
		self.path_text.setCursor(self.cursor.arrow)
		self.path_text.setGeometry(QtCore.QRect(74, 55, 105, 19))
		#角色名文本框
		self.user_text = QtGui.QLineEdit(self)
		self.user_text.setReadOnly(False)
		self.user_text.setStyleSheet(_fromUtf8('border :0px ; \
								background-color: rgba(255, 255, 255, 0); \
								color: white; \
								font : Timers'))
		self.user_text.setCursor(self.cursor.arrow)
		self.user_text.setGeometry(QtCore.QRect(74, 84, 105, 19))
		#关闭按钮
		self.close_btn = QtGui.QPushButton(self)
		self.close_btn.setGeometry(QtCore.QRect(268, 5, 21, 21))
		self.close_btn.setObjectName('close_btn')
		self.close_btn.setStyleSheet(_fromUtf8('\
										QPushButton{background-image: \
										url(./ui/close.png); \
										width:16px;height:13px;padding-top:0px;border:0px;} \
										QPushButton:hover{background-image: \
										url(./ui/close_hover.png); \
										width:16px;height:13px;padding-top:0px;border:0px;} \
										QPushButton:pressed{background-image: \
										url(./ui/close_press.png); \
										width:16px;height:13px;padding-top:0px;border:0px;}'))
		self.connect(self.close_btn, QtCore.SIGNAL('clicked()'), self.close_btnEvent)
		#文件夹按钮
		self.folder_btn = QtGui.QPushButton(self)
		self.folder_btn.setGeometry(QtCore.QRect(180, 59, 16, 13))
		self.folder_btn.setObjectName('folder_btn')
		self.folder_btn.setStyleSheet(_fromUtf8('\
										QPushButton{background-image: \
										url(./ui/Folder.png); \
										width:16px;height:13px;padding-top:0px;border:0px;} \
										QPushButton:pressed{background-image: \
										url(./ui/Folder_press.png); \
										width:16px;height:13px;padding-top:0px;border:0px;}'))

		self.connect(self.folder_btn, QtCore.SIGNAL('clicked()'), self.fetchPath)

		#角色名确认按钮
		self.verify_btn = QtGui.QPushButton(self)
		self.verify_btn.setGeometry(QtCore.QRect(180, 87, 13, 13))
		self.verify_btn.setObjectName('verify_btn')
		self.verify_btn.setStyleSheet(_fromUtf8('\
										QPushButton{background-image: \
										url(./ui/verify.png); \
										width:13px;height:13px;padding-top:0px;border:0px;} \
										QPushButton:pressed{background-image: \
										url(./ui/verify_press.png); \
										width:13px;height:13px;padding-top:0px;border:0px;}'))
		self.connect(self.verify_btn, QtCore.SIGNAL('clicked()'), self.fetchUserText)
		#开始按钮
		self.start_btn = QtGui.QPushButton(self)
		self.start_btn.setGeometry(QtCore.QRect(211, 46, 65, 65))
		self.start_btn.setObjectName('start_btn')
		self.start_btn.setStyleSheet(_fromUtf8('\
										QPushButton{background-image: \
										url(./ui/START1.png); \
										width:65px;height:65px;padding-top:0px;border:0px;} \
										QPushButton:hover{background-image: \
										url(./ui/START2.png); \
										width:65px;height:65px;padding-top:0px;border:0px;} \
										QPushButton:pressed{background-image: \
										url(./ui/START3.png); \
										width:65px;height:65px;padding-top:0px;border:0px;} \
										QPushButton:released{background-image: \
										url(./ui/START4.png); \
										width:65px;height:65px;padding-top:0px;border:0px;}'))
		self.connect(self.start_btn, QtCore.SIGNAL('clicked()'), self.startApplication)

	def startApplication(self):
		try:
			if self.path_selectd and self.name_verified:
				#将历史路径，历史角色名写入./history/configure
				#将SPF文件路径写入./history/configure/spf_path,格式为：{'*.SPF': '*\*.SPF'}
				if not os.path.exists('./history'):
					os.mkdir('./history')
				history = [self.history_path, self.history_name]
				with open('./history/configure', 'w') as f:
					pickle.dump(history, f)
				with open('./history/spf_path', 'w') as f:
					for spf in self.spf_name:
						self.spf_path[spf] = str(self.absolute_path + '\\' + spf)
					pickle.dump(self.spf_path, f)
				#禁用start键
				self.start_btn.setDisabled(True)
				
				#获取LDT文件
				spfreader = SPFReader()
				spfreader.analyzeSPF(self)
				spfreader.getFile('ROWID.SPF', 'DATA/LDT/NPCTALK.LDT')
				spfreader.getFile('ROWID.SPF', 'DATA/LDT/GLOBAL_RES.LDT')
				#打开主窗口UI
				self.mainwindow = UI.MainWindow()
				self.mainwindow.show()
				self.close()
			else:
				if not self.path_selectd:
					self.showDialog(_fromUtf8('請選擇正確的遊戲档案'), 1, (200, 70))
				elif not self.name_verified:
					self.showDialog(_fromUtf8('請確認角色名'), 1, (200, 70))
		except Exception as e:
			self.showDialog(_fromUtf8('錯誤代碼'), 1, (200, 70))
			raise e
			sys.exit()

	def fetchPath(self):
		#获取游戏文件夹路径,并判断该文件夹里是否存在所需SPF。若存在，则保存到历史路径中
		try:
			self.absolute_path = (str(QtGui.QFileDialog.getExistingDirectory(self, _fromUtf8('选择游戏文件夹路径'), \
																_fromUtf8('C:\Users\Administrator\Desktop')))).decode('utf-8')
			if self.absolute_path:
				self.path_text.setText(self.absolute_path)

				file_exists = True
				miss_file = ''
				miss_file_num = 0

				for spf in self.spf_name:
					if not os.path.exists(self.absolute_path+ '\\'+ spf):
						miss_file += spf + '\n'
						file_exists = False
						miss_file_num += 1
				if file_exists:
					self.history_path = self.absolute_path
					self.path_selectd = True
				else:
					self.showDialog( miss_file +_fromUtf8('文件不存在'), 1, (200, 60+18*miss_file_num))
					self.path_selectd = False
		except Exception as e:
				self.showDialog(_fromUtf8('错误代码：'), 1, (200, 70))
				raise e

	def fetchUserText(self):
		#获取用户设定的角色名，保存到历史角色名中
		try:
			self.char_name = str(self.user_text.text())
			if self.char_name == '':
				self.showDialog(_fromUtf8('角色名不能為空'), 1, (200, 70))
			else:
				self.showDialog(_fromUtf8('角色名已確認'), 1, (200, 70))
				self.history_name = self.char_name.encode('utf-8')
				self.name_verified = True
		except Exception as e:
				self.showDialog(_fromUtf8('錯誤代碼'), 1, (200, 70))
				raise e

	def showDialog(self, string, mode, size):
		messagebox = MessageBox(self)
		messagebox.setGeometry(0, 0, size[0], size[1])
		messagebox.move((self.size.width()-size[0])/2, (self.size.height()-size[1])/2)
		if mode == 1:
			#无确认键
			messagebox.tip(_fromUtf8(string))
		if mode == 2:
			#有确认键
			messagebox.imformation(_fromUtf8(string))

	def close_btnEvent(self):
		sip.delete(app)
		sys.exit()

app = QtGui.QApplication(sys.argv)
launcher = Launcher()
#读取历史配置
if os.path.exists('./history/configure'):
	configure = {}
	try:
		with open('./history/configure', 'r') as configure:
			getback_history = pickle.load(configure)
			launcher.history_path = getback_history[0]
			launcher.absolute_path = launcher.history_path
			launcher.history_name = getback_history[1]
			launcher.path_text.setText(_fromUtf8(launcher.history_path))
			launcher.user_text.setText(_fromUtf8(launcher.history_name))
			launcher.path_selectd = True
			launcher.name_verified = True
	except Exception as e:
		launcher.show()
		launcher.showDialog(_fromUtf8('程式發生錯誤\n請嘗試重新啟動'), 1, (200, 80))
		os.remove('./history/configure')
		raise e
else:
	pass
launcher.show()
app.exec_()
sip.delete(app)
if os.path.exists('./DATA'):
	shutil.rmtree("./DATA/") 
sys.exit()