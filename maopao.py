import os,sys,commands

a=commands.getoutput("top -b n1|awk '{print $1,$9}'|sed '1,7d'")
a=a.split('\n')
i=0
j=1

for i in range(len(a)):
	for j in range(len(a)):
		if str(a[i]).split(' ')[1] < str(a[j]).split(' ')[1]:
			pass	
		else:
			a[i],a[j]=a[j],a[i]

t=a[0].split(' ')[0]
os.environ['t'] = str(t)
pid=commands.getoutput('ps -ef|grep $t|grep -v grep')
print pid
m=a[0].split(' ')[1]
print m
