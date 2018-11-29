from IWorkLoadPoints import IWorkLoadPoints
import pandas as pd
import time
import datetime
class NurseRecordPoints(IWorkLoadPoints):
	"""护理病历记录"""
	def __init__(self, iworkload):
		super(NurseRecordPoints, self).__init__(iworkload)
		self.recordtype=["Y","E","W","X","TT"]
		self.iworkload=iworkload
	#数据预处理
	def handleData(self,type=""):
		dataframe=pd.DataFrame(columns=["工号","姓名","登记号","住院号","患者姓名","病区","记录日期","记录时间","入院日期","巡视级别"])
		if type=="":
			for t in self.recordtype:
				recordworkload=self.iworkload.nurseRecordWorkload(t)
				if len(recordworkload)==0:
					continue				
				recordworkload.columns=["工号","姓名","登记号","住院号","患者姓名","病区","记录日期","记录时间","入院日期"]
				recordworkload["巡视级别"]=t	
				dataframe=pd.concat([dataframe,recordworkload],ignore_index=True) 				
				pass

			return dataframe
		else:
			recordworkload=self.iworkload.nurseRecordWorkload(type)
			recordworkload.columns=["工号","姓名","登记号","住院号","患者姓名","病区","记录日期","记录时间","入院日期"]
			recordworkload["巡视级别"]=type			
			return recordworkload

		pass	
	def statistics(self):
		dataframe=pd.DataFrame(columns=["工号","姓名","病区","巡视级别","统计数量"])
		
		for t in self.recordtype:
			self.recordworkload=self.iworkload.nurseRecordWorkload(t)
			if len(self.recordworkload)==0:
				continue	
			self.recordworkload.columns=["工号","姓名","登记号","住院号","患者姓名","病区","记录日期","记录时间","入院日期"]
			self.recordworkload["统计数量"]=1
			self.recordworkload["巡视级别"]=t
			result=self.recordworkload.groupby(["工号","姓名","病区","巡视级别"],as_index=False)["统计数量"].sum()
			dataframe=pd.concat([dataframe,result],ignore_index=True) 
		finalResult=dataframe.groupby(["工号","姓名","病区","巡视级别"],as_index=False)["统计数量"].sum()
		self.saveFile(finalResult,"护理巡视")
		pass
	#明细
	def getDetail(self):
		levelRecord=self.handleData()		
		levelRecord.sort_values(by=['住院号',"巡视级别",'记录日期',"记录时间"],ascending=[True,True,True,True],inplace=True) 
		levelRecord.reset_index(drop=True,inplace=True)
		levelRecord["间隔"]=0		
		max_rowindex=len(levelRecord)		
		for i,row in levelRecord.iterrows():
			if max_rowindex==i+1:#到了最后一行
				break
			else:
				currentID=row['住院号']
				nextID=levelRecord.at[i+1,'住院号']				
				#print(currentTime)		
				if currentID==nextID:#同一个住院病号
					currentTime=datetime.datetime.strptime(row["记录日期"]+" "+row["记录时间"],"%Y-%m-%d %H:%M:%S")
					nextTime=datetime.datetime.strptime(levelRecord.at[i+1,'记录日期']+" "+levelRecord.at[i+1,'记录时间'],"%Y-%m-%d %H:%M:%S")					
					diff=((nextTime-currentTime).seconds/60)
					levelRecord.at[i+1,'间隔']=int(diff)
				else:
					continue
		self.saveFile(levelRecord,"护理巡视")
		return levelRecord
		
	def questionData(self):		
		#
		levelRecord=self.handleData()
		levelRecord.sort_values(by=['住院号',"巡视级别",'记录日期',"记录时间"],ascending=[True,True,True,True],inplace=True) 
		levelRecord.reset_index(drop=True,inplace=True)
		levelRecord["间隔"]=0
		
		max_rowindex=len(levelRecord)		
		for i,row in levelRecord.iterrows():
			if max_rowindex==i+1:#到了最后一行
				break
			else:
				currentID=row['住院号']
				nextID=levelRecord.at[i+1,'住院号']				
				#print(currentTime)		
				if currentID==nextID:#同一个住院病号
					currentTime=datetime.datetime.strptime(row["记录日期"]+" "+row["记录时间"],"%Y-%m-%d %H:%M:%S")
					nextTime=datetime.datetime.strptime(levelRecord.at[i+1,'记录日期']+" "+levelRecord.at[i+1,'记录时间'],"%Y-%m-%d %H:%M:%S")					
					diff=((nextTime-currentTime).seconds/60)
					levelRecord.at[i+1,'间隔']=int(diff)
				else:
					continue
		#		
		tmp=levelRecord[levelRecord["间隔"]==0]#删掉每个病号第一次记录		
		levelRecord.drop(tmp.index,inplace=True)
		
		#求各级别的平均间隔时间
		levelRecordstatistics=levelRecord.groupby(["病区","巡视级别"])["间隔"].mean()
		self.saveFile(levelRecordstatistics,"护理巡视平均")
		return levelRecordstatistics			
			
		