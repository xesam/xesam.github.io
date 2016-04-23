---
layout: post
title:  "【Javascript】Sizzle引擎--原理与实践（五）"
date:   2012-02-25 10:46:04 +0800
categories: Javascript
---

这篇是关于Sizzle.filter部分的详细分解，前提是先看懂Sizzle.filter的分发过程。

回顾一下Sizzle.filter的过程：

```javascript
match = preFilter()
if(match){
    filter()
}
```
当preFilter返回为false的时候，filter就被短路了。

### 过滤CLASS

怎么判断一个元素时候含有某个类，源码中的方法：

```javascript
    function checkClass(elem,className,not){
        return not ^ (' ' + elem.className + ' ').indexOf(' '+ className +' ') > -1;
    }
```

注意那个not参数，前面有提到过的，取补集而已。

    checkClass(elem,className)  --->hasClass(elem,className)
    checkClass(elem,className,true)  --->hasNoClass(elem,className)

#### 实例

```html
<div id="test" class="a b c d"></div>
<script type="text/javascript">
    function checkClass(elem,className,not){
        return not ^ (' ' + elem.className + ' ').indexOf(' '+ className +' ') > -1;
    }
    var test = document.getElementById('test');
    console.log(checkClass(test,'a')); //1
    console.log(checkClass(test,'b')); //1
    console.log(checkClass(test,'e')); //0

    var test = document.getElementById('test');
    console.log(checkClass(test,'a',true)); //0
    console.log(checkClass(test,'b',true)); //0
    console.log(checkClass(test,'e',true)); //1
</script>
```

对照

```javascript
Expr.match.CLASS = /\.((?:[\w\u00c0-\uFFFF\-]|\\.)+)/;
```

获得的一个类似['.className','className']的数组，取做match，经过层层处理之后，传递给preFilter.CLASS的形式主要是['.className','className',?,?]的形式，因此在CLASS处理部分，只需要match的前两个参数就可以了。

因此在CLASS的preFilter部分，其大致处理形式就是这样的：

```javascript
   preFilter.CLASS =  function( match, curLoop, inplace, result, not, isXML ) {
        match = " " + match[1].replace( rBackslash, "" ) + " ";
        if ( isXML ) {//是否是XML，咱可以不考虑
            return match;
        }
        //依次遍历curLoop中的待检测元素
        for ( var i = 0, elem; (elem = curLoop[i]) != null; i++ ) {
            if ( elem ) {
                //找到对应的类
                if ( not ^ (elem.className && (" " + elem.className + " ").replace(/[\t\n\r]/g, " ").indexOf(match) >= 0) ) {
                    if ( !inplace ) {//找到对应的类，而且不允许就地修改的时候，将满足条件的存入result
                        result.push( elem );
                    }
                } else if ( inplace ) {//没有对应的类，而且允许就地修改的时候，将对应项的数据改为false
                    curLoop[i] = false;
                }
            }
        }
        return false;//这里在非XML的情况下，都是返回false，因此后面的filter部分始终被短路
    };
```
在上面的步骤中，需要注意的是curLoop已经result是两个数组，属于引用类型，任何改变都会反映到外部的集合中。已经得到了过滤的结果，因此返回false，无需再执行其他步骤。

至于filter.CLASS就是单纯的判断是否含有某个类而已：

```javascript
    filter.CLASS: function( elem, match ) {
        return (" " + (elem.className || elem.getAttribute("class")) + " ").indexOf( match ) > -1;
    },
```
上面的代码已经很清晰了。

### 过滤ID

```javascript
ID: /#((?:[\w\u00c0-\uFFFF\-]|\\.)+)/
```

match的形式如['#id','id']

这个步骤就很简单了，

preFilter处理match[1]的格式问题

```javascript
    preFilter.ID: function( match ) {
        return match[1].replace( rBackslash, "" );
    },
```
filter判断元素的id是不是给定的id

```javascript
    filter.ID: function( elem, match ) {
        return elem.nodeType === 1 && elem.getAttribute("id") === match;
    },
```    

一般来说，要判断id的情况并不多，因为id一般都在Sizzle.find被处理掉了，再来过滤id严重拖慢速度，expr表达式写得估计有问题。

### 过滤TAG

同过滤ID

### 过滤ATTR

过滤attr的过程在filter部分的时候作为实例带过，此处忽略

### 过滤Child

Child有点复杂了，可以从选择符的形式着手。

举个栗子：

