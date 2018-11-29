from IWorkLoadPoints import IWorkLoadPoints

class HomePagePoints(IWorkLoadPoints):
   

	def __init__(self, iworkload):
		super(HomePagePoints, self).__init__(iworkload)
		self.homepageInfo=iworkload.homePageInfo()
		self.homepageInfo.columns=["住院号","患者姓名","出院日期","科主任","科主任工号","质控医师","质控医师工号"]
		self.homepageInfo["数量"]=1
	
    
	def statistics(self):
		#print(self.homepageInfo)
		ordersstatistics=self.homepageInfo.groupby(["质控医师","质控医师工号"],as_index=False)["数量"].sum()
		self.saveFile(ordersstatistics,"质控医师")		
		pass

	
	def getDetail(self):
		self.saveFile(self.homepageInfo,"质控医师")
		pass
