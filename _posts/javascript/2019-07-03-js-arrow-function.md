---
layout: post
title:  "Arrow Function"
date:   2019-07-03 07:00:00 +0800
categories: javascript
tag: [javascript]
---
起源：有人发给我下面一段代码：

```html
<script>
    var name = '11';
    var obj = {
        name:'22',
        fun1:()=>{
            console.log(this.name);
        }
    };
    obj.fun1(); // '11'
</script>

```
问了两个问题：

    为什么打印出来的不是 '22'?
    为什么打印出来的不是 undefined?
<!-- more -->

首先，不谈这两个问题，这段代码本身有个比较严重的问题：

    在使用 ES2015 新特性箭头的同时，又使用了 var 关键字，这是完全不应该的，var 应该永远被抛弃。


回到问题本身，这是两个不同的问题。

#### 为什么打印出来的不是 '22'?

这是箭头函数的规范所致，一句话概括：

    箭头函数的 this 指向创建时所在函数的 this，如果不在函数中，就指向外层上下文的 this。总之，是在创建时（或者说定义时）确定的。

相比之下：

    普通函数的 this 就比较直观，一直指向调用者，总之，是在执行时确定的。


所以，原代码在浏览器中会输出'11',如果改成下面的形式，就能够如期输出 '22'。

```javascript
    var name = '11';
    var obj = {
        name:'22',
        fun1:function(){
            console.log(this.name);
        }
    };
    obj.fun1(); // '22'
```

至于为什么要强调在浏览器中输出'11'，就涉及到第二个问题了。

#### 为什么打印出来的不是 undefined?

在浏览器中，不使用关键字修饰的变量以及在最外层用 var 关键字修饰的变量，默认都是全局变量 window 的一个属性。因此，原代码等同于：

```html
<script>
    window.name = '11';
    window.obj = {
        name:'22',
        fun1:()=>{
            console.log(window.name);
        }
    };
    obj.fun1(); // '11'
</script>

```

这也是 var 的一个固有问题，所以回过头说，还是应该使用 const 或者 let，避免这种默认的机制：

```html
<script>
    const name = '11';
    let obj = {
        name:'22',
        fun1:()=>{
            console.log(window.name);
        }
    };
    obj.fun1(); // undefined
</script>

```

在非浏览器的运行时中，就得看运行时各自的规范定义了，比如在 node 中，模块中的 this 指向 module.exports：

```javascript
    var name = '11';
    exports.name = '33';
    var obj = {
        name:'22',
        fun1:()=>{
            console.log(this.name);
        }
    };
    obj.fun1(); // '33'
```

至于其他老黄历，即便知道了也没用！反正别这么写就行了。


