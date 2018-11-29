import datetime
import time
import pandas as pd
from IWorkLoadPoints import IWorkLoadPoints


class NurseOrderHandlePoints(IWorkLoadPoints):
    '''护理处理医嘱'''

    def __init__(self, iworkload):
        super(NurseOrderHandlePoints, self).__init__(iworkload)
        self.workload = iworkload.nurseOrderHandle()
        self.workload.columns = ["工号", "姓名", "数量"]

    ''''''

    def statistics(self):
        self.saveFile(self.workload, "处理医嘱")
