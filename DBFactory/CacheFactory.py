import pyodbc
import pandas as pd
from IDBFactory import  IDBFactory

class CacheFactory(IDBFactory):
	"""使用Cache数据库实现查询和相应操作"""
	def __init__(self, arg=""):
		super(CacheFactory, self).__init__()
		self.constr= "DSN=DHCAPP;UID=_system;PWD=sys;"
		self.conn=self.connection();
		pass
		
	def connection(self):
		return pyodbc.connect(self.constr)		
		pass	
#查询方法；数据量较大时使用此方法
	def exequery(self,querytext):
		self.conn=self.connection();
		cursor=self.conn.cursor()
		cursor.execute(querytext)
		result = cursor.fetchall()	

		cursor.close()	
		self.close_connection()
		return result
		pass
	def close_connection(self):
		self.conn.close()
		pass

		
