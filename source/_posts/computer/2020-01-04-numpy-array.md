---
layout: post
title:  "Numpy Array"
date:   2020-01-04 08:00:00 +0800
categories: computer
tag: [computer]
---

numpy 一维数组与 python 列表类似，略。本文主要讨论多维数组的处理。

<!-- more -->

### 索引

```python
In [1]: from numpy import *

In [2]: a = arange(12).reshape(3,2,2)

In [3]: a
Out[3]:
array([[[ 0,  1],
        [ 2,  3]],

       [[ 4,  5],
        [ 6,  7]],

       [[ 8,  9],
        [10, 11]]])

```

此时，np 数组与 python list 的区别如下：

```python
    In [5]: a[0][1][1] == a[0, 1, 1]
    Out[5]: True
```

这两种语法是等价的，但是 python list 是不支持后一种的。

### 切片

以下是对比，注意 shape 的变化：

```python
In [9]: a[0:3][1]
Out[9]:
array([[4, 5],
       [6, 7]])

In [13]: a[0:3][1].shape
Out[13]: (2, 2) # 先沿着0轴切片，后索引

In [10]: a[0:3, 1]
Out[10]:
array([[ 2,  3],
       [ 6,  7],
       [10, 11]])

In [14]: a[0:3, 1].shape
Out[14]: (3, 2) # 原本的1轴被消除了

In [11]: a[0:3, 1:]
Out[11]:
array([[[ 2,  3]],

       [[ 6,  7]],

       [[10, 11]]])

In [15]: a[0:3,1:].shape
Out[15]: (3, 1, 2) # 切片保留所有轴
```

### 组合&分割

```python
In [7]: b = arange(12, 24).reshape(3,2,2)

In [8]: b
Out[8]:
array([[[12, 13],
        [14, 15]],

       [[16, 17],
        [18, 19]],

       [[20, 21],
        [22, 23]]])

```
两个主要函数：stack 以及 concatenate。

stack 用于堆叠

```python
In [33]: stack((a, b))
Out[33]:
array([[[[ 0,  1],
         [ 2,  3]],

        [[ 4,  5],
         [ 6,  7]],

        [[ 8,  9],
         [10, 11]]],


       [[[12, 13],
         [14, 15]],

        [[16, 17],
         [18, 19]],

        [[20, 21],
         [22, 23]]]])

In [34]: stack((a, b)).shape
Out[34]: (2, 3, 2, 2) # 默认沿着 axis = 0 堆叠

In [40]: stack((a, b), axis=1)
Out[40]:
array([[[[ 0,  1],
         [ 2,  3]],

        [[12, 13],
         [14, 15]]],


       [[[ 4,  5],
         [ 6,  7]],

        [[16, 17],
         [18, 19]]],


       [[[ 8,  9],
         [10, 11]],

        [[20, 21],
         [22, 23]]]])

In [37]: stack((a, b), axis=1).shape
Out[37]: (3, 2, 2, 2) # 沿着 axis = 1 堆叠
```

concatenate 用于连接

```python
In [46]: concatenate((a,b))
Out[46]:
array([[[ 0,  1],
        [ 2,  3]],

       [[ 4,  5],
        [ 6,  7]],

       [[ 8,  9],
        [10, 11]],

       [[12, 13],
        [14, 15]],

       [[16, 17],
        [18, 19]],

       [[20, 21],
        [22, 23]]])

In [53]: a.shape
Out[53]: (3, 2, 2)

In [54]: b.shape
Out[54]: (3, 2, 2)

In [47]: concatenate((a,b)).shape
Out[47]: (6, 2, 2)

In [48]: concatenate((a,b), axis=1)
Out[48]:
array([[[ 0,  1],
        [ 2,  3],
        [12, 13],
        [14, 15]],

       [[ 4,  5],
        [ 6,  7],
        [16, 17],
        [18, 19]],

       [[ 8,  9],
        [10, 11],
        [20, 21],
        [22, 23]]])

In [53]: a.shape
Out[53]: (3, 2, 2)

In [54]: b.shape
Out[54]: (3, 2, 2)

In [49]: concatenate((a,b), axis=1).shape
Out[49]: (3, 4, 2)
```
连接与堆叠的区别简单理解就是：连接增加了形状，堆叠增加了维度。

```python
In [55]: concatenate((a,b), axis=3)
---------------------------------------------------------------------------
AxisError                                 Traceback (most recent call last)
<ipython-input-55-ec2463892184> in <module>
----> 1 concatenate((a,b), axis=3)

AxisError: axis 3 is out of bounds for array of dimension 3
```

可以看到，axis=3 不存在，因此 concatenate 会包报错，所以，可以增加一个维度，再进行 concatenate 操作：

```python
In [57]: concatenate((a[...,newaxis],b[...,newaxis]), axis=3)
Out[57]:
array([[[[ 0, 12],
         [ 1, 13]],

        [[ 2, 14],
         [ 3, 15]]],


       [[[ 4, 16],
         [ 5, 17]],

        [[ 6, 18],
         [ 7, 19]]],


       [[[ 8, 20],
         [ 9, 21]],

        [[10, 22],
         [11, 23]]]])

In [58]: concatenate((a[...,newaxis],b[...,newaxis]), axis=3).shape
Out[58]: (3, 2, 2, 2)
```
concatenate 有几个快捷方法:

```python
    vstack(tup) : concatenate(tup, axis = 0)
    hstack(tup) : concatenate(tup, axis = 1)
    dstack(tup) : concatenate(tup, axis = 2)
```

如果 tup 中数组维度不够，则 hstack 或者 dstack 会自动增加维度。

分割就是 concatenate 的逆操作

    split  <——> concatenate

split 同样有几个快捷函数：

    vsplit(ary, indices_or_sections) : split(ary, indices_or_sections, axis=0)
    hsplit(ary, indices_or_sections) : split(ary, indices_or_sections, axis=1)
    dsplit(ary, indices_or_sections) : split(ary, indices_or_sections, axis=2)
