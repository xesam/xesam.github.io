---
layout: post
title:  "【Javascript】Prototype源码浅析—Enumerable部分(一)"
date:   2012-01-16 11:46:04 +0800
categories: javascript
tag: [javascript]
---

在javascript中，根本找不到 Enumerable 的影子，因为这一块是Prototype作者从Ruby中借鉴过来的。
并且Enumerable在实际中根本没有直接应用的机会，都是混入到其他的对象中，可以说是其他对象的一个“父类”（不过只是调用了Object的extend方法，进行了方法的直接拷贝而已）。

我并不熟悉Ruby，不过看Enumerable中的一些方法，倒是跟Python中的有几分相似。

Enumerable其中一个最重要的方法是each，each这个方法应该都比较熟悉，其作用便是遍历一个序列的所有元素，并进行相应的处理。不过多数是应用在数组上，比如原生数组的forEach方法，以及jQuery中的链式调用，都依赖于each方法。因为jQuery选择器返回的是一个DOM对象数组，然后再在返回的数组上来调用each，从而分别处理每一个元素。

一般each都有两个参数：一个是迭代处理的函数和方法对应的上下文。

```javascript
    var each = Array.prototype.forEach || function(iterator,context){
        for(var i = 0,len = this.length ; i < len ; i++){
           iterator.call(context,this[i],this);
        }
    };
```
按照上面的方法，我们给Array对象扩展一个打印当前所有元素的print方法。

```javascript
    Array.prototype.each = Array.prototype.forEach || function(iterator,context){
        for(var i = 0,len = this.length ; i < len ; i++){
            iterator.call(context,this[i],i,this);
        }
    };
    Array.prototype.print = function(){
        this.each(function(item){
            console.log(item);
        });
    }
    console.log([1,2,3,4].print());//1,2,3,4
```

在Enumerable中，each并没有对应到具体的方法，前面说过Enumerable并不之际应用，而是作为一个“父类”应用到其他的对象，因此它的each方法是调用“子类”_each方法，因此任何混入Enumerable模块的对象，都必须提供一个_each方法，作为作用于实际循环的迭代代码。

现在Array.prototype上实现一个_each方法和一个each方法，实现一：

```javascript
    Array.prototype.each = function(iterator,context){
        this._each(iterator,context)
    }
    Array.prototype._each = function(iterator,context){
        for(var i = 0,len = this.length ; i < len ; i++){
            iterator.call(context,this[i],i,this);
        }
    };
    
```
按照先前说的，_each只需要提供一个iterator参数就可以了，不过由于_each也被扩展到Array.prototype上面，于是实现的时候也附带了context参数。因此在Enumerable中，并没有使用_each的第二个context参数，是否实现对each没有影响。因此上面的实现一 不应该依赖_each的context，于是修改each如下：

```javascript
    Array.prototype.each = function(iterator,context){
        var index = 0;
        this._each(function(value){
            iterator.call(context,value,index++);
        })
    }
```
　　
这样一来，each方法的独立性提高了，在后续的Hash中也可以使用这个Enumerable了。任何看遍历的对象，只要提供了_each方法，就可以从Enumerable这里获得相应的方法。

因此，将上面的print例子用Enumerable的形式来实现，便得到如下的结果：

```javascript
    var Enumerable = {};
    Enumerable.each = function(iterator, context) {
        var index = 0;
        this._each(function(value){
            iterator.call(context, value, index++);
        });
        return this;
    };
    Enumerable.print = function(){
        this.each(function(item){
            console.log(item);
        })
    };
    Array.prototype._each = function(iterator,context){
        for(var i = 0,len = this.length ; i < len ; i++){
            iterator.call(context,this[i],i,this);
        }
    };
    //下面的实现源码中是用的extend方法
    for(var key in Enumerable){
        Array.prototype[key] = Enumerable[key];
    };
    [1,2,3,4].print();//1,2,3,4
```

理解each的实现是理解Enumerable对象的关键，后面的Array和Hash都混入Enumerable对象，颇为重要。
