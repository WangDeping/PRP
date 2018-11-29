import sys
import io
import time
import PathControl
import pandas as pd
from CacheWorkLoad import CacheWorkLoad
from Utils import getMonthFirstDayAndLastDay
from DepartWorkLoad import *


def main():
    print(time.strftime('%Y-%m-%d %H:%M:%S',time.localtime(time.time())))
    timeperiod=["2018-06-01","2018-06-30"]
    questionWriter=pd.ExcelWriter("问题记录.xlsx")
    workload=CacheWorkLoad(timeperiod)
    # 手术
    anawlps=AnaeWorkLoadPoints(workload)  
    anawlps.excelwriter=questionWriter
    anawlps.questionData()
    # 护理记录单/护理巡视
    nrwlps=NurseRecordPoints(workload)
    nrwlps.excelwriter=questionWriter
    nrwlps.questionData()
    
    questionWriter.save()
    pass
    
if __name__ == '__main__':
    main()
    

