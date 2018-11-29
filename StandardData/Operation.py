class Operation(object):
	"""docstring for Operation"""
	def __init__(self, arg="1"):
		super(Operation, self).__init__()		
		self.level=arg#手术级别
		if self.level=="1":
			self.operator=40#主刀分数
			self.assistant1=20#一助分数
			self.assistant2=10#二助分数
			self.circuit=70#器械护士分数
			self.instrument=70#巡回护士分数
		elif self.level=="2":
			self.operator=100#主刀分数
			self.assistant1=80#一助分数
			self.assistant2=60#二助分数
			self.circuit=130#器械护士分数
			self.instrument=130#巡回护士分数
		elif self.level=="3":
			self.operator=150#主刀分数
			self.assistant1=90#一助分数
			self.assistant2=70#二助分数
			self.circuit=170#器械护士分数
			self.instrument=170#巡回护士分数
		elif self.level=="4":
			self.operator=180#主刀分数
			self.assistant1=130#一助分数
			self.assistant2=80#二助分数
			self.circuit=250#器械护士分数
			self.instrument=250#巡回护士分数
		elif self.level=="剖宫产":
			self.operator=70#主刀分数
			self.assistant1=50#一助分数
			self.assistant2=30#二助分数
			self.circuit=130#器械护士分数
			self.instrument=130#巡回护士分数
		
	def queryalldata(self):
		return{"1":Operation("1"),"2":Operation("2"),"3":Operation("3"),"4":Operation("4"),"剖宫产":Operation("剖宫产")}
		pass