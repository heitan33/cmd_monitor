# -*- coding: utf-8 -*-
import smtplib,commands,time
from multiprocessing import Process
from email.mime.text import MIMEText
from email.header import Header
import os
import threading
global receivers
receivers = ['yyy3988@qq.com']

ip=commands.getstatusoutput("ip addr|grep eth1|grep inet|awk '{print $2}'")

ip=ip[1]
ip=''.join(ip)

def cpu_stat():
	global i,cpu
	i=0
	while True:
		cpu=commands.getoutput("iostat|sed -n '3,4p'|awk '{print $NF}'|sed -n '2p'")
		#cpu=os.system("iostat|sed -n '3,4p'|awk '{print $NF}'|sed -n '2p'")
		if float(cpu) < 60:
			print ("......")
			i=i+1	
			print(i)
			if(i==3):
				print("WARNING-cpu")
				warn_mail()
				while i==3:
					cpu=commands.getoutput("iostat|sed -n '3,4p'|awk '{print $NF}'|sed -n '2p'")
					if float(cpu) >=60:
						time.sleep(30)
						i=0
						recovery_mail()
						break
					else:
						continue
			else:
				pass
		else:
			i=0
#			continue
#		time.sleep(30)
#		continue


def hardware_stat():
	global di,nf
	di=0
	while True:
		nf=commands.getoutput("iostat|grep vdb|awk '{print $4}'")		
		try:	
			if float(nf) >= 500:
				print ("......")
				di=di+1
				print(di)
				if(di==3):
					print("WARNING-diskIO")
					warn1_mail()
					while di==3:
						nf=commands.getoutput("iostat|grep vdb|awk '{print $4}'")
						if float(nf) < 500:
							time.sleep(30)
							di=0
							recovery1_mail()
							break
						else:
							continue
				else:
					pass	
			else:	
				di=0
#			time.sleep(30)
		except:
			continue


def disk_stat():
	global de,disk
	de=0
	while True:
		try:
			disk=commands.getoutput("df -h|awk '{print $5}'|sed '1d'|xargs")
			disk=disk.split('%')
			for dev in disk.split('%'): 
				if int(dev) > 80:
					print ("......")
					warn4_mail()					
				else:
					continue
#				time.sleep(30)
		except:
			continue
		

def free_stat():
	global fe,buff
	fe=0
	while True:
		buff=commands.getoutput("free -m|sed '1d'|grep buffers|awk '{print $4}'")	
		if float(buff) <= 1500:
			print ("......")
			fe=fe+1
			print(fe)
			if(fe==3):
				print("WARNING-memory")
				warn2_mail()
				while fe==3:
					buff=commands.getoutput("free -m|sed '1d'|grep buffers|awk '{print $4}'")	
					if  float(buff) > 1500:
						time.sleep(30)
						recovery2_mail()
						fe=0
						break
					else:
						continue
			else:
				pass	
		else:	
			fe=0
#		time.sleep(30)
		continue


def load_stat():
	global load,lo
	lo=0
	while True:
		try:
			load=commands.getoutput("uptime|awk -F, '{print $NF}'")
#		float(load)	
			if float(load) >= 3:
#				print("WARNING-loaded")
				lo=lo+1
				if lo==1:
					print("WARNING-Loaded")
					warn3_mail() 
					while lo == 1:
						load=commands.getoutput("uptime|awk -F, '{print $NF}'")
						if float(load) < 3:
							time.sleep(30)
							recovery3_mail()
							lo=0
						else:
							continue
				else:
					pass
		except:	
#		time.sleep(30)
			continue


def recovery_mail():
	mail_host="smtp.ym.163.com"
	mail_user="wangb@hadlinks.com"
	mail_pass="wb19911010"
#sender = 'from@runoob.com'
#sender= 'pop.ym.163.com'
	message = MIMEText('%s CPU空闲率恢复正常 %s'%(ip,cpu),'plain','utf-8')
	message['From'] = Header("tech")
	message['To'] = Header("wangb")
	subject = 'CPU使用率过高'
	message['subject']= Header(subject,'utf-8')
	try:
		smtpObj = smtplib.SMTP()
		smtpObj.connect(mail_host,25)	
		state=smtpObj.login(mail_user,mail_pass)
		if state[0] == 235:
