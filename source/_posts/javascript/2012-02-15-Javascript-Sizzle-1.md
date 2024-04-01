---
layout: post
title:  "【Javascript】Sizzle引擎--原理与实践（一）"
date:   2012-02-15 11:46:04 +0800
categories: javascript
tag: [javascript]
---

## 简述
Sizzle是jQuery的御用选择器引擎，是jQuery作者John Resig写的DOM选择器引擎，速度号称业界第一。
另外，Sizzle是独立的一部分，不依赖任何库，如果你不想用jQuery,可 以只用Sizzle。
所以单独拿出来特别对待。在Prototype1.7中，选择器也采用了Sizzle，不过版本有点老，所以我去Sizzle网站搞了一份新的 下来，于是下面分析的时候使用的是最新版的Sizzle.js

## 预先说明

在分析初期为了保证各个浏览器的结果一致，不考虑原生getElementsByClass以及querySelectorAll的影响，同时忽略XML类型，因此作一下处理：

源码1292行，

```javascript
    (function(){
        ...
    })()
```

改为：

```javascript
    (function(){
        return false;
        ...
    })()
```
源码1140行

```javascript
if ( document.querySelectorAll ) {
    ...
}
```
改为：

```javascript
if ( document.querySelectorAll && false) {
    ...
}
```
至于其他的浏览器兼容处理部分，会在初步分析中一并涉及。

## 预备知识

CSS选择器，jQuery选择器。由于jQuery选择器的形式来自CSS，但是在CSS的基础上又增加了很多新的选择表达式，因此，一切以jQuery选择器为基础。

### 实例开题

对于一个选择表达式：

    div#outer > ul , div p:nth(1)，form input[type="text"]
    
#### 关于分块的讨论

这里面包含三个并联的选择符，我们怎么处理？

解决方案：

    1. 可以用split(',')来处理，但是这样只是单纯的分割出来了，并不能获得更多的信息。
    2. 所以我们采用正则来分块，缺点是可读性以及效率的问题，优点是可以提取一些必要的信息，进行预处理。

所以jquery采取的是正则，但是并没有完全分块，而是一部分一部分的取。对于上面的例子我们看看怎么分块。

div#outer > ul , div p:nth(1)，form input[type="text"] 

先分离出来 div#outer > ul，处理完毕后再分离出来 div p:nth(1)，处理完毕后再分离出来 form input[type="text"]，最后合并三部分的结果

#### 关于选择顺序的讨论

这里需要记得jQuery选择器的作用，一个典型的例子：

    body div p:first-child
    body div p:first

这两个的含义完全不一样，如果可以用括号这么写的话，可以改成：

    body div p:first-child --> body div (p:first-child)
    body div p:first --> (body div p):first

first-child 是用来限定 p 的，可以算是 p 的一个属性，

body div p:first 是用来限定 body div p 结果集的，可以算是 body div p 结果集的一个方法。

body div p:first == (body div p).eq(0)

类似的情况还有jQuery自定义的几个位置查询表达式，所以

情况一、body div p:first

　　自左向右的查询。先找到body，获得集合A，然后在集合A中查找div获得集合B，在集合B中查找p获得集合C，最后取集合C的第一个元素，得最终结果XX

情况二、body div p:first-child　　

　　自右向左的查询，先找到p:first-child获得集合A1，然后判断祖先元素里面是否有div获得集合B1，然后判断祖先元素里面是否有body获得集合C1，得最终结果C1

　　对比上面的两个过程，相较于过程一，过程二更像是一个过滤的过程，因此，Sizzle最大的亮点是自右向左过滤。

　　另外，为了提高查询效率，最重要的就是缩小查找范围和减少遍历次数。

一个典型的例子是：

    div p

情况一、先找到p，获得集合A，然后判断祖先元素里面是否有div获得集合B,得最终结果B

    div#a p
    
 #a 一般只会有一个，所以情况一里面p的范围太大了，所以如果第一个选择表达式里面含有id，Sizzle总是先查找第一个，从而缩小查找范围
 
情况二、先找到div#a，获得单个元素A1，然后再A1的环境中查找p，得最终结果B1

