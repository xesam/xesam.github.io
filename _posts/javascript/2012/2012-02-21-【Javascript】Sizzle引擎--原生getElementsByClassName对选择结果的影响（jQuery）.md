---
layout: post
title:  "【Javascript】Sizzle引擎--原生getElementsByClassName对选择结果的影响（jQuery）"
date:   2012-02-21 10:46:04 +0800
categories: Javascript
---

个人觉得这个例子虽然可能不具有实际意义，但是可以很好的理解Sizzle选择的过程

## 实例说明

先看一个例子：

```html
<html>
<head>
    <meta http-equiv="Content-Type" content="text/html; charset=utf-8"/>
    <title></title>
</head>
<body>
    <p class="tab" id="a1">1</p>
    <p class="tab" id="a2">2</p>
    <p class="tab" id="a3">3</p>
<script type="text/javascript" src="../sizzle.js"></script>
<script type="text/javascript">
    console.log(Sizzle('.tab:not(:first)'));  
    console.log(Sizzle('p:not(:first)'));      
    console.log(Sizzle('p.tab:not(:first)'));  
</script>
</body>
</html>
```
看上面三个结果的三个表达式，估计很多人会觉得结果肯定是一样的，不错，除去IE6/7/8，结果应该都是一样的，结果（一）：

```javascript
    console.log(Sizzle('.tab:not(:first)'));  //[#a2,#a3]
    console.log(Sizzle('p:not(:first)'));     //[#a2,#a3]
    console.log(Sizzle('p.tab:not(:first)')); //[#a2,#a3]
```

但是在IE6/7/8下面，结果（二）：

```javascript
    console.log(Sizzle('.tab:not(:first)'));  //[#a1,#a2，#a3]
    console.log(Sizzle('p:not(:first)'));     //[#a2,#a3]
    console.log(Sizzle('p.tab:not(:first)')); //[#a2,#a3]
```
    
其实不仅是IE6/7/8，任何不支持 getElementsByClassName 方法的浏览器结果都是结果（二）这样。

### 结果分析

在结果（一）的过程中，

'.tab:not(:first)'选择流程是：

1. document.getElementsByClassName('.tab')获得结果集[#a1,#a2,#a3];
2. 过滤:not(:first)，获得结果集[#a2,#a3];
    
'p:not(:first)'选择流程是：

1. document.getElementsByTagName('p')获得结果集[#a1,#a2,#a3];
2. 过滤:not(:first)，获得结果集[#a2,#a3];

'p.tab:not(:first)'选择流程是：

1. document.getElementsByClassName('.tab')获得结果集[#a1,#a2,#a3];
2. 过滤p，获得结果集[#a1,#a2,#a3];
3. 过滤:not(:first)，获得结果集[#a2,#a3];

在结果（二）的过程中：

'.tab:not(:first)'选择流程是：

1. document.getElementsByTagName('*')获得结果集[html,head,body,#a1,#a2,#a3,script,script]
2. 过滤:not(:first)，获得结果集[head,body,#a1,#a2,#a3,script,script]
3. 过滤.tab，获得结果集[#a1,#a2,#a3]

'p:not(:first)'选择流程是：

1. document.getElementsByTagName('p')获得结果集[#a1,#a2,#a3];
2. 过滤:not(:first)，获得结果集[#a2,#a3];

'p.tab:not(:first)'选择流程是：

1. document.getElementsByTagName('p')获得结果集[#a1,#a2,#a3];
2. 过滤:not(:first)，获得结果集[#a2,#a3];
3. 过滤.tab，获得结果集[#a2,#a3]

可以看到，在不含class的选择符中，两种情况过程是一样的，当含有class的时候，会优先去寻找含有class的元素，从而直接影响了后面过滤步骤的候选集。

### 原因分析

至于产生的原因，我们回到代码层面来解释：

#### 第一个影响因素

先看Sizzle.find部分

```javascript
for ( i = 0, len = Expr.order.length; i < len; i++ ) {}

Expr.order: [ "ID", "NAME", "TAG" ];
```

最初的查找的时候，匹配type的是有一个优先级的 ID-->NAME-->TAG ,对于支持 getElementsByClassName 的浏览器，Sizzle 源码进行了一个处理：

在1296行：

```javascript
Expr.order.splice(1, 0, "CLASS");
    Expr.find.CLASS = function( match, context, isXML ) {
        if ( typeof context.getElementsByClassName !== "undefined" && !isXML ) {
            return context.getElementsByClassName(match[1]);
        }
    };
```
于是在支持getElementsByClassName的浏览器中，Sizzle.find的实现变成

```javascript
for ( i = 0, len = Expr.order.length; i < len; i++ ) {}

Expr.order: [ "ID","CLASS" "NAME", "TAG" ];
```

而且CLASS的优先级仅次于ID。

所以.tab:not(:first)在过滤的第一步，不同浏览器的候选集就已经发生了差异。

#### 第二个影响因素

再看Sizzle.filter部分

```javascript
for ( type in Expr.filter ) {}
Expr.filter={
        CLASS: function( match, curLoop, inplace, result, not, isXML ) {},
        ID: function( match ) {},
        TAG: function( match, curLoop ) {},
        CHILD: function( match ) {},
        ATTR: function( match, curLoop, inplace, result, not, isXML ) {},
        PSEUDO: function( match, curLoop, inplace, result, not ) {}
        POS: function( match ) {}
    },
```

这里与 Sizzle.find 的一个显著不同是这里用的 for..in 循环，没有确定的顺序【优先级】，因此并不能保证先过滤什么类型。

所以.tab:not(:first)在先过滤了:not(:first)，然后再过滤.tab，所以结果和想想的不一致。

#### 第三个影响因素

这个涉及到filter的实现，对于含有not的表达式，候选集合会被筛选一遍。

.tab:not(:first)在not部分集合改变，直接去除了第一个元素。

.tab:first 就没有改变，因为first是在POS匹配中处理的。

## 解决方案

如果我们把Sizzle.filter的实现改成和Sizzle.find一致，变成如下形式：


```javascript
for ( i = 0, len = Expr.filterOrder.length; i < len; i++ ) {}

Expr.filterOrder: [ "ID","CLASS" "NAME", "TAG" ,"ATTR","CHILD","PSEUDO","POS"];
```

那么我们就可以保证选择的结果和预期的一致。不过这种牵一发而动全身的事情，显然是不适合的。

另外一个方法就是避免使用这种有歧义的选择符，将:not(:first)作为集合的一个方法调用，而不直接写到选择表达式里面。

另外，如果知道DOM的结构，处理方式就很多了，比如加tag限制，层级限制等等

## 说明

这种问题并不是出现在没个类似的选择表达式中，具体的情况可以查看Sizzle源码的filter部分。

filter部分比较麻烦，有什么错误之处，欢迎交流。

