import sys
import io
import time
import pandas as pd
sys.path.append("G:\\王德平\\Python\\PRP\\WorkLoad")
sys.path.append("G:\\王德平\\Python\\PRP\\DBFactory")
sys.path.append("G:\\王德平\\Python\\PRP\\DepartWorkLoad")
sys.path.append("G:\\王德平\\Python\\PRP\\StandardData")
from CacheWorkLoad import CacheWorkLoad
from ExeCommonItem import ExeCommonItem
from Utils import getMonthFirstDayAndLastDay
from ExeWorkLoadPoints import ExeWorkLoadPoints
from AnaeWorkLoadPoints import AnaeWorkLoadPoints
from OrderPoints import OrderPoints
from UsagePoints import UsagePoints
from ChronicPoints import ChronicPoints
from NurseRecordPoints import NurseRecordPoints
#timeperiod=getMonthFirstDayAndLastDay(2017,5)
timeperiod=["2017-06-01","2017-06-30"]
nurseWriter=pd.ExcelWriter("护理工作量.xlsx")
doctorWriter=pd.ExcelWriter("医疗工作量.xlsx")
workload=CacheWorkLoad(timeperiod)

print(time.strftime('%Y-%m-%d %H:%M:%S',time.localtime(time.time())))
exewlps=ExeWorkLoadPoints(workload)
exewlps.excelwriter=nurseWriter
exewlps.statistics()
#*******滴眼用法统计
usagewlps=UsagePoints(workload)
usagewlps.excelwriter=nurseWriter
usagewlps.statistics()
#*******开单工作量
orderwlps=OrderPoints(workload)
orderwlps.excelwriter=doctorWriter
orderwlps.statistics()
#***********手麻工作量
anaewlps=AnaeWorkLoadPoints(workload)
anaewlps.excelwriter=doctorWriter
anaewlps.statistics()
#***********慢病
chronicwlps=ChronicPoints(workload)
chronicwlps.excelwriter=doctorWriter
chronicwlps.statistics()
#**********护理病历
nusercordwlps=NurseRecordPoints(workload)
nusercordwlps.excelwriter=nurseWriter
nusercordwlps.statistics()
#***********
nurseWriter.save()
doctorWriter.save()

print(time.strftime('%Y-%m-%d %H:%M:%S',time.localtime(time.time())))
'''orderwlps=OrderPoints(workload)
orderPoints=orderwlps.getPoints()
orderPoints.to_excel("开单工作量.xlsx")'''
print(time.strftime('%Y-%m-%d %H:%M:%S',time.localtime(time.time())))
pass

