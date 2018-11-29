import pandas as pd
class IWorkLoadPoints(object):
    """科室工作量得分或者按工作类别获取工作量得分接口 IWorkLoadPoints"""
    def __init__(self,iworkload):
        super(IWorkLoadPoints, self).__init__()
        self.iworkload = iworkload
        self.excelwriter=""
        pass
    def getPoints(self):	
    	pass
    def statistics(self):
        pass
    def getDetail(self):
   	 	pass	
    def handleData(self,data):
        pass
    def saveFile(self,data,sheetname):
        data.to_excel(self.excelwriter,sheetname)
		