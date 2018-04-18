#encoding:utf8
import urllib2
import cookielib
import re

def getCookie():
    #创建一个MozillaCookieJar对象
    cookie = cookielib.MozillaCookieJar()
    #从文件中的读取cookie内容到变量
    cookie.load('cookie.txt',ignore_discard=True,ignore_expires=True)
    #打印cookie内容,证明获取cookie成功
    for item in cookie:
        print 'name:' + item.name + '-value:' + item.value
    #利用获取到的cookie创建一个opener
    handler = urllib2.HTTPCookieProcessor(cookie)
    opener = urllib2.build_opener(handler)
    res = opener.open('http://122.246.11.153:11380/sharegoTest/common/index.action')
    data = res.read()
    print data
    reg = r'href=(".+?")'
    imgre = re.compile(reg)
    imglist = re.findall(imgre,data)
    for imgurl in imglist:
        imgurl = imgurl.strip('"')
        imgurl = 'http://122.246.11.153:11380' + imgurl
        print imgurl
        res1 = opener.open(imgurl)
        data1 = res1.read()
        reg1 = r''+ str(imgurl) + ''
        # reg1 = re.compile(imgurl)
        dirs = reg1.findall(data1)
        if not dirs:
            print imgurl
        else:
            continue


    

def main():
    # Cookie()
    getCookie()

if __name__== "__main__":
    main()