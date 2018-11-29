import pymysql
class MysqlFactory(object):
	"""docstring for MYSQLFactory"""
	def __init__(self, arg=""):
		super(MysqlFactory, self).__init__()
		self.arg = arg

	def connection(self):
		self.conn=pymysql.connect("127.0.0.1","root","5055585","prp")
		return self.conn
		pass

	def exequery(self,querytext=""):
		self.connection()
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

	def exenonquery():
		pass
		