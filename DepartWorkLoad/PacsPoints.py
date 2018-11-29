from IWorkLoadPoints import IWorkLoadPoints
import pandas as pd


class PacsPoints(IWorkLoadPoints):
	"""影像科工作量"""
	def __init__(self, iworkload):
		super(PacsPoints, self).__init__(iworkload)
		self.type={'INSPECTION':'检查','REPORT':'报告','VERIFY':'审核'}

	def handleData(self,type):	
		recordworkload=self.iworkload.pacsWorkload(type)
		recordworkload.columns=["科室代码","检查科室","用户代码","工号","姓名","子类","部位代码","部位","数量"]
		return recordworkload
		pass
	def statistics(self):
		self.getDetail()
		pass

	def getDetail(self):
		for key in self.type:
			workload=self.handleData(key)
			self.saveFile(workload, self.type[key])
		pass
