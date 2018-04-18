# -*- coding: utf-8 -*-
import smtplib,commands,time,subprocess
from email.mime.text import MIMEText
from email.header import Header
import os
import threading
import cp

c=commands.getoutput("grep 'model name' /proc/cpuinfo | wc -l")

global receivers,z,ip,mail_user,mail_pass
receivers = ['yyy3988@qq.com']
mail_user = "yyy3988@qq.com"
mail_pass = "uahaibjiqzelbjih"
mail_host = "smtp.qq.com"
ip = 'test-131'
# output = subprocess.Popen('curl ifconfig.me',stdout=subprocess.PIPE,stderr=subprocess.PIPE,shell=True)
# output.wait()
# ip=output.stdout.read()
# print(ip)

zoo = subprocess.Popen('ls zookeeper*',stdout=subprocess.PIPE,stderr=subprocess.PIPE,shell=True)
zoo.wait()
z = zoo.stdout.read()
print(z)


def cpu_stat():
	global i,cpu
	i=0
	while True:
		cpu=commands.getoutput("sar -u 1 1|sed -n '4p'|awk '{print $NF}'")
		cpu = 100 - float(cpu)
		time.sleep(10)
		if float(cpu) > 70:
#			print ("......")
			i=i+1
	#		print(i)
			if(i==3):
				cp.cpu_top()
				print("WARNING-cpu")
				warn_mail()
				r1=0
				while i==3:
					cpu=commands.getoutput("sar -u 1 1|sed -n '4p'|awk '{print $NF}'")
					time.sleep(10)
					if float(cpu) <= 70:
						r1=r1+1
						if r1==3:
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


def disk_stat():
	global disk
	while True:
		try:
			disk=commands.getoutput("df -h|awk '{print $5}'|sed '1d'|xargs")
			list1 = disk.split(" ")
			time.sleep(10)
			for dev in list1:
				newint = int(dev.strip("%"))
				if newint >= 90:
					warn1_mail()
					while True:
						judge=1
						disk2 = commands.getoutput("df -h|awk '{print $5}'|sed '1d'|xargs")
						list2 = disk2.split(" ")
						for dev2 in list2:
							newint2 = int(dev2.strip("%"))
							if newint2 < 90:
								pass
							else:	
								judge=0
								break

						if judge==1:
							break
						else:
							pass

					recovery1_mail()
					break
				else:
					pass
		except:
			continue
		

def free_stat():
	global fe,buff
	fe=0
	while True:
		buff=commands.getoutput("free -m|sed '1d'|grep buffers|awk '{print $4}'")	
		if buff == '':
			buff=commands.getoutput("free -m|sed -n '2p'|awk '{print $NF}'")
		time.sleep(10)
		if float(buff) <= 1500:
	#		print ("......")
			fe=fe+1
	#		print(fe)
			if(fe==3):
				print("WARNING-memory")
				warn2_mail()
				ff=0
				while fe==3:
					buff=commands.getoutput("free -m|sed '1d'|grep buffers|awk '{print $4}'")	
					if buff == '':
						buff=commands.getoutput("free -m|sed -n '2p'|awk '{print $NF}'")
					else:
						pass

					time.sleep(10)
					if  float(buff) > 1500:
						ff=ff+1
						if ff==3:
							time.sleep(30)
							recovery2_mail()
							fe=0
							break
	
						else:
							continue

					else:
						continue
			else:
				pass	
		else:	
			fe=0


def load_stat():
	global load,lo
	lo=0
	while True:
		try:
			load=commands.getoutput("uptime|awk -F, '{print $(NF-1)}'")
			time.sleep(10)
			if float(load) >= float(c):
				lo=lo+1
				if lo==3:
					print("WARNING-Loaded")
					warn3_mail() 
					r3=0
					while lo == 3:
						load=commands.getoutput("uptime|awk -F, '{print $(NF-1)}'")
						time.sleep(10)
						if float(load) < float(c):
							r3=r3+1
							if r3==3:
								time.sleep(10)
								recovery3_mail()
								lo=0
							else:
								continue	

						else:
							continue
				else:
					continue	
		except:	
			continue


