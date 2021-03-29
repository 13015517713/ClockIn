#  用提供好的api爬取天气数据，然后发送给邮箱服务器
import requests
import json
from email.mime.text import MIMEText
import smtplib

#  邮件传输
def smtp_tran(data):
    # print(data)
    msg=MIMEText(data,'html','utf-8')
    HOST='smtp.qq.com'
    SUBJECT='汇报今天早上八点的自动打卡状况'
    # From表示发送邮件的 To表示接收邮件的邮箱
    FROM='2430278602@qq.com'
    msg['Subject']=SUBJECT
    msg['From']=FROM
    TO = ""
    with open("./config.json","r",encoding = 'utf-8') as configfile:
            config = json.load(configfile)
            TO = config["mail"]
    msg['To']=TO
    server=smtplib.SMTP(HOST,25)
    # server.set_debuglevel(1)
    # 这里填写自己的邮件码，即邮件的认证方式
    server.login(FROM,'cqrtcbeqxylkechb')
    server.sendmail(FROM,[TO],msg.as_string())
    server.quit()
# smtp_tran(get_sky())
# print(get_sky(),end='')
