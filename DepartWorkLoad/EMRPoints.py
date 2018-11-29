from IWorkLoadPoints import IWorkLoadPoints
import pandas as pd
class EMRPoints(IWorkLoadPoints):
	"""电子病历工作量"""
	def __init__(self, iworkload):
		super(EMRPoints, self).__init__(iworkload)
		self.emrwokload=iworkload.patientRounds()
		self.emrwokload.columns=["就诊ID","登记号","住院号","患者姓名","入院日期","出院日期","无用字段01","科室",
		                             "无用字段02","病区","床号","创建者ID","创建者","无用字段03","无用字段04","无用字段05",
		                             "无用字段06","无用字段07","病历类型","姓名","操作结果","提交类型" ]
		self.emrwokload["数量"]=1                        
		self.statisticsResult=pd.DataFrame(columns=["病历类型","姓名","数量"])                     
	# 明细
	def getDetail(self):
		self.saveFile(self.emrwokload,'电子病历')
		pass
	# 日常病程记录->副主任、主任医师查房
	def patientRounds(self):
		workload=self.emrwokload
		# 通过病历名称和提交类型认定为副主任医师、主任医师查房
		rounds=workload[(workload["病历类型"].isin(['主任医师查房记录','副主任医师查房记录','主治医师查房记录'])) & (workload["提交类型"].isin(['主任签名','主治签名']))]
		result=rounds.groupby(["病历类型","姓名"],as_index=False)["数量"].sum()
		return result
		pass
	# 统计
	def statistics(self):
		patientrounds=self.patientRounds()
		result=pd.concat([patientrounds,self.statisticsResult],ignore_index=True) 
		self.saveFile(result,"上级医师查房")
		pass