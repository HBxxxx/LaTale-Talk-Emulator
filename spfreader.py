# -*- coding: utf-8 -*-
import pickle
import struct
import os

class SPFReader():

	def __init__(self):

		self.spf_file = {}
		#self.spf_name = ['ROWID.SPF', 'BANX.SPF', 'DALBONG.SPF']

	def analyzeSPF(self, window):
		try:
			#获取SPF文件路径，格式为：{'*.SPF': '*\*.SPF'}
			with open('./history/spf_path', 'r') as f:
				spf_path = pickle.load(f)

			for spf in spf_path:
				#获取SPF文件名:*.SPF
				spf_name = spf
				file = {}
				#打开绝对路径下的SPF文件，格式为*\*.SPF
				with open( spf_path[spf], 'rb') as f:
					f.seek(-140, 2)
					offset = struct.unpack('i', f.read(4))[0]
					filenumber = offset / 140
					f.seek(-(offset + 4), 1)
					for i in range(filenumber):
						datalist = []
						string = f.read(128).rstrip(b'\x00')#删除多余的'0x00'
						datalist.append(struct.unpack('i', f.read(4))[0])#保存偏移量
						datalist.append(struct.unpack('i', f.read(4))[0])#保存文件长度
						No = struct.unpack('h', f.read(2))[0]
						f.seek(2, 1)
						file[string] = datalist
					#在./history文件下保存不含后缀名的SPF分析文件(字典格式)
					with open('./history/' + spf_name.split('.')[0], 'w') as f:
						pickle.dump(file, f)
		except Exception as e:
			raise e		
	def getFile(self, SPFname, filename):
		try:
			#传入的*.SPF保留*
			spfname = SPFname.split('.')[0]
			#打开对应分析文件
			with open('./history/' + spfname, 'r') as f:
				spf = pickle.load(f)

				offset = spf[filename][0]
				size = 	spf[filename][1]

				with open('./history/spf_path', 'r') as f:
					spf_path = pickle.load(f)
				#打开游戏文件夹下对应的SPF文件
				with open(spf_path[SPFname], 'rb') as r:
					r.seek(offset, 0)
					file = r.read(size)
				#将文件保存在根目录下
				file_path = './' + os.path.dirname(filename)
				if not os.path.exists(file_path):
					os.makedirs(file_path)
				with open('./' + filename, "wb") as w:
					w.write(file)
				return './' + filename
		except Exception as e:
			raise e			
	'''
	def getFileData(self, SPFname, filename):
		#获取数据流
		spfname = SPFname.split('.')[0]

		with open('./history/' + spfname, 'r') as f:
			spf = pickle.load(f)

			with open('./history/spf_path', 'r') as f:
				spf_path = pickle.load(f)

			offset = spf[filename][0]
			size = 	spf[filename][1]

			with open(spf_path[SPFname], 'rb') as r:
				r.seek(offset, 0)
				file = r.read(size)

			return file
	'''		