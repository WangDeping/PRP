from IWorkLoadPoints import IWorkLoadPoints
import pandas as pd


class AdmissionPoints(IWorkLoadPoints):
    """办入院护士工作量"""

    def __init__(self, iworkload):
        super(AdmissionPoints, self).__init__(iworkload)
        self.admissionworkload = iworkload.admissionPatientsInfo()
        self.admissionworkload.columns = ["就诊记录", "登记号", "患者姓名", "住院号", "工号", "姓名","科室","结算日期"]
        self.admissionworkload["数量"] = 1



    def statistics(self):
        admissiondata=self.admissionworkload
        data=admissiondata.groupby(["工号","姓名"],as_index=False)["数量"].sum()
        self.saveFile(data,"办理入院")	
        pass

    def getDetail(self):
        self.saveFile(self.dischargeworkload, "办理入院明细")
        pass