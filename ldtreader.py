# -*- coding: utf-8 -*-
import struct

class LDTReader():

	def __init__(self, parent = None):
		#super(LDTReader, self).__init__(parent)

		self.DATA = {}
		self.property_number = 0
		self.property_type = []
		self.property_name = []
		self.example_number = 0
		self.ldt_name = [""]

	def readLDT(self, LDTpath):
		try:
			with open(LDTpath, 'rb') as f:
				#获取属性数量
				f.seek(4, 0)
				data = struct.unpack('I', f.read(4))
				self.property_number = data[0]
				#获取实例属相
				data = struct.unpack('I', f.read(4))
				self.example_number = data[0]
				#获取属性名称
				f.seek(12, 0)
				for i in range(self.property_number):
					self.property_name.append(f.read(64).split(b'\x00')[0])
				#获取属性类型
				f.seek(8204,0)
				for i in range(self.property_number):
					data = struct.unpack('I', f.read(4))
					self.property_type.append(data[0])
				#获取实例信息
				f.seek(8716, 0)
				for i in range(self.example_number):
					#读取实例的ID，用于存入ID字典（ID用二进制数据保存）
					example_id = f.read(4)
					example_data = {}
					for j in range(self.property_number):
						if self.property_type[j] == 2 or self.property_type[j] == 3:
							#属性类型为数值或逻辑值
							data = struct.unpack('I', f.read(4))
							example_data[self.property_name[j]] = (data[0])
						else:
							#属性类型为字符串
							size = struct.unpack('H', f.read(2))
							if size[0] == 0:
								example_data[self.property_name[j]] = ''
							if size[0] != 0:
								data = f.read(size[0])
								example_data[self.property_name[j]] = data
					#存入ID字典
					self.DATA[example_id] = example_data
		except Exception as e:
			raise e

	def getNo(self, No):
		#将输入No转换成二进制
		No = struct.pack('I', int(No))
		if No in self.DATA:
			return self.DATA[No]
		else:
			return -1