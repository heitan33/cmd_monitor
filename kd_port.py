#coding = utf-8
# -*- coding: utf-8 -*-
import socket
import optparse
import re
import threading
import sys

def anlyze_host(target_host):
    try:
        pattern = re.compile(r'\d{1,3}\.\d{1,3}\.\d{1,3}\.\d{1,3}') 
        match = pattern.match(target_host)
        if match:
            return(match.group())
        else:
            try:
                target_host = socket.gethostbyname(target_host) 
                return(target_host)
            except Exception as err:
                print('地址解析错误：',err)
                exit(0)
    except Exception as err:
        print('请注意错误1：',sys.exc_info()[0],err)
        print(parser.usage)
        exit(0)
                    

def anlyze_port(target_port):
    try:
        pattern = re.compile(r'(\d+)-(\d+)')
        match = pattern.match(target_port)
        if match:
            start_port = int(match.group(1))
            end_port = int(match.group(2))
            return([x for x in range(start_port,end_port + 1)])
        else:
            return([int(x) for x in target_port.split(',')])
    except Exception as err:
        print('请注意错误2:',sys.exc_info()[0],err)
        print(parser.usage)
        exit(0)

def scanner(target_host,target_port):
#创建一个socket对象
    s = socket.socket(socket.AF_INET,socket.SOCK_STREAM)
    s.settimeout(5)
    try:
        s.connect((target_host,target_port))
        #s.sendall(b'hello\r\n\r\n')
        #message = s.recv(100)
        #if message:
        print('[+]%s的%3s端口:open!!\n' % (target_host,target_port)) 
           # print(' %s' % message.decode('utf-8'))
    except socket.timeout:
        print('[-]%s的%3s端口:close!!\n' % (target_host,target_port)) 
    except Exception as err:
        print('请注意错误3:',sys.exc_info()[0],err)
        exit(0)


        
def main():
   usage = 'Usage:%prog -h <host> -p <port>'
   parser = optparse.OptionParser(usage,version='%prog v1.0')
   parser.add_option('--host',dest='target_host',type='string',
                     help='需要扫描的主机,域名或IP')
   parser.add_option('--port',dest='target_port',type='string',
                    help='需要扫描的主机端口，支持1-100或21,53,80两种形式')
   (options,args) = parser.parse_args()
   if options.target_host == None or options.target_port == None:
      print(parser.usage)
      exit(0)
   else:
      target_host = options.target_host
      target_port = options.target_port

   target_host = anlyze_host(target_host)
   target_port = anlyze_port(target_port)

   for port in target_port:
      for i in range(5):
         t = threading.Thread(target=scanner,args=(target_host,port))
         t.start()

if __name__ == '__main__':
   main()  
