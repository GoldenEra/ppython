### 简介 ###
> 许多人在纠结WEB快速开发究竟是采用PHP，还是采用Python，二者同样是脚本语言，但特点鲜明：

  * **PHP**: Web专用开发利器，有10多年的经验积累，但其他领域基本不涉及，扩展性不强，企业应用少。
  * **Python**: 近期的明星语言，面向对象、简单高效、可扩展性强，但Web开发积累少，成熟度低。

> ppython开源项目既是结合使用PHP和Python两种语言，取其所长、补其所短，面向企业WEB领域的开发技术。此技术可以理解为PHP和Python相结合的技术，也可称为PHP和Python混合编程技术，或者PHP调用Python服务的技术，也有人习惯称之为前台PHP后台Python的技术框架。

> 本项目是LAJP项目的语言环境的拓展，变化是将LAJP中的Java语言变更为Python语言，因此LAJP的技术、文档对本项目有参考作用。LAJP的官方网页：http://code.google.com/p/lajp

### 特点 ###
  * **优势互补**: PHP和Python都是流行的脚本语言，PHP非常适合网页编程；而Python可以当作轻量级JAVA，二者结合可发挥各自优势。
  * **高效稳定**：Apache+PHP组合可带来优异的WEB服务稳定性，而Python的语言能力可补充如连接池、事物管理、分布式、对象模型等高端特性。
  * **通信机制** PHP和Python间的通讯方式采用TCP Socket和Unix Socket两种机制，兼顾通讯效率和分布式。
  * **数据类型自动转换机制** PHP数据和Python数据可准确地自动匹配和转换，无须程序员编写解析代码。
  * **易用**：安装配置简单，PHP端和Python端编程符合各自的编程习惯。
  * **轻量级**：架构非常轻量级，除了最基本的PHP和Python环境，不需要任何扩充的、第三方的组件、容器。

### PHP和Python的互通 ###

![http://ppython.googlecode.com/svn/wiki/images/ppythonmode.png](http://ppython.googlecode.com/svn/wiki/images/ppythonmode.png)

PHP和Python是两种不同的语言，通讯中采用两种socket机制。

  * **一、TCP Socket**

传统的TCP/IP通讯。

  * **二、UNIX Domain Socket**

Unix/Linux本地socket，相对于TCP Socket，有以下特点：

  1. 只能在同一台主机中通讯（IPC），不能跨网络
  1. 传输速度，大于TCP Socket
  1. 服务端只向本机提供服务(没有对外侦听端口)，相对安全，易于管理。

### 数据类型转换 ###

PHP和Python各有其语言内部定义的数据类型，当PHP数据传送到Python，或Python数据传送到PHP时，传统上需要转码处理，而使用本技术程序员无需进行任何的此类工作。

![http://ppython.googlecode.com/svn/wiki/images/type_convert.png](http://ppython.googlecode.com/svn/wiki/images/type_convert.png)

详细内容请浏览wiki文档：http://code.google.com/p/ppython/w/list

### 提高Python的多线程效率 ###

Python因其语言GIL特性，多线程效率不高。在PHP+Python的混搭机制中，Python端可以多进程方式部署，从而提高Python的整体工作效率。

### 示例 ###

示例程序表现了一个简单的PHP页面调用Python的加法函数程序片段。

  * **php端程序**

```
<?php
  require_once("php_python.php"); //框架提供的程序脚本

  $p1 = 2;     
  $p2 = 3; 

  //"ppython"是框架"php_python.php"提供的函数，用来调用Python端服务
  //调用Python的testModule模块的add函数，并传递2个参数。
  $ret = ppython("testModule::add", $p1, $p2);

  echo "返回信息：".$ret;    //打印 5
?>
```

  * **Python端程序，文件名testModule.py**

```
# -*- coding: UTF-8 -*-

def add(a, b):
  return a + b
```