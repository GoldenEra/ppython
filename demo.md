# 一个增删改查的简单WEB示例程序 #

这里展示了一个PHP+Python+Oracle的简单的示例程序。


## 数据库 ##

在Oracle中创建一张用户表，程序围绕着这张表进行增删改查操作：
```
create table users(
  id varchar(40)       not null, --用户ID
  userName varchar(20) not null, --用户姓名
  age int              not null, --年龄
  sex char(1)          not null, --1:男 0:女
  tel varchar(21),               --电话
  constraint PK_USERS primary key (ID)
);
```

## Python + Oracle 的环境配置 ##

Python+Oracle的环境配置请参考这篇文章：http://programmerdigest.cn/2012/03/1190.html

_注意：Demo程序要求Python3，请按Python3+Oracle环境要求配置。_

## PHP 的环境配置 ##

互联网上有非常多的关于Apache+PHP的配置文章，因此这里不再重复提供。

对于PHP的配置一般来说只有一个要求：需要支持socket。可以通过phpinfo()输出来检查是否符合要求，“Sockets Support”显示“enabled”即可。

## Python 程序 ##

业务程序 demo1.py
```
# -*- coding: utf-8 -*-

import uuid
import php_python

def addUser(userName, age, sex, tel):
    """增加用户，返回主键uuid"""
    myuuid = str(uuid.uuid1())  #生成主键uuid
    try:
        conn = php_python.getConn()
        cursor = conn.cursor()
        cursor.execute("insert into users(id,userName,age,sex,tel)values(:id,:userName,:age,:sex,:tel)",
        {
            'id': myuuid,
            'userName': userName,
            'age': age,
            'sex': sex,
            'tel': tel,
        })
        conn.commit()
        print ("增加用户成功")
    except Exception as e:
        print ('增加用户异常', e)
    finally:
        php_python.closeConn(conn)
    
    return myuuid
    
def delUser(id_):
    """删除用户-业务函数"""
    try:
        conn = php_python.getConn()
        cursor = conn.cursor()
        cursor.execute("delete from users where id=:1", (id_,))
        conn.commit()
        print ("删除用户成功,ID:%s" % id_)
    except Exception as e:
        print ('删除用户异常', e)
    finally:
        php_python.closeConn(conn)

def changeUser(id_, userName, age, sex, tel):
    """修改用户资料"""
    try:
        conn = php_python.getConn()
        cursor = conn.cursor()
        cursor.execute("update users set userName=:userName,age=:age,sex=:sex,tel=:tel where id=:id",
        {
            'id': id_,
            'userName': userName,
            'age': age,
            'sex': sex,
            'tel': tel,
        })
        conn.commit()    
        print ("修改用户成功,ID:%s" % id_)
    except Exception as e:
        print ('修改用户异常', e)
    finally:
        php_python.closeConn(conn)

def userList():
    """用户列表"""
    retList = [] #返回列表
    try:
        conn = php_python.getConn()
        cursor = conn.cursor()
        cursor.execute("select id,userName,age,sex,tel from users")
        res = cursor.fetchall()
        for row in res:
            line = {}
            line['id'] = row[0]
            line['userName'] = row[1]
            line['age'] = row[2]
            line['sex'] = "男" if row[3] == '1' else "女"
            line['tel'] = row[4]
            retList.append(line)
        print ("用户列表成功")
        return retList
    except Exception as e:
        print ('用户列表异常', e)
        return []
    finally:
        php_python.closeConn(conn)
```

ppython框架文件 php\_python.py：
请在这里下载 http://code.google.com/p/ppython/source/browse/trunk/sourcecode/python/php_python.py

ppython框架文件 process.py：
请在这里下载 http://code.google.com/p/ppython/source/browse/trunk/sourcecode/python/process.py

## PHP 程序 ##

增加用户(增) demo\_add.php
```
<?php header("Content-Type: text/html; charset=utf-8");
require_once('php_python.php');

$id = ppython("demo1::addUser","张三",30,"1","13912345679");
echo "增减的用户ID：".$id;
?>
```

删除用户(删) demo\_del.php
```
<?php header("Content-Type: text/html; charset=utf-8");
require_once('php_python.php');

ppython("demo1::delUser","7171f41e-b148-11e1-b4ca-60d819d051d0"); #根据用户ID删除用户
echo "del OK";
?>
```

修改用户(改) demo\_change.php
```
<?php header("Content-Type: text/html; charset=utf-8");
require_once('php_python.php');

$id = ppython("demo1::changeUser","7171f41e-b148-11e1-b4ca-60d819d051d0","李四",35,"1","13912345677");

echo "change OK";
?>
```

用户列表(查) demo\_list.php
```
<?php header("Content-Type: text/html; charset=utf-8");
require_once('php_python.php');

$list = ppython("demo1::userList");
?>

<html>
<body>
  <table border="1">
  <caption>用户列表</caption>
  <?php foreach($list as $row){?>
    <tr>
        <td><?php echo $row['id']?></td>
        <td><?php echo $row['userName']?></td>
        <td><?php echo $row['age']?></td>
        <td><?php echo $row['sex']?></td>
        <td><?php echo $row['tel']?></td>
    </tr>
  <?php } ?>
  </table>
</body>
</html>
```

ppython框架文件 php\_python.php：
请在这里下载 http://code.google.com/p/ppython/source/browse/trunk/sourcecode/php/php_python.php

## 运行测试程序 ##

1. 将php\_python.py, process.py, demo1.py 三个文件复制到单独的目录，修改php\_python.py文件权限可执行，启动python服务：
```
$ ./php_python.py
```

2. 将php\_python.php, demo\_add.php, demo\_del.php, demo\_change.php, demo\_list.php 五个文件复制到Apache发布目录。

3. 浏览器访问demo\_add.php, demo\_del.php, demo\_change.php, demo\_list.php地址，测试demo程序。