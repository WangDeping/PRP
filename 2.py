from Utils import getPinyin
import pandas as pd

a=pd.read_excel("需要新增加的内科.xlsx")
for i,row in a.iterrows():
    s=a.iat[i,0]
    kh=s.find("(")
    if kh>0:
        s=s[0:kh]

    print(getPinyin(s))
    #print(a.iat[i,0])