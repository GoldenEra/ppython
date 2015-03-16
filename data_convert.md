# PHP-Python数据转换说明 #

本文通过程序样例来介绍PHP和Python之间的的数据怎样相互转换，可作为LAPP的使用规范文档。


## PHP序列化数据简介 ##

在PHP语言中，数据类型是隐匿的，并且是根据上下文而自动变化的，比如：

```
$a = 10;
$a = "a is " . $a;
```

在第一行中，$a是int类型，在第二行中$a变化为string类型。通常“弱”类型语言，像Javascript,VB,PHP等都是这样。PHP中提供了一些函数（is\_array()、is\_bool()、is\_float()、is\_integer()等）来获得变量的类型，更直接的方式是观察变量序列化后的排列规则:


---


### 整形 ###

```
$a = 10;
echo serialize($a);
```

输出：

```
i:10;
```

i表示int类型，10是其值。


---


### 字符串 ###

```
$a = "abcd";
echo serialize($a);
```

输出：

```
s:4:"abcd";
```

s表示string类型，4表示长度，"abcd"是其值。


---


### 布尔 ###

```
$a = TRUE;
echo serialize($a);
```

输出：

```
b:1;
```

b表示boolean类型，1表示TRUE，0表示FALSE。


---


### 浮点 ###

```
$a = 10.24;
echo serialize($a);
```

输出：

```
d:10.2400000000000002131628207280300557613372802734375;
```

d表示double类型，10.2400000000000002131628207280300557613372802734375是其值。


---


### 空（NULL） ###

```
$a = NULL;
echo serialize($a);
```

输出：

```
N;
```


---


### 数组 ###

```
$a = array();
$a[] = 20;
$a[] = "abcde";
$a[] = TRUE;

echo serialize($a);
```

输出：

```
a:3:{i:0;i:20;i:1;s:5:"abcde";i:2;b:1;}
```

开始的a表示array，紧跟着的3表示数组长度，{}内部是数组元素：
  * `i:0;i:20;`是第一个元素，i:0;是KEY（表示下标是int类型的0），i:20;是VALUE。
  * `i:1;s:5:"abcde";`是第二个元素，i:1;是KEY（表示下标是int类型的1），s:5:"abcde";是VALUE。
  * `i:2;b:1;`是第三个元素，i:2;是KEY（表示下标是int类型的2），b:1;是VALUE。

这种下标为自增int类型的数组，转换到Python的List类型。

```
$a = array();
$a["a"] = 20;
$a["b"] = "abcde";
$a["c"] = TRUE;

echo serialize($a);
```

输出：

```
a:3:{s:1:"a";i:20;s:1:"b";s:5:"abcde";s:1:"c";b:1;}
```

这里数组下标是字符串，数据结构可以看作是Python的字典类型，实际上也是按字典转换到Python的。


---


### 对象 ###

```
class aaa_bbb_ccc_user
{
    var $name = "zhangsan";
    var $age = 30;
}
$user = new aaa_bbb_ccc_user;

echo serialize($user);
```

输出：

```
O:16:"aaa_bbb_ccc_user":2:{s:4:"name";s:8:"zhangsan";s:3:"age";i:30;}
```

开始的O标示Object，16是对象类名"aaa\_bbb\_ccc\_user"的长度，接下来的2表示对象有2个属性：name属性（值为"zhangsan"），age属性（值为30）。

PHP4中没有命名空间，因此"aaa\_bbb\_ccc\_user"对应Python的 aaa.bbb.ccc.user 对象，$name和$age和Python对象的属性name和age对应。


---


## PHP Python 数据转换 ##

首先必须清楚，PHP数据类型和Python数据类型并非可以一一对应，因此数据转换需要做出必要的规定，比如在Python中有List、元组、字典等数据类型，而PHP相应的容器型数据类型只有数组，数据转换详细参看下面的表格：

**PHP数据转换到Python：**

| **PHP类型** | **Python类型** |
|:--------------|:-----------------|
|NULL|None|
|int|int|
|string|string|
|boolean|boolean|
|float|float|
|array(下标int)<sup>1</sup> |元组|
|array(下标string)<sup>2</sup> |字典|
|对象(PHP4)<sup>3</sup> |对象|

1) 当PHP数组第一个元素的下标是int类型0时，转换到Python的List

2) 当PHP数组第一个元素的下标非int类型0时，转换到Python的字典，下标字符串作为字典的key

3) 目前只支持PHP4对象的转换

**Python数据转换到PHP：**

| **Python类型** | **PHP类型** |
|:-----------------|:--------------|
|None|NULL|
|int|int|
|string|string|
|boolean|boolean|
|float|float|
|List<sup>1</sup> |array(下标int)|
|元组<sup>1</sup> |array(下标int)|
|字典<sup>2</sup> |array(下标string)|
|对象<sup>3</sup> |对象(PHP4)|

1) List和元组在转换到PHP的数组时，按顺序自动添加PHP数组下标，从0开始

2) 字典同样转换到PHP的数组，字典的key作为数组的下标

3) 对象的转换规则请看后面的文档