from IWorkLoadPoints import IWorkLoadPoints
import pandas as pd


class ECGPoints(IWorkLoadPoints):
    """心电图室工作量"""

    def __init__(self, iworkload):
        super(ECGPoints, self).__init__(iworkload)
        self.appworkload = iworkload.rislocApplication("XDTS-心电图室")
        self.appworkload.columns = ["日期", "患者姓名", "姓名", "报告人", "审核人", "收入","项目名称"]
        self.appworkload["数量"] = 1

    # 心电图室工作量不具体到人，只统计患者人次
    def statistics(self):
        result=self.appworkload.groupby(["项目名称"],as_index=False)["数量"].sum()        
        self.saveFile(result, "心电工作量")
        pass

    def getDetail(self):
        self.saveFile(self.appworkload, "心电图检查明细")
        pass
