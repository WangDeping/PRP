from IWorkLoadPoints import IWorkLoadPoints
from ExeCommonItem import ExeCommonItem
from ExeSpecialItem import ExeSpecialItem
from HourOrder import HourOrder
import pandas as pd
import time
from Singleton import Singleton
class ExeWorkLoadPoints(IWorkLoadPoints):
	"""门诊、病房执行工作量 ExeWorkLoad"""
	
	def __init__(self,iworkload):
		super(ExeWorkLoadPoints, self).__init__(iworkload)

		#初始化一般执行赋分标准		
		self.exeCommonGradeData=ExeCommonItem().queryalldata()
		#初始化特殊执行赋分标准
		self.exeSpecialGradeData=ExeSpecialItem().queryalldata()
		#小时医嘱
		self.exeHourOrder=HourOrder().queryalldata()
		#基础工作量
		_singleton=Singleton(iworkload)
		self.exeworkload=_singleton.exeworkload	
		

	#统计
	def statistics(self):
		gradedata=self.gradeDetail()
		gradedata=gradedata.groupby(["科室","工号","姓名","Grade"],as_index=False)["每次治疗数量"].sum()
		gradedata.sort_values(by=["科室","工号","姓名"], ascending=False)			
		self.saveFile(gradedata,"护士执行分档")	
		pass

	def getDetail(self):
		detail=self.gradeDetail()
		self.saveFile(detail,"执行明细")
		pass

	def handleData(self,data):
		exe_columns=self.iworkload.exe_columns		
		data.insert(len(self.iworkload.exe_columns),"每次治疗数量",1)#插入每次治疗数量列
		for i, row in data.iterrows():
			qty=float(row[exe_columns["数量"]])#数量
			tm=1
			if row[exe_columns["疗程"]] is  None:#把疗程为空的默认为1				
				pass
			elif "天" in row[exe_columns["疗程"]]:#去掉天,保留数字				
				tm=int(row[exe_columns["疗程"]].replace("天",""))				
				pass
			elif "付" in row[exe_columns["疗程"]]:#去掉付,保留数字	
				tm=	int(row[exe_columns["疗程"]].replace("付",""))					
				pass
			elif "周" in row[exe_columns["疗程"]]:#去掉周,保留数字		
				tm=float(row[exe_columns["疗程"]].replace("周",""))					
				pass
			data.at[i,"每次治疗数量"]=qty/tm			
		return data			
		pass
	def gradeDetail(self):
		exedata=self.handleData(self.exeworkload)	
		#exedata["科室"][exedata.医嘱项=="重症监护床位费(230元)"]="ZZYXK-重症医学科"
		exedata.loc[exedata["医嘱项"]=="重症监护床位费(230元)","科室"]="ZZYXK-重症医学科"
		###优先计算特殊项目执行
		#根据名称连接查询
		exeworkmerge=pd.merge(exedata,self.exeSpecialGradeData,how='left',left_on="医嘱项",right_on="SpecialItem")		
		#特殊项目执行		
		sp_workload=exeworkmerge[exeworkmerge["ID"].notnull()]
		sp_workload=sp_workload.drop(['ID','SpecialItem'],axis=1)		
		#普通项目执行
		common_workdata=exeworkmerge[exeworkmerge["ID"].isnull()]
		exeworkmerge=common_workdata.drop(['ID','SpecialItem','Grade'],axis=1)
		common_workloadmerge=pd.merge(exeworkmerge,self.exeCommonGradeData,how='left',left_on="医嘱项",right_on="CommonItem")
		common_workload=common_workloadmerge.drop(['ID','CommonItem'],axis=1)		
		#普通项目每次执行工作量都设置为1
		common_workload["每次治疗数量"]=1
		#普通项目中的小时医嘱除以24作为工作量
		common_workload.loc[(common_workload["频次"]=="Qh")&(common_workload["医嘱项"].isin(self.exeHourOrder)),["每次治疗数量"]]=1/24
		#汇总项目
		exedata=pd.concat([sp_workload,common_workload],ignore_index=True)	
		return exedata
		#工作量分类求和		
		gradedata=exedata.groupby(["科室","工号","姓名","Grade"],as_index=False)["每次治疗数量"].sum()
		gradedata.sort_values(by=["科室","工号","姓名"], ascending=False)
		
		return gradedata
		pass

		'''def questionData(self):
    		data=pd.read_excel('index.xlsx')
    		data.columns=['PID','EID','NURSE','D','T']
    		data.sort_values(by=['PID','D','T'],inplace=True)
    		data['Diff']=''
    		data=data.reset_index(drop=True)     		
    		for i,row in data.iterrows():
        	if(i==0):
            	continue       
        	if((row['PID']!=data.iat[i-1,0])or(row['D']!=data.iat[i-1,3])):                       
           		continue       
        	diff=datetime.combine(date.today(), row['T'])-(datetime.combine(date.today(),data.iat[i-1,4]))
        	data['Diff'][i]=diff.seconds/60        
         
    		data.saveFile('PDA执行')
    		pass'''

    
