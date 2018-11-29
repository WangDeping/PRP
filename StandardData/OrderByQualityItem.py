from MysqlFactory import MysqlFactory
import pandas as pd
class OrderByQualityItem(object):
	"""特殊医嘱开单，若是临时医嘱需要提取数量，若是长期医嘱需要提取执行次数"""
	def __init__(self, arg=""):
		super(OrderByQualityItem, self).__init__()
		self.arg = arg
		self.db=MysqlFactory()
		#self.item_header={"id":"id","item":"item","grade":"grade"}
	
	#特殊医嘱开单(利用pandas的read_sql功能)
	def queryalldata(self):
		querytext="select * from orderbyqualityitem  where deleted is NULL"
		dbconn=self.db.connection()
		dataframe=pd.read_sql(querytext,dbconn)			
		self.db.close_connection()		
		return dataframe
		pass
		