class HourOrder(object):
	"""docstring for HourOrder"""
	def __init__(self, arg=""):
		super(HourOrder, self).__init__()
		self.arg = arg
	
	def queryalldata(self):
		return ["血氧饱和度监测",
		"胰岛素泵持续皮下注射胰岛素",
		"氧气吸入(加压给氧加收)",
		"心电监测",
		"氧气吸入"]#小时医嘱
		pass