#	smtpObj.sendmail(sender, receivers, message)
			smtpObj.sendmail('wangb@hadlinks.com',receivers,message.as_string())
			print ("success")
		else:
			smtpObj.quit()
	except	smtplib.SMTPException,e:
		print e


def recovery1_mail():
	mail_host="smtp.ym.163.com"
	mail_user="wangb@hadlinks.com"
	mail_pass="wb19911010"
#sender = 'from@runoob.com'
#sender= 'pop.ym.163.com'
	message = MIMEText('%s 硬盘IO恢复正常 %s'%(ip,nf),'plain','utf-8')
	message['From'] = Header("tech")
	message['To'] = Header("wangb")
	subject = '硬盘IO恢复正常'
	message['subject']= Header(subject,'utf-8')
	try:
		smtpObj = smtplib.SMTP()
		smtpObj.connect(mail_host,25)	
		state=smtpObj.login(mail_user,mail_pass)
		if state[0] == 235:
#	smtpObj.sendmail(sender, receivers, message)
			smtpObj.sendmail('wangb@hadlinks.com',receivers,message.as_string())
			print ("success")
		else:
			smtpObj.quit()
	except	smtplib.SMTPException,e:
		print e


def recovery2_mail():
	mail_host="smtp.ym.163.com"
	mail_user="wangb@hadlinks.com"
	mail_pass="wb19911010"
#sender = 'from@runoob.com'
#sender= 'pop.ym.163.com'
	message = MIMEText('%s 内存使用率恢复正常 %s'%(ip,buff),'plain','utf-8')
	message['From'] = Header("tech")
	message['To'] = Header("wangb")
	subject = '内存使用率恢复正常'
	message['subject']= Header(subject,'utf-8')
	try:
		smtpObj = smtplib.SMTP()
		smtpObj.connect(mail_host,25)	
		state=smtpObj.login(mail_user,mail_pass)
		if state[0] == 235:
#	smtpObj.sendmail(sender, receivers, message)
			smtpObj.sendmail('wangb@hadlinks.com',receivers,message.as_string())
			print ("success")
		else:
			smtpObj.quit()
	except	smtplib.SMTPException,e:
		print e

def recovery3_mail():
	mail_host="smtp.ym.163.com"
	mail_user="wangb@hadlinks.com"
	mail_pass="wb19911010"
#sender = 'from@runoob.com'
#sender= 'pop.ym.163.com'
	message = MIMEText('%s 负载恢复正常 %s'%(ip,load),'plain','utf-8')
	message['From'] = Header("tech")
	message['To'] = Header("wangb")
	subject = '负载恢复正常'
	message['subject']= Header(subject,'utf-8')
	try:
		smtpObj = smtplib.SMTP()
		smtpObj.connect(mail_host,25)	
		state=smtpObj.login(mail_user,mail_pass)
		if state[0] == 235:
#	smtpObj.sendmail(sender, receivers, message)
			smtpObj.sendmail('wangb@hadlinks.com',receivers,message.as_string())
			print ("success")
		else:
			smtpObj.quit()
	except	smtplib.SMTPException,e:
		print e


def warn_mail():
	mail_host="smtp.ym.163.com"
	mail_user="wangb@hadlinks.com"
	mail_pass="wb19911010"
#sender = 'from@runoob.com'
#sender= 'pop.ym.163.com'
#	receivers = ['yyy3988@qq.com','xbwen@hadlinks.com']
	message = MIMEText('%s CPU空闲率过低 %s'%(ip,cpu),'plain','utf-8')
	message['From'] = Header("tech")
	message['To'] = Header("wangb")
	subject = 'CPU使用率过高'
	message['subject']= Header(subject,'utf-8')
	try:
		smtpObj = smtplib.SMTP()
		smtpObj.connect(mail_host,25)	
		state=smtpObj.login(mail_user,mail_pass)
		if state[0] == 235:
#	smtpObj.sendmail(sender, receivers, message)
			smtpObj.sendmail('wangb@hadlinks.com',receivers,message.as_string())
			print ("success")
		else:
			smtpObj.quit()
	except	smtplib.SMTPException,e:
		print e


def warn1_mail():
	mail_host="smtp.ym.163.com"
	mail_user="wangb@hadlinks.com"
	mail_pass="wb19911010"