def recovery_mail():
	message = MIMEText('%s CPU使用率恢复正常 %s'%(ip,cpu),'plain','utf-8')
	message['From'] = Header("tech")
	message['To'] = Header("wangb")
	subject = 'CPU使用率恢复正常'
	message['subject']= Header(subject,'utf-8')
	try:
		smtpObj = smtplib.SMTP()
		smtpObj.connect(mail_host,25)	
		state=smtpObj.login(mail_user,mail_pass)
		if state[0] == 235:
			smtpObj.sendmail(mail_user,receivers,message.as_string())
			print ("success")
		else:
			smtpObj.quit()
	except	smtplib.SMTPException,e:
		print e


def recovery1_mail():
	message = MIMEText('%s 硬盘恢复正常'%(ip),'plain','utf-8')
	message['From'] = Header("tech")
	message['To'] = Header("wangb")
	subject = '硬盘恢复正常'
	message['subject']= Header(subject,'utf-8')
	try:
		smtpObj = smtplib.SMTP()
		smtpObj.connect(mail_host,25)	
		state=smtpObj.login(mail_user,mail_pass)
		if state[0] == 235:
			smtpObj.sendmail(mail_user,receivers,message.as_string())
			print ("success")
		else:
			smtpObj.quit()
	except	smtplib.SMTPException,e:
		print e


def recovery2_mail():
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
			smtpObj.sendmail(mail_user,receivers,message.as_string())
			print ("success")
		else:
			smtpObj.quit()
	except	smtplib.SMTPException,e:
		print e


def recovery3_mail():
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
			smtpObj.sendmail(mail_user,receivers,message.as_string())
			print ("success")
		else:
			smtpObj.quit()
	except	smtplib.SMTPException,e:
		print e


def warn_mail():
	message = MIMEText('%s CPU使用率过高 %s'%(ip,cpu),'plain','utf-8')
	message['From'] = Header("tech")
	message['To'] = Header("wangb")
	subject = 'CPU使用率过高'
	message['subject']= Header(subject,'utf-8')
	try:
		smtpObj = smtplib.SMTP()
		smtpObj.connect(mail_host,25)	
		state=smtpObj.login(mail_user,mail_pass)
		if state[0] == 235:
			smtpObj.sendmail(mail_user,receivers,message.as_string())
			print ("success")
		else:
			smtpObj.quit()
	except	smtplib.SMTPException,e:
		print e


def warn1_mail():
	message = MIMEText('%s 磁盘用量过高,超过百分之90'%(ip),'plain','utf-8')
	message['From'] = Header("tech")
	message['To'] = Header("wangb")
	subject = '磁盘用量过高'
	message['subject']= Header(subject,'utf-8')
	try:
		smtpObj = smtplib.SMTP()
		smtpObj.connect(mail_host,25)	
		state=smtpObj.login(mail_user,mail_pass)
		if state[0] == 235:
			smtpObj.sendmail(mail_user,receivers,message.as_string())
			print ("success")
		else:
			smtpObj.quit()
	except	smtplib.SMTPException,e:
		print e		


def warn2_mail():
	message = MIMEText('%s 内存使用率过高 %s '%(ip,buff),'plain','utf-8')
	message['From'] = Header("tech")
	message['To'] = Header("wangb")
	subject = '内存使用率过高'
	message['subject']= Header(subject,'utf-8')
	try:
		smtpObj = smtplib.SMTP()
		smtpObj.connect(mail_host,25)
		state = smtpObj.login(mail_user,mail_pass)
		if state[0] == 235:
			smtpObj.sendmail(mail_user,receivers,message.as_string())
			print ("success")
		else:
			smtpObj.quit()
	except	smtplib.SMTPException,e:
		print e		


def warn3_mail():
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
			smtpObj.sendmail(mail_user,receivers,message.as_string())
			print ("success")
		else:
			smtpObj.quit()
	except	smtplib.SMTPException,e:
		print e		


def zookeeper():
	if z != "":	
		while True:
			port = commands.getoutput("netstat -ntulp|grep '2181'")
			if 'LISTEN' not in port:
				warn5_mail()
	#			print("email")
				while True:
					port = commands.getoutput("netstat -ntulp|grep '2181'")
					time.sleep(10)
					if 'LISTEN' not in port:
						continue
					else:
						recovery5_mail()
						break
			else:
				time.sleep(10)
				continue
	else:
		pass


