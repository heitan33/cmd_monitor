# -*- coding: utf-8 -*-
import os
import smtplib,commands,time,subprocess
from email.mime.text import MIMEText
from email.header import Header
import threading

spam = ['8080','8081','8082','8083',]
global port,ip
ip='test-131'
receivers = ['yyy3988@qq.com']
mail_host="smtp.qq.com"
mail_user="yyy3988@qq.com"
mail_pass="uahaibjiqzelbjih"

def action():
	global port
	while True:
		for port in spam:
			tomcat(port)

def tomcat(port):
	while True:
		os.environ['port'] = str(port)
		targ = commands.getoutput("netstat -ntulp|grep $port")
		print (targ)
		print("=====")
		if 'LISTEN' not in targ:
			warn5_mail()	
			while True:
				port = commands.getoutput("netstat -ntulp|grep $port")
				time.sleep(5)
				if 'LISTEN' not in port:
					continue
				else:
					recovery5_mail()
					break
		else:
			time.sleep(3)
		break

def main():
	global port
	action()

def warn5_mail():
	global port,mail_user,mail_pass,mail_host
        message = MIMEText('%s  %s服务停止'%(ip,port),'plain','utf-8')
        message['From'] = Header("tech")
        message['To'] = Header("wangb")
        subject = '%s端口没有监听'%port
        message['subject']= Header(subject,'utf-8')
        try:
                smtpObj = smtplib.SMTP_SSL()
                smtpObj.connect(mail_host,465)
                state=smtpObj.login(mail_user,mail_pass)
                if state[0] == 235:
                        smtpObj.sendmail(mail_user,receivers,message.as_string())
                        print ("success")
                else:
                        smtpObj.quit()
        except  smtplib.SMTPException,e:
                print e


def recovery5_mail():
	global port,mail_user,mail_pass,mail_host
        message = MIMEText('%s %s端口正常'%(ip,port),'plain','utf-8')
        message['From'] = Header("tech")
        message['To'] = Header("wangb")
        subject = '%s端口已正常监听'%port
        message['subject']= Header(subject,'utf-8')
        try:
                smtpObj = smtplib.SMTP_SSL()
                smtpObj.connect(mail_host,465)   
                state=smtpObj.login(mail_user,mail_pass)
                if state[0] == 235:
                        smtpObj.sendmail(mail_user,receivers,message.as_string())
                        print ("success")
                else:
                        smtpObj.quit()
        except  smtplib.SMTPException,e:
                print e


if __name__ == "__main__":
	main()
