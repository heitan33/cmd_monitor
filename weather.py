import urllib, urllib2, sys,os
import ssl


host = 'https://ali-weather.showapi.com'
path = '/spot-to-weather'
method = 'GET'
appcode = 'f847be8a3fd44c4b981cd0c950e9ed88'
querys = 'area=%E5%AE%81%E6%B3%A2&need3HourForcast=0&needAlarm=0&needHourData=0&needIndex=0&needMoreDay=0'
bodys = {}
url = host + path + '?' + querys

request = urllib2.Request(url)
request.add_header('Authorization', 'APPCODE ' + appcode)
ctx = ssl.create_default_context()
ctx.check_hostname = False
ctx.verify_mode = ssl.CERT_NONE
response = urllib2.urlopen(request, context=ctx)
content = response.read()
content = content.decode('utf-8').encode('gbk') 
if (content):
	print(content)
