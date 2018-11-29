from IWorkLoadPoints import IWorkLoadPoints
class OxygenLocPoints(IWorkLoadPoints):
	"""高压氧室工作量统计，按照人次统计"""
	def __init__(self,iworkload):
		super(OxygenLocPoints,self).__init__(iworkload)
		self.appworkload=iworkload.rislocApplication("GYY-高压氧")		
		self.appworkload.columns=["日期","患者姓名","姓名","报告人","审核人","收入","项目名称"]
		self.appworkload["数量"]=1
	def statistics(self):
		result=self.appworkload.groupby(["姓名","项目名称"],as_index=False)["数量"].sum()
		self.saveFile(result,"高压氧工作量")
		pass
	def getDetail(self):
		self.saveFile(self.appworkload,"高压氧治疗人次")
		pass	
		