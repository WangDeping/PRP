from IWorkLoadPoints import IWorkLoadPoints
import pandas as pd


class DischargePoints(IWorkLoadPoints):
    """办理出院结算护士工作量"""

    def __init__(self, iworkload):
        super(DischargePoints, self).__init__(iworkload)
        self.dischargeworkload = iworkload.dischargePatientsInfo()
        self.dischargeworkload.columns = ["就诊记录", "登记号", "患者姓名", "住院号", "工号", "姓名","科室","住院费","结算日期"]
        self.dischargeworkload["数量"] = 1



    def statistics(self):
        dischargedata=self.dischargeworkload
        data=dischargedata.groupby(["工号","姓名"],as_index=False)["数量"].sum()
        self.saveFile(data,"出院结算")	
        pass

    def getDetail(self):
        self.saveFile(self.dischargeworkload, "出院结算明细")
        pass