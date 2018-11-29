from IWorkLoadPoints import IWorkLoadPoints
import pandas as pd
class RecordCheckPoints(IWorkLoadPoints):
	"""护理病历审核/质控护士得分,只有状态为审核的才可以计算工作量"""
	def __init__(self,iworkload):
		super(RecordCheckPoints,self).__init__(iworkload)
		self.checkworkload=iworkload.nurseRecordCheckPointsWorkload()	
		if self.checkworkload.empty:	 
			self.checkworkload=pd.DataFrame(columns=["护士姓名","工号","上报日期","病人姓名","科室","住院号"])
		else:
			self.checkworkload.columns=["护士姓名","工号","上报日期","病人姓名","科室","住院号"]
		
		pass
	def statistics(self):
		data=self.checkworkload		
		data["统计数量"]=1
		
		workload=data.groupby(["护士姓名","工号"],as_index=False)["统计数量"].sum()
		self.saveFile(workload,"护理病历审核")
		pass

	def getDetail(self):   			
		self.saveFile(self.checkworkload,"护理病历审核明细")
		pass