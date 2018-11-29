import sys
import io
import time
import PathControl
import Utils
import pandas as pd
from Utils import getMonthFirstDayAndLastDay
from CacheWorkLoad import CacheWorkLoad
from DepartWorkLoad import *
def  main():
    print(time.strftime('%Y-%m-%d %H:%M:%S',time.localtime(time.time())))
    #timeperiod=getMonthFirstDayAndLastDay(2017,12)
    timeperiod=["2018-06-01","2018-06-30"]
    ORDER_SAVE=False#医生医嘱
    EXE_SAVE=False#护士执行
    OPERATION_SAVE=True#手术
    ADMISSION_SAVE=False#入院
    DISCHARGE_SAVE=False#出院
    ECG_SAVE=False#心电
    RECORDChECK_SAVE=False#护理病历审核
    PACS_SAVE=False#影像科工作量
    workload=CacheWorkLoad(timeperiod)
    
    # 心电
    '''
    ecgwlps=ECGPoints(workload)    
    ecgwlps.excelwriter=detailWriter
    ecgwlps.statistics()
    '''
    
    # 执行记录
    if EXE_SAVE:
        nurse_detailWriter=pd.ExcelWriter(timeperiod[0]+"至"+timeperiod[1]+"护理工作量详细记录.xlsx")
        exewlps=ExeWorkLoadPoints(workload)
        exewlps.excelwriter=nurse_detailWriter
        exewlps.getDetail()
        nurse_detailWriter.save()
    #护理巡视明细
    '''
    nurrec=NurseRecordPoints(workload)
    nurrec.excelwriter=detailWriter
    nurrec.getDetail()
    ''' 
    
    #开单记录
    if ORDER_SAVE:
        doctor_detailWriter=pd.ExcelWriter(timeperiod[0]+"至"+timeperiod[1]+"医疗工作量详细记录.xlsx")
        orderswlps=OrderPoints(workload)    
        orderswlps.excelwriter=doctor_detailWriter
        orderswlps.getDetail() 
        doctor_detailWriter.save()   
    #手术
    if OPERATION_SAVE:
        operation_detailWriter=pd.ExcelWriter(timeperiod[0]+"至"+timeperiod[1]+"手术工作量详细记录.xlsx")
        operationwlps=AnaeWorkLoadPoints(workload)   
        operationwlps.excelwriter=operation_detailWriter
        operationwlps.getDetail() 
        operation_detailWriter.save() 
    #出院结算
    if DISCHARGE_SAVE:
        discharge_detailWriter=pd.ExcelWriter(timeperiod[0]+"至"+timeperiod[1]+"出院结算详细记录.xlsx")
        dischargewlps=DischargePoints(workload)
        dischargewlps.excelwriter=discharge_detailWriter
        dischargewlps.getDetail()
        discharge_detailWriter.save()
    if ECG_SAVE:
        ecg_detailWriter=pd.ExcelWriter(timeperiod[0]+"至"+timeperiod[1]+"心电图详细记录.xlsx")
        ecgwlps=ECGPoints(workload)
        ecgwlps.excelwriter=ecg_detailWriter
        ecgwlps.getDetail()
        ecg_detailWriter.save()
    if RECORDChECK_SAVE:
        record_detailWriter=pd.ExcelWriter(timeperiod[0]+"至"+timeperiod[1]+"护理病历审核记录.xlsx")
        recordwlps=RecordCheckPoints(workload)
        recordwlps.excelwriter=record_detailWriter
        recordwlps.getDetail()
        record_detailWriter.save()
    if PACS_SAVE:
        pacs_detailWriter=pd.ExcelWriter(timeperiod[0]+"至"+timeperiod[1]+"影像科工作量.xlsx")
        pacswlps=PacsPoints(workload)
        pacswlps.excelwriter=pacs_detailWriter
        pacswlps.getDetail()
        pacs_detailWriter.save()
     # 保存到excel     
    
    

main()