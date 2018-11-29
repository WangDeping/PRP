import sys
import time
import pandas as pd
import PathControl
from CacheWorkLoad import CacheWorkLoad
from NurseRecordPoints import NurseRecordPoints
import Utils
from DepartWorkLoad import *
def  main():
    print(time.strftime('%Y-%m-%d %H:%M:%S',time.localtime(time.time())))
    timeperiod=["2018-07-01","2018-07-31"]
    #detailWriter=pd.ExcelWriter("护理记录.xlsx")
    #doctorWriter=pd.ExcelWriter("开单测试.xlsx")
    operaWriter=pd.ExcelWriter("手术.xlsx")
    workload=CacheWorkLoad(timeperiod)
    '''
    orderwlps = OrderPoints(workload)
    orderwlps.excelwriter = doctorWriter
    orderwlps.statistics()
    
    nurrec=NurseRecordPoints(workload)
    nurrec.excelwriter=detailWriter
    nurrec.getDetail()
    '''
    anaewlps = AnaeWorkLoadPoints(workload)
    anaewlps.excelwriter = operaWriter
    anaewlps.statistics()
     # 保存到excel     
    #detailWriter.save()
    #doctorWriter.save()
    operaWriter.save()
main()
