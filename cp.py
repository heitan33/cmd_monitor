import os,sys,commands,subprocess,time

def cpu_top():
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
#        print(a)

        t=a[0].split(' ')[0]
        os.environ['t'] = str(t)
        pid=commands.getoutput("ps -ef|grep $t|grep -v grep")
        os.environ['pid'] = str(pid)
        #print(pid)
        time.sleep(1)
        m=a[0].split(' ')[1]
        os.environ['m'] = str(m)
        #print m
        commands.getoutput('date>>/home/ec2-user/nohup.out')
        commands.getoutput('echo "$pid">>/home/ec2-user/nohup.out')
        commands.getoutput('echo "$m%">>/home/ec2-user/nohup.out')
        commands.getoutput('echo "\n">>/home/ec2-user/nohup.out')

cpu_top()























































