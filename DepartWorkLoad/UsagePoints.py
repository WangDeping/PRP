from IWorkLoadPoints import IWorkLoadPoints
class UsagePoints(IWorkLoadPoints):
	"""docstring for UsagePoints"""
	def __init__(self, iworkload):
		super(UsagePoints, self).__init__(iworkload)		
		self.usagetup=("滴眼","滴眼")
		columns=["执行ID","科室","登记号","医嘱项","频次","用法","要求执行日期","工号","姓名","数量","疗程"]
		self.usageworkload=self.iworkload.usageExeWorkLoad(self.usagetup)		
		self.usageworkload.columns=columns
		pass
	def statistics(self):
    	#直接从cache拿到统计
		usagedata=self.usageworkload
		usagedata["统计数量"]=1
		usageWorkLoad=usagedata.groupby(["科室","工号","姓名","用法"],as_index=False)["统计数量"].sum()
		self.saveFile(usageWorkLoad,"特殊用法统计")
		pass
	def getDetail(self):
		self.saveFile(self.usageworkload,"用法详细记录")
		pass