```html
<div>
    <p class="tab" id="a1">1</p>
    <p class="tab" id="a2">2</p>
    <p class="tab" id="a3">3</p>
</div>
<div>
    <p class="tab" id="a4">4</p>
</div>
<script type="text/javascript">
    console.log(Sizzle('p:only-child'));     //[#a4]
    console.log(Sizzle('p:last-child'));     //[#a3,#a4]
    console.log(Sizzle('p:first-child'));    //[#a1,,#a4]
    console.log(Sizzle('p:nth-child(1)'));   //[#a1,#a4]
    console.log(Sizzle('p:nth-child(odd)')); //[#a1,#a3,#a4]
    console.log(Sizzle('p:nth-child(even)'));//[#a2]
    console.log(Sizzle('p:nth-child(n)'));   //[#a1,#a2,#a3,#a4]
    console.log(Sizzle('p:nth-child(2n+1)'));//[#a1,#a3,#a4]
</script>
```

在上面的几个形式中，可以分为两组：

only-child,last-child,first-child分为一组A

nth-child单独为一组B。

虽然由 nth-child 可以完全得到组A，但是组A是特殊形式的简便方式。

另外，这两种方式的代码形式的主要是组A不能再带位置参数，组B必须后接一个位置参数。

比如‘last-child(2)’是不行的，‘nth-child’是不行的，这个看名字就可以理解。

先看

```javascript
    CHILD: /:(only|nth|last|first)-child(?:\(\s*(even|odd|(?:[+\-]?\d+|(?:[+\-]?\d*)?n\s*(?:[+\-]\s*\d+)?))\s*\))?/,
```
匹配（match）的分组就是match = ['nth-child','nth','2n+1']或者match = ['first-child','first',undefined]的形式。
其中nth那种的位置表达式可能比较多，因此preFilter中处理的问题就是把nth形式中的各种形式转换成统一的形式。

转换原理

even 转换成 2n，odd 转换成 2n+1,5 转换成 0n+5 ，可得最后要得到的形式就是 an+b 的形式。

```javascript
match[2] === "even" && "2n";//对于even的形式转化为2n
match[2] === "odd" && "2n+1;"//对于odd的形式转化为2n+1
!/\D/.test( match[2] ) && "0n+" + match[2];//对于纯数字(比如'nth-child(5)')的形式转化为'nth-child(0n+5)'
match[2];//其他形式('3n+4')的直接保留
//这里理解&&这种操作符的用途就行，虽然某些人说这种用法并不提倡。
```

现在形式统一了，只需要提取出an+b中相应的a和b就可以了，提取方式当然用正则，注意a、b都可能为负数。

```javascript
    var test = /(-?)(\d*)(?:n([+\-]?\d*))?/.exec('an+b');
```

获得的test分组类似['an+b','-','a','+b']，对于实例‘-2n-1’就是['-2n-1','-','2','-1']

现在每个数组都是字符串，需要时数字才便于处理，因此我们先将数字字符串转换为纯数字，字符串转换为数字也挺简单：

```javascript
number = numberStr-0
```
因此这个基本步骤就是：

```javascript
var posStr = match[2] === "even" && "2n" || match[2] === "odd" && "2n+1" ||!/\D/.test( match[2] ) && "0n+" + match[2] || match[2];
var test = /(-?)(\d*)(?:n([+\-]?\d*))?/.exec(posStr);//分离an+b
var temp1 = (test[1] + (test[2] || 1)) - 0;          //'a'转化为a，带符号
var temp2 = test[3] - 0;                             //‘b’转化为b，也带符号
```
看具体源码：

```javascript
CHILD: function( match ) {
    if ( match[1] === "nth" ) {
        if ( !match[2] ) {  //nth的形式必须有位置参数
            Sizzle.error( match[0] );
        }
        match[2] = match[2].replace(/^\+|\s*/g, '');//去除开头的加号或者结尾的空白
        //下面的步骤就对应于上面的分解步骤
        var test = /(-?)(\d*)(?:n([+\-]?\d*))?/.exec(
            match[2] === "even" && "2n" || match[2] === "odd" && "2n+1" ||!/\D/.test( match[2] ) && "0n+" + match[2] || match[2]);
        match[2] = (test[1] + (test[2] || 1)) - 0;
        match[3] = test[3] - 0;
        //到这里的时候，match的形式已经统一成['nth-child(??)','nth',a,b]的形式
    }
    else if ( match[2] ) {//非nth的形式一定不能有位置参数
        Sizzle.error( match[0] );
    }

    match[0] = done++;
    //到这里的时候，match的形式已经统一成[done,'nth',a,b]的形式
    return match;
},
```

### 过滤POS

### 过滤PSEUDO
