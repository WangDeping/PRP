from IWorkLoadPoints import IWorkLoadPoints
from AnesthetistItem import AnesthetistItem
from ASA import ASA
from Operation import Operation
import pandas as pd
class AnaeWorkLoadPoints(IWorkLoadPoints):
	"""手术麻醉工作量统计，根据申请单统计"""
	def __init__(self, iworkload):
		super(AnaeWorkLoadPoints, self).__init__(iworkload)
		self.anestGradeData=AnesthetistItem().queryalldata()
		self.operationGradeData=Operation().queryalldata()
		self.asaGradeData=ASA.queryalldata()
		#手术申请单
		self.anaeworkload=self.iworkload.anaesthesiaWorkLoad()
	def getPoints(self):
		points=self.handleData(self.anaeworkload)
		return points
		pass
	def getDetail(self):
		self.saveFile(self.anaeworkload,"手术申请单")
		pass
	def questionData(self):
		data=self.anaeworkload
		repeat_operationData=data[data.duplicated(["手术日期","病案号","手术名称"])]#重复申请单
		self.saveFile(repeat_operationData,"重复手术")
		pass
	#
	def statistics(self):
		
		data=self.anaeworkload
		repeat_operationData=data[data.duplicated(["手术日期","病案号","手术名称"])]#重复申请单
		self.saveFile(repeat_operationData,"重复手术")
		data.drop(repeat_operationData.index,inplace=True)#去掉重复申请单
		data["统计数量"]=1
		#把剖宫产手术单独化为剖宫产级别
		
		data.loc[data["手术名称"].str.contains("剖宫产"),"手术级别"]="剖宫产"
		
		operatorWorkLoad=data.groupby(["手术医生","手术级别"],as_index=False)["统计数量"].sum()
		self.saveFile(operatorWorkLoad,"主刀")
		assistant1WorkLoad=data.groupby(["一助","手术级别"],as_index=False)["统计数量"].sum()
		self.saveFile(assistant1WorkLoad,"一助")
		assistant2WorkLoad=data.groupby(["二助","手术级别"],as_index=False)["统计数量"].sum()
		self.saveFile(assistant2WorkLoad,"二助")
		asaworkload=data.groupby(["麻醉医生","ASA"],as_index=False)["统计数量"].sum()
		self.saveFile(asaworkload,"ASA")
		circuitPoints=self.__NurseWorkLoadPoints("巡回护士",data)#
		self.saveFile(circuitPoints,"巡回护士")
		instrumentPoints=self.__NurseWorkLoadPoints("器械护士",data)#
		self.saveFile(instrumentPoints,"器械护士")
		#****************
		repeat=data[data.duplicated(['手术日期','病案号',"手术医生"])]#查询出同一台次手术的重复申请单
		data.drop(repeat.index,inplace=True)#在源表里删除重复麻醉台次
		anesthetistPoints=self.__AnesthetistWorkLoadPoints(data)#	
		anesthetistPoints.columns=["姓名","分数"]
		self.saveFile(anesthetistPoints,"麻醉得分")
		pass

	def handleData(self,data):
		repeat_operationData=data[data.duplicated(["手术日期","病案号","手术名称"])]#重复申请单
		repeat_operationData.to_excel("重复手术.xlsx")
		data.drop(repeat_operationData.index,inplace=True)#去掉重复申请单
		data["统计数量"]=1	
		pass
		operatorPoints=self.__OperatorWorkLoadPoints(data)#手术医生
		operatorPoints.columns=["姓名","分数"]
		pass
		circuitPoints=self.__NurseWorkLoadPoints("巡回护士",data)#
		instrumentPoints=self.__NurseWorkLoadPoints("器械护士",data)#
		circuitPoints.columns=["姓名","分数"]
		instrumentPoints.columns=["姓名","分数"]
		nursePoints=pd.concat([circuitPoints,instrumentPoints],ignore_index=True)	
		nursePoints=nursePoints.groupby(["姓名"],as_index=False)["分数"].sum()		
		pass
		#ASA得分
		asaPoints=self.__ASAWorkLoadPoints(data)#
		asaPoints.columns=["姓名","分数"]
		pass
		#麻醉医师统计工作量：麻醉方式以及ASA分级
		#麻醉工作量统计，根据手术日期和住院号、手术医师、麻醉医师确定是否为同一台手术，不做重复统计	
		#麻醉涉及删除源数据操作，必须最后一步统计	
		#一台手术多种麻醉方式的只统计麻醉方式赋分最高的，数据源中的麻醉方式是以逗号“,”分隔的
		repeat=data[data.duplicated(['手术日期','病案号',"手术医生"])]#查询出同一台次手术的重复申请单
		data.drop(repeat.index,inplace=True)#在源表里删除重复麻醉台次
		anesthetistPoints=self.__AnesthetistWorkLoadPoints(data)#	
		anesthetistPoints.columns=["姓名","分数"]
		pass
		points=pd.concat([operatorPoints,nursePoints,asaPoints,anesthetistPoints],ignore_index=True)
		return points
		pass
	#主刀、一助、二助统计：
	def __OperatorWorkLoadPoints(self,operationData):
		OperatorWorkLoad=operationData.groupby(["手术医生","手术级别"],as_index=False)["统计数量"].sum()
		OperatorWorkLoad["分数"]=0
		for i,row in OperatorWorkLoad.iterrows():
			OperatorWorkLoad.at[i,"分数"]=self.operationGradeData[row["手术级别"]].operator*row["统计数量"]
		operationPoints=OperatorWorkLoad.groupby(["手术医生"],as_index=False)["分数"].sum()
		#一助工作量统计
		Assistant1WorkLoad=operationData.groupby(["一助","手术级别"],as_index=False)["统计数量"].sum()
		Assistant1WorkLoad["分数"]=0
		for i,row in Assistant1WorkLoad.iterrows():
			Assistant1WorkLoad.at[i,"分数"]=self.operationGradeData[row["手术级别"]].assistant1*row["统计数量"]
		assistant1Points=Assistant1WorkLoad.groupby(["一助"],as_index=False)["分数"].sum()
		assistant1Points.columns=["手术医生","分数"]#给列重新命名方便拼接
		
		#二助统计
		Assistant2WorkLoad=operationData.groupby(["二助","手术级别"],as_index=False)["统计数量"].sum()
		Assistant2WorkLoad["分数"]=0
		for i,row in Assistant2WorkLoad.iterrows():
			Assistant2WorkLoad.at[i,"分数"]=self.operationGradeData[row["手术级别"]].assistant2*row["统计数量"]
		assistant2Points=Assistant2WorkLoad.groupby(["二助"],as_index=False)["分数"].sum()
		assistant2Points.columns=["手术医生","分数"]#给列重新命名方便拼接
		result=pd.concat([operationPoints,assistant1Points,assistant2Points],ignore_index=True)		
		allPoints=result.groupby(["手术医生"],as_index=False)["分数"].sum()		
		return allPoints
		pass
	
	#巡回、器械统计方法
	def __NurseWorkLoadPoints(self,nurseClass,operationData):
		#把巡回器械先进行统计
		__NurseWorkLoad=operationData.groupby([nurseClass,"手术级别"],as_index=False)["统计数量"].sum()
		#筛选多人组合工作的手术通知单
		Sub_NurseWorkLoad=__NurseWorkLoad[__NurseWorkLoad[nurseClass].str.contains(",")]
		#需要对多人的进行计算,主要是以“,”拆开计算
		Need_ReCountList=[]
		for ix, row in Sub_NurseWorkLoad.iterrows():
			#几个巡回(器械)护士
			nurse_counts=row[nurseClass].count(",")+1
			#护士名字
			nurse_name=row[nurseClass].split(",")
			for c in range(nurse_counts):
				Need_ReCountList.append([nurse_name[c],row["手术级别"],row["统计数量"]/nurse_counts])
		Need_RecountDataFrame=pd.DataFrame(Need_ReCountList,columns=[nurseClass,'手术级别','统计数量'])
		#删除筛选的多人组合的巡回或器械护士
		__NurseWorkLoad.drop(Sub_NurseWorkLoad.index,inplace=True)
		#把重新计算的多人组合拆开后添加到原统计表中
		NurseWorkLoad=__NurseWorkLoad.append(Need_RecountDataFrame)
		result=NurseWorkLoad.groupby([nurseClass,"手术级别"],as_index=False)["统计数量"].sum()
		#计算分数
		result["分数"]=0
		for i,row in result.iterrows():
			result.at[i,"分数"]=self.operationGradeData[row["手术级别"]].instrument*row["统计数量"]#巡回器械赋分一样
		nursePoints=result.groupby(nurseClass,as_index=False)["分数"].sum()
		return nursePoints
	#麻醉统计方法
	def __AnesthetistWorkLoadPoints(self,operationData):
				
		Need_RecountList=[]
		__AnesthetistWorkLoad=operationData.groupby(["麻醉医生","麻醉方法"],as_index=False)["统计数量"].sum()
		#筛选含有多种麻醉方式的子集
		Sub_AneWorkLoad=__AnesthetistWorkLoad[__AnesthetistWorkLoad["麻醉方法"].str.contains(",")]
		#遍历
		for ix, row in Sub_AneWorkLoad.iterrows():
			#分割每行的麻醉方法
			#AneTypesCount=row["麻醉方法"].count(",")+1
			AneTypes=row["麻醉方法"].split(",")
			pointsList=[]
			for key in AneTypes:
				if key=='无':
					continue
				pointsList.append(self.anestGradeData[key])
			Need_RecountList.append([row["麻醉医生"],max(pointsList),row["统计数量"]])
		Need_RecountDataFrame=pd.DataFrame(Need_RecountList,columns=['麻醉医生','麻醉方法','统计数量'])
		__AnesthetistWorkLoad.drop(Sub_AneWorkLoad.index,inplace=True)		
		__AnesthetistWorkLoad["分数"]=0
		Need_RecountDataFrame["分数"]=0			
		for i ,row in __AnesthetistWorkLoad.iterrows():
			__AnesthetistWorkLoad.at[i,"分数"]=self.anestGradeData[row["麻醉方法"]]*row["统计数量"]
		
		for i,row in Need_RecountDataFrame.iterrows():
			Need_RecountDataFrame.at[i,"分数"]=row["麻醉方法"]*row["统计数量"]
		AnesthetistWorkLoad=__AnesthetistWorkLoad.append(Need_RecountDataFrame)		
		anepoints=AnesthetistWorkLoad.groupby(["麻醉医生"],as_index=False)["分数"].sum()
		return anepoints
		pass
	#ASA统计
	def __ASAWorkLoadPoints(self,operationData):
		asaworkload=operationData.groupby(["麻醉医生","ASA"],as_index=False)["统计数量"].sum()	
		asaworkload["分数"]=0
		for i,row in asaworkload.iterrows():
			asaworkload.at[i,"分数"]=self.asaGradeData[row["ASA"]]*row["统计数量"]
			#print(self.asaGradeData["Ⅰ"].asa,row["统计数量"])
		asapoints=asaworkload.groupby(["麻醉医生"],as_index=False)["分数"].sum()
		return asapoints