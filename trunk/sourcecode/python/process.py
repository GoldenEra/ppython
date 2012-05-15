# -*- coding: UTF-8 -*-

import sys
import time
import threading
import socket
from types import *

REQUEST_MIN_LEN = 10    #合法的request消息包最小长度    
TIMEOUT = 180            #socket处理时间180秒


def z_encode(p):
    """
    encode param from python data
    """
    tp=type(p)
    print "返回类型:%s" % tp
    if p == None:                               #None->PHP中的NULL
        return "N;"
    elif tp==IntType:                           #int->PHP整形
        return "i:%d;"%p
    elif tp==StringType :                       #String->PHP字符串
        return 's:%d:"%s";' % (len(p),p)
    elif tp==BooleanType:                       #boolean->PHP布尔
        b=1 if p else 0
        return 'b:%d;'% b
    elif tp==FloatType:                         #float->PHP浮点
        return 'd:%r;'%p
    elif tp==ListType  or tp==TupleType:        #list,tuple->PHP数组(下标int)
        s=''
        for pos,i in enumerate(p):
            s+=z_encode(pos)
            s+=z_encode(i)
        return "a:%d:{%s}"%(len(p),s)
    elif tp==DictType:                          #字典->PHP数组(下标str)
        s=''
        for key in p:
            s+=z_encode(key)
            s+=z_encode(p[key])
        return "a:%d:{%s}"%(len(p),s)
    else:                                       #其余->PHP对象
        class_name = "_" + p.__class__.__name__                     #对象类名
        module_name = p.__class__.__module__.replace('.','_')       #对象类所在模块名
        attrs = p.__dict__                                          #对象属性字典
        s = ''
        for key in attrs:
            s += z_encode(key)
            s += z_encode(attrs[key])
        return "O:%s:%d:{%s}" % ((module_name+class_name), len(attrs), s)

def z_decode(p):
    """
    decode php param from string to python
    """
    if p[0]=='N' and p[1]==';':         #NULL
        return None,p[2:]
    elif p[0]=='b' and p[1]==':':       #布尔
        if p[2] == '0':
            return False,p[4:]
        else:
            return True,p[4:]
    elif p[0]=='i' and p[1]==':':       #整形
        i=p.find(';',1)
        return int(p[2:i]),p[i+1:]
    elif p[0]=='d' and p[1]==':':       #浮点
        i=p.find(';',1)
        return float(p[2:i]),p[i+1:]
    elif p[0]=='s' and p[1]==':':       #字符串
        i=p.find(':',2)
        len=int(p[2:i])
        k=i+1+len+2
        v=p[i+1:k]
        return v[1:-1],p[k+1:]
    elif p[0]=='a' and p[1]==':':       #list数组以及map
        d=[]
        dd={}
        flag=1
        i=p.find(':',2)
        n=int(p[2:i])
        pp=p[i+1+1:]
        for i in range(n):
            v1,pp=z_decode(pp)
            v2,pp=z_decode(pp)
            d.append(v2)
            dd[v1]=v2
            if v1 != i:
                flag=0
        if pp and pp[0]=='}':
            if pp[1:] and pp[1]==';':
                pp=pp[2:]
            else:
                pp=pp[1:]
        
        return (d,pp) if flag else (dd,pp)

    elif p[0]=='O' and p[1]==':':       #对象 TODO
        pass
    else:
        return p,''

def parse_php_req(p):
    """
    解析PHP请求消息
    返回：元组（模块名，函数名，入参list）
    """
    d=[]
    while p:
        v,p=z_decode(p)         #v：值  p：偏移指针
        d.append(v)

    modul_func = d[0]           #第一个元素是调用模块函数名
    pos = modul_func.find("::")
    modul = modul_func[:pos]    #模块名
    func = modul_func[pos+2:]   #函数名

    return modul, func, d[1:]   

def call_fun(fn):
    '''反射'''
    def _(*args, **kw):
        print "entering " + fn.__name__
        v = fn(*args, **kw)
        print "leaving " + fn.__name__
        return v
    return _

class ProcessThread(threading.Thread):
    """
    preThread 处理线程
    """
    def __init__(self, socket):
        threading.Thread.__init__(self)

        #客户socket
        self._socket = socket 

    def run(self):

        #---------------------------------------------------
        #    1.接收消息
        #  消息报文格式：
        #  示例： 60,s:25:"aaa.bbb.ccc.modul1::func1";a:1:{i:0;s:x:"login";}
        #  说明： 
        #   1）开始的60，标示逗号后的消息体长度
        #   2）第一个元素，表示要调用的Python函数，aaa.bbb.ccc.modul1包模块名，func1函数名
        #   3）从‘a’开始，是函数入参
        #   4）函数返回数据，要包装为PHP序列化字符串，通过Socket反给PHP
        #---------------------------------------------------
        
        try:  
            self._socket.settimeout(TIMEOUT)                  #设置socket超时时间
            firstbuf = self._socket.recv(16 * 1024)           #接收第一个消息包

            if len(firstbuf) < REQUEST_MIN_LEN:               #不够消息最小长度
                print "非法包，小于最小长度: %s" % firstbuf
                return

            firstComma = firstbuf.find(',')                   #查找第一个","分割符
            totalLen = int(firstbuf[0:firstComma], 10)        #消息包总长度(10进制)

            #构造请求消息包,从第一个冒号后读取直到消息结束    
            reqMsg = firstbuf[firstComma+1:]
            while (len(reqMsg) < totalLen):    
                reqMsg = reqMsg + self._socket.recv(16 * 1024)

            #调试
            print "请求包：%s" % reqMsg

        except Exception, e:  
            print '接收消息异常', e 
            self._socket.close()
            return

        #---------------------------------------------------
        #    2.请求消息包格式检查
        #---------------------------------------------------

        #从消息包中解析出模块名、函数名、入参list
        modul, func, params = parse_php_req(reqMsg) 

        #检查模块、函数是否存在
        try:
            callMod = __import__ (modul)    #根据module名，反射出module
            print '模块存在:%s' % modul
        except Exception, e:
            print '模块不存在:%s' % modul
            self._socket.sendall("F" + "module '%s' is not exist!" % modul) #异常
            self._socket.close()
            return

        try:
            callMethod = getattr(callMod, func)
            print '函数存在:%s' % func
        except Exception, e:
            print '函数不存在:%s' % func
            self._socket.sendall("F" + "function '%s()' is not exist!" % func) #异常
            self._socket.close()
            return

        #---------------------------------------------------
        #    3.Python函数调用
        #---------------------------------------------------

        try:  
            exec "import %s" % modul  #加载模块

            print "调用函数及参数1：%s(%s)" % (modul+'.'+func, params)
            #params = ','.join([repr(x) for x in params])    
            params = ','.join([repr(x) for x in params[0]])         
            print "调用函数及参数2：%s(%s)" % (modul+'.'+func, params)
            
            exec "ret=%s(%s)" % (modul+'.'+func, params)     #函数调用
        except Exception, e:  
            print '调用Python业务函数异常', e 
            self._socket.close()
            return

        #---------------------------------------------------
        #    4.结果返回给PHP
        #---------------------------------------------------
        retType = type(ret)
        print "函数返回：%s" % retType
        rspStr = z_encode(ret)  #函数结果组装为PHP序列化字符串

        try:  
            #加上成功前缀'S'
            rspStr = "S" + rspStr
            #调试
            print "返回包：%s" % rspStr
            self._socket.sendall(rspStr)
        except Exception, e:  
            print '发送消息异常', e 
            self._socket.sendall("F" + e) #异常信息返回
        finally:
            self._socket.close()
            return