---
layout: post
title:  "Numpy Broadcasting 机制"
date:   2020-03-04 08:00:00 +0800
categories: computer
tag: [computer]
---

首先需要明确的是，ndarray 在执行 element-wise （比如四则运算）的时候才会进行广播（Broadcasting），而 numpy 中 element-wise 的要求是 shape (形状)匹配，即

    narrayA.shape == narrayB.shape 为 True

换句话说就是执行运算的 ndarray 轴数（维度）相同，并且每个轴的长度相等。

Broadcasting 的逻辑流程：

1. 如果两个 ndarray 的轴数目不同，则将轴数较小的数组扩展到与轴数较大数组的轴数一致。即扩展 shape 的长度，扩展方式是通过在 shape 左端补 1 直到维度相等。
2. 从最后一根轴开始，依次比较每根轴的长度。
（1）如果当前轴的长度不相等，并且其中较短轴的长度等于 1，则将此轴的长度扩展至与较长轴的长度一致，并用此轴上的第一组数据填充扩展出来的其他部分。
（2）如果其中较短轴的长度不等于 1，则抛出错误。

以上是运算逻辑，并不代表 Numpy 在执行过程中进行了实际的内存分配。

一个例子：

```python
import numpy as np

a = np.arange(4).reshape((4,1))
b = np.arange(4)
a + b
```

a:

    array([[0],
          [1],
          [2],
          [3]])

b:

    array([0, 1, 2, 3])

此时，a.shape 为 (4,1)，b.shape 为 (4,)，很明显 shape 不一致，所以我们先让两者的轴数相等，扩展 b：

b:

    array([[0, 1, 2, 3]])

此时，a.shape 为 (4,1)，b.shape 为 (1,4)

从后往前依次处理每根轴，a 的最后一个轴长度小为 1，b 的最后一个轴长度为 4，两者不相等并且，因此需要将 a 的轴长度扩展，并用轴上的第一个值填充扩展出来的部分，扩展 a:

a：

    array([[0,0,0,0],
          [1,1,1,1],
          [2,2,2,2],
          [3,3,3,3]])

此时，a.shape 为 (4,4)，b.shape 为 (1,4)，继续比较轴长度，扩展 b:

b:

    array([[0, 1, 2, 3],
          [0, 1, 2, 3],
          [0, 1, 2, 3],
          [0, 1, 2, 3]])

此时，a.shape 为 (4,4)，b.shape 为 (4,4)，两者相等，可以进行运算：

a + b

    array([[0, 1, 2, 3],
          [1, 2, 3, 4],
          [2, 3, 4, 5],
          [3, 4, 5, 6]])

  

  参考：
  1. [https://www.geeksforgeeks.org/python-broadcasting-with-numpy-arrays/](https://www.geeksforgeeks.org/python-broadcasting-with-numpy-arrays/)
  2. [https://docs.scipy.org/doc/numpy/user/basics.broadcasting.html](https://docs.scipy.org/doc/numpy/user/basics.broadcasting.html)