因此，最终的过程就变成

1. 分割表达式
2. 查找元素
3. 过滤元素（过滤分两种，1、通过元素自身属性过滤 2、通过元素之间关系过滤。）

因此可以获得Sizzle的大致代码结构

Sizzle引擎基本结构

    主要流程：window.Sizzle = function(){};
    查找元素：Sizzle.find = function(){};
    过滤元素：Sizzle.filter = function(){};

定义用到的一些查找方式和过滤条件：Sizzle.selectors = {};

Sizzle.selectors 经常要用到，于是给它一个简短的名字，就叫做 Expr

于是Sizzle的代码框架如下：


```javascript
window.Sizzle = function(){
    //主要负责分块和主线流程，通过元素之间关系过滤也被放在这个部分
};
Sizzle.find = function(){
    //查找元素
};
Sizzle.filter = function(){
    //过滤元素，主要处理通过元素自身属性过滤
};
Sizzle.selectors = {
    //命名空间，以及定义一些变量和特异方法
};
var Expr = Sizzle.selectors;//别称
```
剩下的问题就是怎么获得我们需要的元素集合

## 关于查找元素的初步讨论

我们先看，怎么找元素，浏览器原生只有三种查找元素的方式（文章开头我们已经假设初步所有的浏览器原生都不支持getElementsByClassName，虽然大部分都支持）：

```javascript
    getElementById
    getElementsByName
    getElementsByTagName
```

### 问题一
当我们遇到一个选择表达式的时候，怎么判断这个选择表达式是什么类型的。

解决方案：

依次检测这个表达式的类型，获得匹配的类型，注意，一旦获得了匹配的类型，就不会继续匹配了。至于先匹配哪个类型，查找原则就是尽可能的缩小检索范围（特异性越高，检索范围就越小）。一般情况下，ID数量小于NAME数量,NAME数量又小于TAG数量。因此判断顺序就是['ID','NAME','TAG']

实例说明：

1. input[name="test"]，先查找[name="test"]，此时虽然还可以继续查找input，但是没有那个必要了，因为如果查询input之后再去取交集，会破坏程序的结构。

Sizzle的处理方式就是：先查找[name="test"]获得集合A，然后在A中过滤input，input被作为一个过滤条件丢到过滤部分去处理。

2. input#demo[name="test"] 由于ID的优先级比NAME高，所以先查找#demo获得集合A，然后在A中过滤input[name="test"]，input[name="test"]被作为一个过滤条件丢到过滤部分去处理。

#### 关于过滤元素的初步讨论

过滤是一个条件一个条件来进行的，对于一个集合A以及过滤表达式

```javascript
expr='[class="test"][rel=1]:first-child'
```

在A中过滤[class="test"]得到集合B，此时过滤表达式expr='[rel=1]:first-child'

在B中过滤[rel=1]得到集合C，此时过滤表达式expr=':first-child'

在C中过滤:first-child得到集合D，此时过滤表达式expr=''，过滤完毕

【说明，上面的顺序不代表真实的顺序，是指为了说明“过滤是一个条件一个条件来进行的”这句活而已】

过滤分两步：

1. 预过滤Expr.preFilter，处理兼容问题以及格式转换，决定下一步的走向
2. 最终过滤Expr.filter，这一步的形式都是一样的，最终返回的都是一个布尔值。

过滤方式：

    假设第一轮的筛选集合：A = ['#1','#2','#3','#4','#5','#6']
    过滤条件为isMatch
    满足条件的集合为C = ['#1','#2','#3']

第一、

```javascript
var B = [];
for( i = 0; (item = A[i]) != null; i++ ){
    A[i] = isMatch(item);
}
for( i = 0;  i < A.length; i++ ){
    if(A[i]){
        B.push(A[i]);
    }
}
```

1. ['#1','#2','#3','#4','#5','#6']
2. ['#1','#2','#3',false,false,false]
3. ['#1','#2','#3']

第二、

```javascript
var B = [];
for( i = 0; (item = A[i]) != null; i++ ){
    if(isMatch(item)){
        B.push(A[i]);
    }
}
```
