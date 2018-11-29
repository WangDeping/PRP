from IWorkLoadPoints import IWorkLoadPoints
from OrderByQualityItem import OrderByQualityItem
import pandas as pd
from Singleton import Singleton
class OrderPoints(IWorkLoadPoints):
	"""开单工作量详情"""
	def __init__(self, iworkload):
		super(OrderPoints, self).__init__(iworkload)
		self.orders=iworkload.orderWorkLoad()
		#特殊开单项目，临时医嘱直接获取数量，长期医嘱按照执行记录获取数量
		self.specalorders=OrderByQualityItem().queryalldata()
		_singleton=Singleton(iworkload)
		self.exeworkload=_singleton.exeworkload	
		self.handleDataSource=self.handleData(self.orders)
	'''def getPoints(self):		
		result=self.handleData(self.orders)
		ordersPoints=self.orders.groupby(["开单者工号","开单者姓名","科室","医嘱项"],as_index=False)["数量"].sum()
		return ordersPoints
		pass'''
	def statistics(self):
		result=self.handleDataSource
		ordersstatistics=result.groupby(["开单者工号","开单者姓名","科室","医嘱项"],as_index=False)["数量"].sum()
		self.saveFile(ordersstatistics,"开单分档汇总")		
		verifyOrdersstatistics=result.groupby(["审核者工号","审核者姓名","科室","医嘱项"],as_index=False)["数量"].sum()
		self.saveFile(verifyOrdersstatistics,"审核医嘱分档汇总")
		pass
	def getDetail(self):
		result=self.handleDataSource
		self.saveFile(result,"开单明细")
		pass

	def handleData(self,orders):
		#删除开单人为空的项目
		tmp=orders[orders["科室"].isnull()]
		orders.drop(tmp.index,inplace=True)
		#orders.to_excel("orders.xlsx")
		tmp=orders[orders["医嘱项"].str.contains("氯化钠")]
		orders.drop(tmp.index,inplace=True)
		tmp=orders[orders["医嘱项"].str.contains("诊查费")]
		orders.drop(tmp.index,inplace=True)
		tmp=orders[orders["医嘱项"].str.contains("注射用水")]
		orders.drop(tmp.index,inplace=True)
		tmp=orders[orders["医嘱项"].str.contains("注射液")]
		orders.drop(tmp.index,inplace=True)
		tmp=orders[orders["医嘱项"].str.contains("手术申请")]
		orders.drop(tmp.index,inplace=True)
		tmp=orders[orders["医嘱项"].str.contains("一次性")]
		orders.drop(tmp.index,inplace=True)
		tmp=orders[orders["医嘱项"].str.contains("挂号")]
		orders.drop(tmp.index,inplace=True)
		tmp=orders[orders["医嘱项"].str.contains("床位")]
		orders.drop(tmp.index,inplace=True)
		tmp=orders[orders["医嘱项"].str.contains("开塞露")]
		orders.drop(tmp.index,inplace=True)
		tmp=orders[orders["科室"].str.contains("查体中心")]
		orders.drop(tmp.index,inplace=True)
		tmp=orders[orders["科室"].str.contains("超声")]
		orders.drop(tmp.index,inplace=True)
		tmp=orders[orders["科室"].str.contains("社会卫生")]
		orders.drop(tmp.index,inplace=True)
		tmp=orders[orders["科室"].str.contains("药剂配送")]
		orders.drop(tmp.index,inplace=True)
		pass
		orders["数量"]=1
		#特殊开单项：临时直接按照数量提取
		tmp=orders[(orders["长期临时"]=="临时医嘱")&(orders["医嘱项"].isin(self.specalorders['item']))]
		
		for i,row in tmp.iterrows():
			orders.at[i,"数量"]=row["试探数量"] 
		#特殊长期医嘱按照执行记录抓取数据
		#tmp=orders[(orders["长期临时"]=="长期医嘱")&(orders["医嘱项"].isin(self.specalorders['item']))]	
	
		#for i,row in tmp.iterrows():
			
			#tmp_result=self.exeworkload[self.exeworkload["执行ID"].str.contains(row["医嘱ID"])]
			#tmp_result=self.exeworkload[self.exeworkload["执行ID"].str.startswith(row["医嘱ID"])]			
				
		#	orders.at[i,"数量"]=len(self.exeworkload[self.exeworkload["执行ID"].str.startswith(row["医嘱ID"])])	
		tmp=orders[(orders["长期临时"]=="长期医嘱")&(orders["医嘱项"].isin(self.specalorders['item']))]
		orders.drop(tmp.index,inplace=True)
		pass
		tmp=self.exeworkload[(self.exeworkload["长期临时"]=="长期医嘱")&(self.exeworkload["医嘱项"].isin(self.specalorders['item']))]	
		empty=pd.DataFrame(columns=("科室","登记号","病人姓名","审核者工号","审核者姓名","开单者工号","开单者姓名","医嘱项","开单日期","医嘱ID","试探数量","长期临时"))
		for i,row in tmp.iterrows():
			empty.loc[i]=[row["科室"],row["登记号"],None,row["审核者工号"],row["审核者姓名"],row["开单者工号"],row["开单者姓名"],row["医嘱项"],row["要求执行日期"],row["执行ID"],None,row["长期临时"]]
		empty["数量"]=1		
		orders=orders.append(empty,ignore_index=True)		
		return orders
		