#sender = 'from@runoob.com'
#sender= 'pop.ym.163.com'
#	receivers = ['yyy3988@qq.com']
	message = MIMEText('%s 磁盘写入速率过高 %s'%(ip,nf),'plain','utf-8')
	message['From'] = Header("tech")
	message['To'] = Header("wangb")
	subject = '磁盘写入速率过高'
	message['subject']= Header(subject,'utf-8')
	try:
		smtpObj = smtplib.SMTP()
		smtpObj.connect(mail_host,25)	
		state=smtpObj.login(mail_user,mail_pass)
		if state[0] == 235:
#	smtpObj.sendmail(sender, receivers, message)
			smtpObj.sendmail('wangb@hadlinks.com',receivers,message.as_string())
			print ("success")
		else:
			smtpObj.quit()
	except	smtplib.SMTPException,e:
		print e		


def warn2_mail():
	mail_host="smtp.ym.163.com"
	mail_user="wangb@hadlinks.com"
	mail_pass="wb19911010"
#sender = 'from@runoob.com'
#sender= 'pop.ym.163.com'
#	receivers = ['yyy3988@qq.com']
	message = MIMEText('%s 内存使用率过高 %s '%(ip,buff),'plain','utf-8')
	message['From'] = Header("tech")
	message['To'] = Header("wangb")
	subject = '内存使用率过高'
	message['subject']= Header(subject,'utf-8')
	try:
		smtpObj = smtplib.SMTP()
		smtpObj.connect(mail_host,25)	
		state=smtpObj.login(mail_user,mail_pass)
		if state[0] == 235:
#	smtpObj.sendmail(sender, receivers, message)
			smtpObj.sendmail('wangb@hadlinks.com',receivers,message.as_string())
			print ("success")
		else:
			smtpObj.quit()
	except	smtplib.SMTPException,e:
		print e		


def warn3_mail():
	mail_host="smtp.ym.163.com"
	mail_user="wangb@hadlinks.com"
	mail_pass="wb19911010"
#sender = 'from@runoob.com'
#sender= 'pop.ym.163.com'
#	receivers = ['yyy3988@qq.com']
	message = MIMEText('%s 负载过高 %s'%(ip,load),'plain','utf-8')
	message['From'] = Header("tech")
	message['To'] = Header("wangb")
	subject = '负载过高'
	message['subject']= Header(subject,'utf-8')
	try:
		smtpObj = smtplib.SMTP()
		smtpObj.connect(mail_host,25)	
		state=smtpObj.login(mail_user,mail_pass)
		if state[0] == 235:
#	smtpObj.sendmail(sender, receivers, message)
			smtpObj.sendmail('wangb@hadlinks.com',receivers,message.as_string())
			print ("success")
		else:
			smtpObj.quit()
	except	smtplib.SMTPException,e:
		print e		


def warn4_mail():
        mail_host="smtp.ym.163.com"
        mail_user="wangb@hadlinks.com"
        mail_pass="wb19911010"
#sender = 'from@runoob.com'
#sender= 'pop.ym.163.com'
#       receivers = ['yyy3988@qq.com']
        message = MIMEText('%s 磁盘使用率过高 %s'%(ip,dev),'plain','utf-8')
        message['From'] = Header("tech")
        message['To'] = Header("wangb")
        subject = '磁盘使用率过高'
        message['subject']= Header(subject,'utf-8')
        try:
                smtpObj = smtplib.SMTP()
                smtpObj.connect(mail_host,25)
                state=smtpObj.login(mail_user,mail_pass)
                if state[0] == 235:
#       smtpObj.sendmail(sender, receivers, message)
                        smtpObj.sendmail('wangb@hadlinks.com',receivers,message.as_string())
                        print ("success")
                else:
                        smtpObj.quit()
        except  smtplib.SMTPException,e:
                print e


def main():

	p1 = Process(target=cpu_stat)
	p2 = Process(target=hardware_stat)
	p3 = Process(target=free_stat)
	p4 = Process(target=load_stat)
	p5 = Process(target=disk_stat)

	p1.start()
	p2.start()
	p3.start()
	p4.start()
	p5.start()

	# threading.Thread(target=cpu_stat).start()
	# threading.Thread(target=hardware_stat).start()
	# threading.Thread(target=free_stat).start()
	# threading.Thread(target=load_stat).start()
	# threading.Thread(target=disk_stat).start()	
		
if __name__== "__main__":
	main()