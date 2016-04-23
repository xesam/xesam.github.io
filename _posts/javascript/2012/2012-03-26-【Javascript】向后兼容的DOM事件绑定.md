---
layout: post
title:  "【Javascript】向后兼容的DOM事件绑定"
date:   2012-03-26 13:46:04 +0800
categories: Javascript
---

## 主要内容

addEventListener绑定方式的问题：

```javascript
document.body.addEventListener( 'click',
    function() {
        alert('body clicked');
    },false);
```
以及第二个参数为object的优势：

```javascript
document.body.addEventListener('click',
    {
        handleEvent: function() {
            alert('body clicked');
        }
    },
    false);
```
原文废话太多，我只翻译了主要部分。原文地址：[原文](http://peter.michaux.ca/articles/our-backwards-dom-event-libraries) 具体细节，请自行查看

先简短的看一下各个浏览器提供的DOM元素事件绑定接口：


```javascript
//IE使用element.attachEvent：
document.body.attachEvent(
    'onclick',
    function() {
        alert('body clicked');
    });
```

```javascript
//其他浏览器使用element.addEventListener：
document.body.addEventListener(
    'click',
    function() {
        alert('body clicked');
    },
    false);
```

一般来说上面的第二个参数都是传入一个函数句柄，但是大多数javascript程序员并不知道第二个参数可以传入一对象obj【DOM2接口 http://www.w3.org/TR/DOM-Level-2-Events/events.html#Events-EventListener 】，如此一来，当event执行的时候，会隐式的调用obj的handleEvent方法。

```javascript
document.body.addEventListener(
    'click',
    {
        handleEvent: function() {
            alert('body clicked');
        }
    },
    false);
```
这么做的一个重要方面是 obj 的 handleEvent 只有在执行的时候才需要去访问【有点类似延迟绑定的效果】。同时，如果在两次event事件间隔中，handleEvent发生了改变，那么产生的效果会跟着改变。这样一个好处就是不用remove事件而直接切换事件。

看下面的例子：

```javascript
document.body.addEventListener('click', obj, false);
// click body will error in some browsers because
// 现在还没有事件
obj.handleEvent = function() {alert('alpha');};

// 单击弹出alpha
obj.handleEvent = function() {alert('beta');};

// 单击弹出"beta"
document.body.removeEventListener('click', obj, false);
//单击什么都没有了

```

【注意，这个用法存在一定的兼容性问题。不过我现在只面向手机浏览器，所以请自行测试】

### 跨浏览器的事件绑定

对于事件绑定，各种库都会处理兼容问题，统一API，大都类似：


```javascript
LIB_addEventListener(
    document.body, 
    'click', 
    function() {
        alert('body clicked');
    });
```

个人实现的一个：

```javascript
    //一个封装
    function LIB_addEventListener(el,type,fn){
        el.addEventListener(type,fn,false);
    }
    function ViewObject() {
        this.data = 'alpha';
        LIB_addEventListener(document.body,'click',this.handleClick);
    }
    ViewObject.prototype.handleClick = function() {
        console.log(this.data);
    };
    var test = new ViewObject();//单击弹出undefined
```

我们期望弹出‘alpha’，但是 this 指向 window，弹出的是 undefined；

解决方式，有的库添加了第四个参数，用来制定上下文：

```javascript
    function LIB_addEventListener(el,type,fn,obj){
        el.addEventListener(type,fn.bind(obj),false);
    }
    function ViewObject() {
        this.data = 'alpha';
        LIB_addEventListener(document.body,'click',this.handleClick,this);
    }
    ViewObject.prototype.handleClick = function() {
        console.log(this.data);
    };
    var test = new ViewObject();
```
此时我们弹出来‘alpha’

这种方式的问题：listener在绑定的时候就已经固定了，于是问题就又来了。

```javascript
    function LIB_addEventListener(el,type,fn,obj){
        el.addEventListener(type,fn.bind(obj),false);
    }
    function ViewObject() {
        this.data = 'alpha';
        LIB_addEventListener(document.body,'click',this.handleClick,this);
    }
    ViewObject.prototype.handleClick = function() {
        console.log(this.data);
    };
    var test = new ViewObject();
    test.handleClick = function(){
        console.log('new fn');//单击弹出的依旧是alpha。我们希望的是new fn
    }
```
采用obj的绑定形式：

```javascript
    function LIB_addEventListener(el,type,obj){
        el.addEventListener(type,obj,false);
    }
    function ViewObject() {
        this.data = 'alpha';
        LIB_addEventListener(document.body, 'click', this);
        LIB_addEventListener(document.body, 'mousemove', this);
    }
    ViewObject.prototype.handleEvent = function(e) {
            if('click' == e.type){
                console.log(this.data)
            }else{
                console.log('not click')
            }
        };

    var test = new ViewObject();
```
上面的例子我改了一下，但是可以说明问题。这样的灵活性也高一些。
