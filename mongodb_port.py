# -*- coding: utf-8 -*-
import smtplib,commands,time,subprocess
from email.mime.text import MIMEText
from email.header import Header
import os
import threading

global receivers,ip
receivers = ['yyy3988@qq.com']
output = subprocess.Popen('curl ifconfig.me',stdout=subprocess.PIPE,stderr=subprocess.PIPE,shell=True)
output.wait()
ip=output.stdout.read()
print(ip)

def mongod():
	while True:
		port = commands.getoutput("sudo lsof -i :27017")
		if 'LISTEN' not in port:
			warn5_mail()
			commands.getoutput("sudo ./mongod --dbpath /data/db --logpath /data/mongodb-linux-x86_64-2.6.9/logs/log --fork --port 27017 --auth")
			time.sleep(10)
			print("email")
			while True:
				time.sleep(10)
				port = commands.getoutput("sudo lsof -i :27017")
				if 'LISTEN' not in port:
					continue
				else:
					recovery5_mail()
					break
		else:
			time.sleep(10)
			continue

def warn5_mail():
	mail_host="smtp.ym.163.com"
	mail_user="wangb@hadlinks.com"
	mail_pass="wb19911010"
	message = MIMEText('%s lumitek mongoDB shutdown'%ip,'plain','utf-8')
	message['From'] = Header("tech")
	message['To'] = Header("wangb")
	subject = 'mongodb shutdown'
	message['subject']= Header(subject,'utf-8')
	try:
		smtpObj = smtplib.SMTP()
		smtpObj.connect(mail_host,25)	
		state=smtpObj.login(mail_user,mail_pass)
		if state[0] == 235:
			smtpObj.sendmail('wangb@hadlinks.com',receivers,message.as_string())
			print ("success")
		else:
			smtpObj.quit()
	except	smtplib.SMTPException,e:
		print e

def recovery5_mail():
	mail_host="smtp.ym.163.com"
	mail_user="wangb@hadlinks.com"
	mail_pass="wb19911010"
	message = MIMEText('%s lumitek mongoDB recover'%ip,'plain','utf-8')
	message['From'] = Header("tech")
	message['To'] = Header("wangb")
	subject = 'mongoDB recover already'
	message['subject']= Header(subject,'utf-8')
	try:
		smtpObj = smtplib.SMTP()
		smtpObj.connect(mail_host,25)	
		state=smtpObj.login(mail_user,mail_pass)
		if state[0] == 235:
			smtpObj.sendmail('wangb@hadlinks.com',receivers,message.as_string())
			print ("success")
		else:
			smtpObj.quit()
	except	smtplib.SMTPException,e:
		print e	

def main():
	mongod()

if __name__== "__main__":
	main()
