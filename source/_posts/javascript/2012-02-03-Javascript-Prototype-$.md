---
layout: post
title:  "【Javascript】Prototype源码浅析—元素选择器部分(一)之$"
date:   2012-02-03 11:46:04 +0800
categories: javascript
tag: [javascript]
---

## 简述　　

$ 方法是 Prototype 的基础，和jquery中的$作用差不多，不过功能却弱了很多。
因为Prototype中还有一个$$方法，看名字就知道，和$相比，$$加了一倍的钱，功能肯定就丰富撒。本文主要是剖析$方法，1.7版本的$$方法使用的是Sizzle引擎，比较复杂，是后面的事情。

## 基本原理

$ 方法其实比较简单，平时在个人的代码中见得也比较多。
基本原理就是如果传入的是一个字符串，就执行document.getElementById方法，如果是一个DOM元素，就直接返回传入的元素，代码实现：

```javascript
function _$(element){
    if(typeof element == 'string'){
        element = document.getElementById(element);
    }
    return element;
}
```
改进版本，如果传入的是多个字符串id：

```javascript
//如果传入的是多个id，保留上面一个函数
function $(element){
    if(arguments.length > 1){
        for(var i = 0,elements = [],len = arguments.length; i < len; i++){
            if(typeof element == 'string'){
                element = _$(element);
            }
            elements.push(element);
        }
    }
    return elements;
}
```
由于_$中已经做了类型判断，所以_$1中的还可以换种形式，上面的函数还可以换种形式：

```javascript
function $(element){
    if(arguments.length > 1){
        for(var i = 0,elements = [],len = arguments.length; i < len; i++){
            elements.push(_$(element));
        }
    }
    return elements;
}
```
可以组合到一个函数里面:

```javascript
function $(element){
    if(arguments.length > 1){
        for(var i = 0,elements = [],len = arguments.length; i < len; i++){
            elements.push($(element));
        }
        return elements;
    }
    if(typeof element == 'string'){
        element = document.getElementById(element);
    }
    return element;
    //最后一步，这里返回的是扩展了的Element元素，于是return Element.extend(element);
}
```
需要说明的一点是，上面只是获取了目标元素，而且返回的结果里面包含的都是原生的DOM元素，相比Prototype的实现，少了一步元素的扩展，这个留到Element部分。
