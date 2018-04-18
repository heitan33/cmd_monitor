# -*- coding: utf-8 -*-

import os
import time
import socket
import smtplib
from email.mime.text import MIMEText
from email.header import Header

receivers = ['yyy3988@qq.com']

spam = {'121.40.115.131 80':'lideHTTP',
		'120.26.109.144 998':'fhsHTTPS',
		'120.26.81.158 80':'YIMAO-https',
		'121.43.114.225 15593':'acuma-TCP',
		'121.43.114.225 15573':'TCP',
		'121.40.115.131 10000':'TC',
		'42.228.5.151 43573':'TCP',
		'120.27.201.179 43573':'TCP',
		}

def main():
	global x,y,k,v
	while True:
		for k,v in spam.items():
			k=k.split(' ')
			x = k[0]
			y = k[1]
			k=''.join(k)
			v=str(v)
			tor()	
		time.sleep(300)

def tor():
	global x,y
	s = socket.socket()
	s.settimeout(3)
	x = str(x)
	y = int(y)
	host = (x,y)
	try:
		s.connect(host)
		print ("''''''")
	except socket.error as e:
		warn_mail()
		print ("warn!!!!!!")
		
def warn_mail():
	mail_host="smtp.ym.163.com"
	mail_user="wangb@hadlinks.com"
	mail_pass="wb19911010"
	message = MIMEText('%s: %s端口未监听，%s不可访问'%(x,y,v),'plain','utf-8')
	message['From'] = Header("tech")
	message['To'] = Header("wangb")
	subject = ('%s: %s端口未正常监听' %(x,y))
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

if __name__== "__main__":
	main()	