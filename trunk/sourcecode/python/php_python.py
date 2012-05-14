#!/usr/bin/env python
# -*- coding: UTF-8 -*-

import time
import socket

import process

HOST = ''				#所有
LISTEN_PORT = 21230		#服务侦听端口
CHARSET = "utf-8"		#设置字符集


if __name__ == '__main__':

    print "-------------------------------------------"
    print "- LAPP-JAVA (Socket) Service" 
    print "- Time: %s" % time.strftime('%Y-%m-%d %H:%M:%S',time.localtime(time.time())) 
    print "-------------------------------------------"

    sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)  #TCP/IP
    sock.bind((HOST, LISTEN_PORT))  
    sock.listen(5)  

    print "Listen port: %d" % LISTEN_PORT

    print "charset: %s" % CHARSET

    #自动程序运行

    print "Server startup..."

    while 1:  
        connection,address = sock.accept()  #收到一个请求

        print "client's IP:%s, PORT:%d" % address

        # 创建线程处理
        try:
            process.ProcessThread(connection).start()
        except:
            pass


