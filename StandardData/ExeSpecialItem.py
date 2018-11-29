from MysqlFactory import MysqlFactory
import pandas as pd
class ExeSpecialItem(object):
	"""特殊护理执行查询(需要查询每次执行个数的)"""
	def __init__(self, arg=""):
		super(ExeSpecialItem, self).__init__()
		self.arg = arg
		self.db=MysqlFactory()
		#self.item_header={"id":"id","item":"item","grade":"grade"}
	
	#特殊护理执行分档标准(利用pandas的read_sql功能)
	def queryalldata(self):
		querytext="select * from exespecialitem"
		dbconn=self.db.connection()
		dataframe=pd.read_sql(querytext,dbconn)			
		self.db.close_connection()		
		return dataframe
		pass
		