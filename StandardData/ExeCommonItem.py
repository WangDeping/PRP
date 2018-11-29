from MysqlFactory import MysqlFactory
import pandas as pd
class ExeCommonItem(object):
	"""一般护理执行工作量"""
	def __init__(self, arg=""):
		super(ExeCommonItem, self).__init__()
		self.arg = arg
		self.db=MysqlFactory()
		#self.item_header={"id":"id","item":"item","grade":"grade"}
	
	#护理执行分档标准(利用pandas的read_sql功能)
	def queryalldata(self):
		querytext="select * from execommonitem"
		dbconn=self.db.connection()
		dataframe=pd.read_sql(querytext,dbconn)		
		self.db.close_connection()		
		return dataframe
		pass
		