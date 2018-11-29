import pyodbc
import pandas as pd
import os
def  main():
    constr= "DSN=DHCAPP;UID=_system;PWD=sys;"
    
    def exequery(querytext):
        conn=pyodbc.connect(constr)
        cursor=conn.cursor()
        cursor.execute(querytext)
        result = cursor.fetchall()	
        cursor.close()	
        conn.close()
        return result
        pass
    result=exequery("CALL web.WJWDATA2016()")
    data=pd.DataFrame.from_records(result)
    data.to_excel("数据统计.xlsx")
main()