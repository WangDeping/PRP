from IWorkLoadPoints import IWorkLoadPoints
class ChronicPoints(IWorkLoadPoints):
	"""慢病上报"""
	def __init__(self, iworkload):		
		super(ChronicPoints, self).__init__(iworkload)
		self.chronicworkload=iworkload.chronicWorkLoad()
		self.chronicworkload.columns=["登记号","患者姓名","科室","姓名","类型"]
	def statistics(self):
		data=self.chronicworkload
		data["统计数量"]=1
		workload=data.groupby(["科室","姓名","类型"],as_index=False)["统计数量"].sum()
		self.saveFile(workload,"慢病上报")
		pass
		