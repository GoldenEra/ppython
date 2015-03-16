# PHP-Python数据转换说明（二） #

这里的代码示例，讲述了PHP和Python之间各种数据类型的转换过程和细节。


## 基本数据类型 ##

基本数据类型有：int、string、float、boolean。


---


### int ###

PHP:
```
<?php header("Content-Type: text/html; charset=utf-8");
require_once('php_python.php');

$a = 20;
$b = 30;

$ret = ppython("testmod::add", 20, 30); //调用Python的add函数

echo "result:" . $ret; //这里会打印“result:50”
?> 
```

Python (文件testMod.py):
```
def add(x, y):
    return x + y
```

在这个例子中，Python提供了一个加法函数服务，PHP调用这个函数，传入参数，并得到返回值。


---


### string ###

PHP:
```
<?php header("Content-Type: text/html; charset=utf-8");
require_once('php_python.php');

$str = "Tom";

$ret = ppython("hello::echo", $str); 

echo $ret;  //打印 “Tom,你好”
?>
```

Python (文件hello.py):
```
# -*- coding: utf-8 -*-

def echo(name):
    return name + ",你好"
```

字符串传输，需要注意字符集，这里PHP和Python都采用utf-8，如果字符集不同，请参照配置文档。


---


### boolean ###

PHP:
```
<?php header("Content-Type: text/html; charset=utf-8");
require_once('php_python.php');

echo ppython("true_false::isTrue", False, True) ? "T" : "F"; //打印“T” 
echo "<br/>";
echo ppython("true_false::isTrue", False, False) ? "T" : "F"; //打印“F” 
?>
```

Python (文件true\_false.py):
```
def isTrue(a, b):
    return a or b
```

这里Python的isTrue函数进行“或”运算。


---


### float ###

PHP:
```
<?php header("Content-Type: text/html; charset=utf-8");
require_once('php_python.php');

$ret = ppython("float::ten", 9.9999999999999999);
echo $ret;
?>
```

Python (文件float.py):
```
def ten(d):
    return d * 10
```


---


## 容器型数据类型 ##

PHP的数组、对象，Python的List、元组、字典、对象，这些可以包容子元素的数据类型，这里称之为容器型数据类型。


---


### 数组 ###

#### 例1 ####

PHP:
```
<?php header("Content-Type: text/html; charset=utf-8");
require_once('php_python.php');

$a = array();
$a[0] = 10;
$a[1] = true;
$a[2] = "abcd";
$a[3] = 3.1415926;
$a[4] = NULL;

echo serialize($a);  //打印数组$a的序列化结构
$ret = ppython("arr::backorder", $a);
echo "<br/>";
echo serialize($ret); //打印python返回的数据的序列化结构
?>
```

Python (文件arr.py):
```
def backorder(arr):
    return arr[::-1]
```

backorder函数倒序arr数组，`[::-1]`是python的语法糖。

输出：
```
a:5:{i:0;i:10;i:1;b:1;i:2;s:4:"abcd";i:3;d:3.14159260000000006840537025709636509418487548828125;i:4;N;}
a:5:{i:0;N;i:1;d:3.14159260000000006840537025709636509418487548828125;i:2;s:4:"abcd";i:3;b:1;i:4;i:10;}
```

PHP数组可以模拟其他语言的List、Map、栈等，这里的映射规定：如果PHP数组第一个元素下标是int的0，转换为Python的元组(tuple)；反之，Python的List、元组转换到PHP数组时，按顺序添加数组下标，从0开始。

#### 例2 ####

PHP：
```
<?php header("Content-Type: text/html; charset=utf-8");
require_once('php_python.php');

$a = array();
$a['name'] = 'zhangsan';
$a['age'] = 30;

echo serialize($a);  //打印数组$a的序列化结构
$ret = ppython("arr::userinfo", $a);
echo "<br/>";
echo serialize($ret);  //打印python返回的数据的序列化结构
echo "<br/>";
echo $ret['id']; //打印 '0001'
?>
```

Python (文件arr.py):
```
def backorder(arr):
    return arr[::-1]

def userinfo(arr):
    arr['id'] = '0001'; #增加一个元素，key为'id'，值为'0001'
    return arr
```

arr.py中增加了一个函数userinfo.

输出：
```
a:2:{s:4:"name";s:8:"zhangsan";s:3:"age";i:30;}
a:3:{s:3:"age";i:30;s:4:"name";s:8:"zhangsan";s:2:"id";s:4:"0001";}
0001
```

PHP数组下标如果是字符串类型，转换到Python的字典类型，PHP数组元素下标为字典的key；反之，Python字典转换到PHP数组时，字典key作为PHP数组下标。


---
