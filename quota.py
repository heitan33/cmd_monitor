import os,re,sys,stat

def lock():
	for a,b,c in os.walk('/root/server'):
		path = a
		regex = re.compile('.*/logs')
		dirs = regex.findall(path)
		for dir in dirs:
			dir = ''.join(dir)
			os.environ['dir'] = str(dir)
			print dir
			os.system("chmod -R 444 $dir")

lock()
