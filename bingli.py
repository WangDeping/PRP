from ftplib import FTP            #加载ftp模块
ftp=FTP()                         #设置变量
ftp.set_debuglevel(2)             #打开调试级别2，显示详细信息
ftp.connect("192.168.254.7",21)          #连接的ftp sever和端口
ftp.login("pis","by@dhcc=2012")      #连接的用户名，密码
print(ftp.dir())