import io
import sys
import time

import pandas as pd

import PathControl
from CacheWorkLoad import CacheWorkLoad
from DepartWorkLoad import *
#from ExeCommonItem import ExeCommonItem
from Utils import getMonthFirstDayAndLastDay

'''数据统计'''


def main():
    #timeperiod=getMonthFirstDayAndLastDay(2018,3)
    timeperiod = ["2018-08-01", "2018-08-31"]
    nurseWriter = pd.ExcelWriter(timeperiod[0]+"至"+timeperiod[1]+"护理工作量.xlsx")
    doctorWriter = pd.ExcelWriter(timeperiod[0]+"至"+timeperiod[1]+"医疗工作量.xlsx")
    examWriter = pd.ExcelWriter(timeperiod[0]+"至"+timeperiod[1]+"特检工作量.xlsx")
    workload = CacheWorkLoad(timeperiod)
    print('开始'+time.strftime('%Y-%m-%d %H:%M:%S', time.localtime(time.time())))
    pass
    
     #临床路径
    cpwwlps=ClinicalPathwayPoints(workload)
    cpwwlps.excelwriter=doctorWriter
    cpwwlps.statistics()
    pass
    # 执行工作量
    exewlps = ExeWorkLoadPoints(workload)
    exewlps.excelwriter = nurseWriter
    exewlps.statistics()
    # 药品用法统计
    usagewlps = UsagePoints(workload)
    usagewlps.excelwriter = nurseWriter
    usagewlps.statistics()
    # 开单工作量
    orderwlps = OrderPoints(workload)
    orderwlps.excelwriter = doctorWriter
    orderwlps.statistics()
    
    # 手麻工作量
    anaewlps = AnaeWorkLoadPoints(workload)
    anaewlps.excelwriter = doctorWriter
    anaewlps.statistics()
    
    # 慢病上报
    chronicwlps = ChronicPoints(workload)
    chronicwlps.excelwriter = doctorWriter
    chronicwlps.statistics()
    # 护理病历
    nursercordwlps = NurseRecordPoints(workload)
    nursercordwlps.excelwriter = nurseWriter
    nursercordwlps.statistics()
    # 护理病历复核
    checkwlps = RecordCheckPoints(workload)
    checkwlps.excelwriter = nurseWriter
    checkwlps.statistics()
    # 护理处理医嘱
    nurseorderhanwlps = NurseOrderHandlePoints(workload)
    nurseorderhanwlps.excelwriter = nurseWriter
    nurseorderhanwlps.statistics()
    # 电子病历(上级医师查房)
    emrwlps = EMRPoints(workload)
    emrwlps.excelwriter = doctorWriter
    emrwlps.statistics()
    #质控医师
    quadocwlps=HomePagePoints(workload)
    quadocwlps.excelwriter=doctorWriter
    quadocwlps.statistics()
    # 医技检查
    #  心电检查
    ecgwlps = ECGPoints(workload)
    ecgwlps.excelwriter = examWriter
    ecgwlps.statistics()
    #影像科
    pacswlps=PacsPoints(workload)
    pacswlps.excelwriter=examWriter
    pacswlps.statistics()
    #  高压氧
    oxywlps = OxygenLocPoints(workload)
    oxywlps.excelwriter = examWriter
    oxywlps.statistics()

    # 办理出院
    dischargewlps=DischargePoints(workload)
    dischargewlps.excelwriter=nurseWriter
    dischargewlps.statistics()

    #办理入院
    admissionwlps=AdmissionPoints(workload)
    admissionwlps.excelwriter=nurseWriter
    admissionwlps.statistics()
    pass

    # 保存到文件
    nurseWriter.save()
    doctorWriter.save()
    examWriter.save()
    print('结束'+time.strftime('%Y-%m-%d %H:%M:%S', time.localtime(time.time())))
    

main()
