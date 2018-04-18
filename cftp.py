#!/bin/python
import pexpect,sys,os
spam = {'10.168.168.85':'^hadLINKS99988$',}

def main():
	global k,v
	for k,v in spam.items():
		k=str(k)
		v=str(v)
		up()

file1=sys.argv[1]
file2=sys.argv[2]
os.environ['file1'] = str(file1)
os.environ['file2'] = str(file2)
#print file1,file2

def up():
	try:		
		child=pexpect.spawn("scp /root/%s root@%s:/root/html/cdn.yunext.com/%s/%s" %(file1,k,file2,file1))
		index=child.expect(['(?i)yes','(?i)[Pp]assword',pexpect.EOF,pexpect.TIMEOUT])
		if (index==0):
			child.sendline('yes')
			index1=child.expect(['(?i)[Pp]assword',pexpect.EOF,pexpect.TIMEOUT])
			if (index1==0):
				child.sendline('%s' %(v))  
				child.expect('#')
				child.close(force=True)			

			if (index==1):
				child.sendline('%s' %(v))	
				child.expect('#')
				child.close(force=True)
			
	except pexpect.exceptions.EOF,e:
		print e
    
def check():
	child=pexpect.spawn("ssh root@10.168.168.85")
	index=child.expect(['(?i)yes','(?i)[Pp]assword',pexpect.EOF,pexpect.TIMEOUT])
	if (index==0):
		child.sendline('yes')
		index1=child.expect(['(?i)[Pp]assword',pexpect.EOF,pexpect.TIMEOUT])
		try:
			if (index1==0):
				child.sendline('%s' %(v))
				child.expect('#')
				child.expect('mkdir /root/html/cdn.yunext.com/%s' %file1)
				child.expect('#')
				child.close(force=True)
				up()

			if (index==1):
				child.sendline('%s' %(v))
				child.expect('#')
				child.expect('mkdir /root/html/cdn.yunext.com/%s' %file1)
				child.expect('#')	
				child.close(force=True)
				up() 				

		except:
			up() 
		
				
def main():
	check()

if __name__== "__main__":
	main()
