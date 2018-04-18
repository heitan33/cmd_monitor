# -*- coding: utf-8 -*-

import socket,time
import smtplib,time
from email.mime.text import MIMEText
from email.header import Header
import os

global port,ip,receivers,mail_user,mail_pass
receivers = ['yyy3988@qq.com']
mail_host="smtp.ym.163.com"
mail_user="tech@hadlinks.com"
mail_pass="hadlinks88988"
ip='352-Balance'

def check_port():
	global port
	while True:
	        spam = [2181,8080,11593,11591,11571]
	        failed_port = []
	        for port in spam:
			time.sleep(1)
	                #print i
			try:
				s1 = socket.socket(socket.AF_INET,socket.SOCK_STREAM)
				s1.settimeout(2)
				result = s1.connect_ex(('localhost',port))
				print port
				print result
				s1.close()
				if int(result) == 0:
					#continue
					pass
					print("=====")
				else:
					print("ERROR1")
					warn_mail()
					while True:
						print("ERROR2")
						s2 = socket.socket(socket.AF_INET,socket.SOCK_STREAM)
						result2 = s2.connect_ex(('localhost',port))
						if int(result2) == 0:
							recovery_mail()
							break
						else:
							continue
						s2.close() 

				#s1.close()
	
			except:
				print("error except")
				continue


def warn_mail():
        global port
        message = MIMEText('%s 端口%s未监听'%(ip,port),'plain','utf-8')
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


def recovery_mail():
        global port
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
					
								

def main():
	global port
	check_port()


if __name__== "__main__":
	main()	
