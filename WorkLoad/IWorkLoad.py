class IWorkLoad(object):
	"""docstring for IWrokLoad"""
	def __init__(self,timeperoid):		
		self.db = "";
		self.timeperoid=timeperoid
		self.exe_columns={"执行ID":"执行ID","科室":"科室","登记号":"登记号",
		"医嘱项":"医嘱项","频次":"频次","要求执行日期":"要求执行日期",
		"工号":"工号","姓名":"姓名","数量":"数量","疗程":"疗程",
		"长期临时":"长期临时",
		"开单者工号":"开单者工号",
		"开单者姓名":"开单者姓名",
		"审核者工号":"审核者工号",
		"审核者姓名":"审核者姓名"}			
		self.operation_header=["病案号","病人姓名","手术日期","手术科室","手术名称","手术级别","手术医生","麻醉医生","麻醉方法","ASA","一助",
		"二助","巡回护士","器械护士"]
		self.order_header=["科室","登记号","病人姓名","审核者工号","审核者姓名","开单者工号","开单者姓名","医嘱项","开单日期","医嘱ID","试探数量","长期临时"]
		
	def IPExeWorkLoad(self):
		pass
	def OPExeWorkLoad(self):
		pass
	def exeWorkLoad(self):
		pass	
	def anaesthesiaWorkLoad(self):
		pass
		
		