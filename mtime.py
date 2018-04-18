# -*- coding: utf-8 -*-
import urllib,urllib2,re

x=0
url='http://movie.mtime.com/'
user_agent = 'Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/61.0.3163.91 Safari/537.36'
values = {}
data = urllib.urlencode(values)
headers = { 'User-Agent' : user_agent }
request = urllib2.Request(url,headers)
page = urllib2.urlopen(request)
html = page.read()
html = html.decode('utf-8')

reg = re.compile('http://movie.mtime.com/.+?/')
data = re.findall(reg,html)

# reg2 = re.compile('<h2>.+?</h2>')
# title = re.findall(reg2,html)
# for title_1 in title:
# 	print title_1

try:
	for data_1 in data:
		#print data_1
	 	request = urllib2.Request(data_1)
	 	page_1 = urllib2.urlopen(request)
	 	page_1 = page_1.read()
	 	page_1 = page_1.decode('utf-8').encode('gbk','ignore')
	# 	# print page_1
	 	reg1 = re.compile('"imageUrl":"(http://.+?.jpg)"|src="(http://.+?.jpg)"')
	# 	reg2 = re.compile('src="(http://.+?.jpg)"')
	 	text = re.findall(reg1,page_1)
	# 	text2 = re.findall(reg2,page_1)
	 	# print text
		for imgurl in text:
			imgurl = list(imgurl)
			for imgurl_1 in imgurl:
				if imgurl_1 == '':
					continue
				else:
					urllib.urlretrieve(imgurl_1,'Q:\\ceshi\\%s.jpg' % x)
					x+=1
					print imgurl_1
	
	# 	for text_1 in text:
	# 		with open('Q:/dmbj.txt','a+') as f:
	# 			# f.write(title_1)
	# 			# f.write('\n')
	# 			f.write(text_1)
	# 			f.write('\n')

# except urllib2.HTTPError,e:
# 	print e

# except IOError,e:
# 	print e

except Exception as e:
	print e