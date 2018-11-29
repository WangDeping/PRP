from IWorkLoadPoints import IWorkLoadPoints

class ClinicalPathwayPoints(IWorkLoadPoints):
	"""临床路径统计"""
	def __init__(self, iworkload):
		super(ClinicalPathwayPoints, self).__init__(iworkload)
		self.clinicalPathway=iworkload.clinicalPathway()
		self.clinicalPathway.columns=["科室","工号","姓名","数量"]		
	
    
	def statistics(self):
		data=self.clinicalPathway.groupby(["工号","姓名"],as_index=False)["数量"].sum()
		
		self.saveFile(data,"临床路径")		
		pass

	
	def getDetail(self):
		self.saveFile(self.clinicalPathway,"临床路径")
		pass
	