def warn5_mail():
	message = MIMEText('%s zookeeper服务停止'%ip,'plain','utf-8')
	message['From'] = Header("tech")
	message['To'] = Header("wangb")
	subject = '2181端口没有监听'
	message['subject']= Header(subject,'utf-8')
	try:
		smtpObj = smtplib.SMTP()
		smtpObj.connect(mail_host,25)	
		state=smtpObj.login(mail_user,mail_pass)
		if state[0] == 235:
			smtpObj.sendmail(mail_user,receivers,message.as_string())
			print ("success")
		else:
			smtpObj.quit()
	except	smtplib.SMTPException,e:
		print e


def recovery5_mail():
	message = MIMEText('%s 2181端口正常'%ip,'plain','utf-8')
	message['From'] = Header("tech")
	message['To'] = Header("wangb")
	subject = '2181端口已正常监听'
	message['subject']= Header(subject,'utf-8')
	try:
		smtpObj = smtplib.SMTP()
		smtpObj.connect(mail_host,25)	
		state=smtpObj.login(mail_user,mail_pass)
		if state[0] == 235:
			smtpObj.sendmail(mail_user,receivers,message.as_string())
			print ("success")
		else:
			smtpObj.quit()
	except	smtplib.SMTPException,e:
		print e	


def up_down():	
	global v1,v2,ym
	ym=0
	while True:
		try:
			v1=commands.getoutput("sar -n DEV 1 1 |grep -i eth1 |sed -n '1p'|awk '{print $6}'")
			v2=commands.getoutput("sar -n DEV 1 1 |grep -i eth1 |sed -n '1p'|awk '{print $7}'")
			time.sleep(10)
			if float(v1) >= 2000 or float(v2) >= 2000:
				ym=ym+1
				if ym==5:
					print("WARNING-Loaded")
					warn6_mail() 
					while ym == 5:
	#					os.system('sh /root/bash/deny.sh')
						v1=commands.getoutput("sar -n DEV 1 1 |grep -i eth1 |sed -n '1p'|awk '{print $6}'")
						v2=commands.getoutput("sar -n DEV 1 1 |grep -i eth1 |sed -n '1p'|awk '{print $7}'")
						time.sleep(10)
						if float(v1) < 2000 and float(v2) < 2000:
							time.sleep(10)
							recovery6_mail()
							ym=0
						else:
							continue
				else:
					pass
			else:
				ym = 0

		except:
			continue


def warn6_mail():
	message = MIMEText('%s 入网速率过高'%ip,'plain','utf-8')
	message['From'] = Header("tech")
        message['To'] = Header("wangb")
      	subject = '服务器上行或下行速率过高'
       	message['subject']= Header(subject,'utf-8')
        try:
                smtpObj = smtplib.SMTP()
                smtpObj.connect(mail_host,25)
                state=smtpObj.login(mail_user,mail_pass)
                if state[0] == 235:
                        smtpObj.sendmail(mail_user,receivers,message.as_string())
                        print ("success")
                else:
                        smtpObj.quit()
        except  smtplib.SMTPException,e:
                print e


def recovery6_mail():
        message = MIMEText('%s 入网速率恢复正常'%ip,'plain','utf-8')
        message['From'] = Header("tech")
        message['To'] = Header("wangb")
        subject = '服务器上行或下行速率恢复正常'
        message['subject']= Header(subject,'utf-8')
        try:
                smtpObj = smtplib.SMTP()
                smtpObj.connect(mail_host,25)
                state=smtpObj.login(mail_user,mail_pass)
                if state[0] == 235:
                        smtpObj.sendmail(mail_user,receivers,message.as_string())
                        print ("success")
                else:
                        smtpObj.quit()
        except  smtplib.SMTPException,e:
                print e


def main():
	threading.Thread(target=cpu_stat).start()
	threading.Thread(target=free_stat).start()
	threading.Thread(target=load_stat).start()
	threading.Thread(target=disk_stat).start()	
	threading.Thread(target=zookeeper).start()
	threading.Thread(target=up_down).start()


if __name__== "__main__":
	main()
