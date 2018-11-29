import pymssql
import pandas as pd
class SQLServerFactory(IDBFactory):
	"""docstring for SQLServerFactory"""
	def __init__(self, arg=""):
		super(SQLServerFactory, self).__init__()
		self.constr = ""

	def connection(self):
		pass
	def exequery(self,conn,querytext=""):

		pass
	def exenonquery():
		pass
		