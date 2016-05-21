---
layout: post
title:  "【Javascript】Prototype源码浅析——Class部分(一)之类"
date:   2011-12-27 08:36:04 +0800
categories: Javascript
---

说明：

在javascript中，由于缺乏传统面向对象语言的继承机制，类与继承是一个比较复杂的概念。
因此本段解析中，不就javascript中的原型、类、继承、封装进行深入探讨。
需要深入了解的可以去参考大牛的文章，另推荐几本书《javascript高级程序设计》、《javascript语言精髓与编程实践》和《javascript设计模式》，多读几遍就会对javascript的原型有深入的了解。

所以本文只就Prototype远源码涉及到的部分进行解析。

到Class这一步，需要说一下前面没有说到的单体模式，通过前面的几个部分的观察，会发现整个Prototype部分，大部分对象的方法扩展采用的都是类似下面的形式：

```javascript
    var obj = (function(){
        var variable ;
        function method(){}
        return {
            method:method
        }
    })();
```
这就是单体模式。

不过这么做有什么好处呢？

单体简单的理解就是一个对象。比如：

```javascript
    var obj = {
        name : 'xesam',
        say  : function(){
            console.log(this.name);
        }
    };
    obj.say();
```
此时，obj有个作用就是可以提供一个命名空间，并且组织了一部分变量和方法。

不够这样的一个去缺点就是name完全暴露在外面，可以随意修改，如果name对我们来说是私有的，那么这么样就无法满足要求了。所以鉴于JS中奇特的作用域限制，我们自然得依靠函数来帮忙，于是修改如下：

```javascript
    var obj = function(){
        var name = 'xesam';
        function say(){
            console.log(name);
        }
    };
    obj.say();
```
此时，name变成一个局部变量，外界就无法访问了，不过此时obj.say()也会报错，因为obj已经不是一个对象（这里的对象是指普通对象，而非函数这种对象）了，因此我们再让函数自执行，返回我们需要的对象：

```javascript
    var obj = (function(){
        var name = 'xesam';
        function say(){
            console.log(name);
        }
        return {
            say : say
        }
    })();
    obj.say();
```
于是就得到了类似Prototype中的形式，这么做的好处大概也就出来了，变量和方法的组织，数据的封装和隐藏。两外，由于匿名函数只执行（实例化）了一次，所以也不会带来内存的问题。如果愿意，也可以这么样来模拟JS中的Math对象。

现在回到Prototype的Class部分，我们来一步步实现Prototype中的Class部分。

对于最常见的类的声明，就是创建一个构造函数，然后扩展其原型。比如：

```javascript
    function Person(name){
        this.name = name;
    }
    Person.prototype.say = function(){
        console.log('hello ' + this.name);
    }
    var xesam = new Person('xesam');
    xesam.say();
```
上面定义构造函数和添加方法分开了，现在我们把他们打包到一起。运用刚才说故偶的单体模式，我们先定义一个对象，用作命名空间：

```javascript
var Class = {}
```
现在需要提供的是一个初始化变量和添加方法的功能。

写之前我们先得规定一下最终形式的调用方法，我们还是尊重Prototype的形式，并且以上面的Person类为例，声明Person类的形式为：

```javascript
    var Person = Class.create({
        initialize:function(name){
            this.name = name;
        },
        say : function(){
            console.log('hello ' + this.name);
        }
    });
    var xesam =new Person('xesam');
    xesam.say();
```
如上所示，Class.create的参数是一个对象，其中initialize包含的是初始化部分（相当于普通面向对象的构造函数），其他部分（say）则是需要添加的方法

【说明：initialize是必须的，其他则可选】

在实现之前，我们先准备一个工具函数$A，作用就是获得一个对象的数组形式（转化为一个数组）：

```javascript
    function $A(iterable) {
        if (!iterable) return [];
        if ('toArray' in Object(iterable)) return iterable.toArray();
        var length = iterable.length || 0, results = new Array(length);
        while (length--) results[length] = iterable[length];
        return results;
    }
```
这个方法挺简单的，无需多说。

下面我们可以获得一个最简单的Class.create实现：

```javascript
    var Class = {};
    Class.create = function(source){
        return function(){
            for(var i in source){
                this[i] = function(){
                    source[i].apply(this,$A(arguments));
                }
                //如果你还记得Function部分的内容，这里可以写成this[i] = source[i].bind();
            }
            source.initialize.apply(this,arguments);
        }
    }

    var Person = Class.create({
        initialize:function(name){
            this.name = name;
        },
        say : function(){
            console.log('hello ' + this.name);
        }
    });
    var xesam =new Person('xesam');
    xesam.say();
```
上面create返回的是一个匿名函数，我们还可以采用另一种方式，先声明一个函数，处理这个函数之后再返回：

```javascript
    Class.create = function(source){
        var kclass = function(){
            this.initialize.apply(this,arguments);
        };
        for(var i in source){
            kclass.prototype[i] = source[i];
        }
        return kclass;
    };
```
这里先前的实现其实差不多，而且和最初的Person比较吻合。

分析上面的实现，你会发现定义完成之后，除了去改动初始定义，就没办法扩展了。因此我们在打包了之后再将具体实现分开，将Class分为初始化和添加方法两个部分，并使用刚才说过的单体模式来组织：

```javascript
    var Class = (function(){
         function create(source){
            function kclass(){
                this.initialize.apply(this,arguments);
            };
            addMethods.call(kclass,source);//注意这里的调用
            return kclass;
        }
        function addMethods(source){
            for(var property in source){
                this.prototype[property] = source[property];
            }
        }
        return {
            create : create,
            addMethods : addMethods
        }
    })();
```
这么处理过之后，addMethods方法分离出来了，但是现在还是在Class对象上，并不会添加到我们新创建的Person类上面，所以我们将addMethods添加到实现中的kclass上面。

```javascript
kclass.addMethods = addMethods;//（代码4-1）
```
注意，这里有个关于扩展性的问题。如果我们的Class并不是只有addMethods一个方法，而且有addMethods1，addMethods2，addMethods3···方法，那么我们总不能按照这个顺序一并写下去吧，所以我们可以用一个对象（比如叫Methods）来把这些方法都组织起来。所以代码4-1的形式变成：

```javascript
kclass.addMethods = Methods.addMethods;
```
继续分析，create的参数可能是多个需要添加的方法，因此不能用一个形参source来限定死了，采用内置的arguments对象来替代。所以Class的基本骨架就出来了：

```javascript
    var Class = (function(){
         function create(){
            var properties = $A(arguments);
            function kclass(){
                this.initialize.apply(this,arguments);//实例化的时候，这里自动调用了initialize方法
            };
            kclass.addMethods = Class.Methods.addMethods;
             //在Prototype中由于有一个Object方法，所以这里调用的是Object.extend(Class.Methods)方法
            for(var i = 0; i < properties.length; i++){
                kclass.addMethods(properties[i]);
            }
            if (!kclass.prototype.initialize){//这里是一个小检测，避免因找不到initialize而报错
                kclass.prototype.initialize = function(){};
            }
            return kclass;
        }
        function addMethods(source){
            for(var property in source){
                this.prototype[property] = source[property];
            }
        }
        return {
            create : create,
            Methods : { //注意这里的改动
                addMethods : addMethods
            }
        }
    })();
```

到此，我们有了一个Class对象（可以创建类和添加方法）和一个Person类（有name属性和say方法）。