---
layout: post
title:  "【Javascript】Prototype源码浅析——Object部分(二)之类型检测"
date:   2011-12-21 08:36:04 +0800
categories: javascript
tag: [javascript]
---
这里我不关心javascript里面各种类型是怎么定义的，唯一要指出的是

```javascript
var str_1 = 'xesam';
var str_2 = new String('xesam');
console.log(str_1 === str_2);
```

其中str_1和str_2不是同一个东西，先前看到群里面有个人提到类似的一个问题，所以才想起来的。

检测一个变量的类型，最常见的就是typeof操作符。typeof的返回值是一个字符串，一般只能返回如下几个结果：

    number,boolean,string,function,object,undefined

但是显然要是我们想区分Date，RegExp这样的具体类，typeof就没有办法了，于是统一归结到object里面。

先看一下Prototype里面的一些定义：

      NULL_TYPE = 'Null',
      UNDEFINED_TYPE = 'Undefined',
      BOOLEAN_TYPE = 'Boolean',
      NUMBER_TYPE = 'Number',
      STRING_TYPE = 'String',
      OBJECT_TYPE = 'Object',
      FUNCTION_CLASS = '[object Function]',
      BOOLEAN_CLASS = '[object Boolean]',
      NUMBER_CLASS = '[object Number]',
      STRING_CLASS = '[object String]',
      ARRAY_CLASS = '[object Array]',
      DATE_CLASS = '[object Date]',
      
【这些变量的值是作为规定的结果返回，避免人为错误】

回到变量检测上，我们看个实例：

```javascript
    var array_1 = [null,undefined,10,NaN,'10',true,function(){}];
    var array_2 = [new Function(),new String(),new Number(),new Boolean(true),{},[],/x/,new Error(),new Date()];
    var varArray = array_1.concat(array_2);
    (function(){
        for(var i in varArray){
            console.log(typeof varArray[i]);
        }
    })();
```
下面是结果：

    object
    undefined
    number
    number
    string
    boolean
    function
    function
    object
    object
    object
    object
    object
    object
    object
    object

需要重点注意的几个是：

    null --> object
    NaN --> number

带有new操作符的除了Function之外，全部都是object。

我们按照Prototype的形式，包装一下这个过程，作为常规的过程，null和undefined这两个特别的我们先处理掉：

```javascript
(function(){
        //先定义一下类型的表示字符串
        var typeMap = {
            'number'   : 'Number',
            'boolean'  : 'Boolean',
            'string'   : 'String',
            'function' : 'Function',
            'object'   : 'Object',
            'undefined': 'Undefined',
            'null'     : 'Null'
        };
        function type(obj){
            switch(obj){                        //检测null和undefined
                case null:{
                    return typeMap['null'];
                }
                case undefined:{
                    return typeMap['undefined'];
                }
            }
            var objType = typeof obj;
            switch(objType){
                case 'number' : {
                    return typeMap['number'];
                }
                case 'boolean' : {
                    return typeMap['boolean'];
                }
                case 'string' : {
                    return typeMap['string'];
                }
                case 'function' : {
                    return typeMap['function'];
                }
                case 'object' : {
                    return typeMap['object'];
                }
            }
        }
        for(var i in varArray){
            console.log(type(varArray[i]));
        }
    })();
```
【说明：这里和Prototype里面有个不一致的地方，Prototype里面并没有用typeof来检测函数，我这里用了，注意就行】

或者上面的例子再简单一点：

```javascript
    (function(){
        function type(obj){
            return obj === null ? 'Null' :
                   obj === undefined ? 'Undefined' :
                   typeof obj === 'number'   ? 'Number':
                   typeof obj === 'boolean'  ? 'Boolean':
                   typeof obj === 'string'   ? 'String':
                   typeof obj === 'function' ? 'Function': 'Object';
        }
        for(var i in varArray){
            console.log(type(varArray[i]));
        }
    })();
```
运行结果：

    Object
    Undefined
    Number
    Number
    String
    Boolean
    Function
    Function
    Object
    Object
    Object
    Object
    Object
    Object
    Object
    Object

现在我们分离出来了“基本类型”【我这里基本类型是指的typeof可以检测出来的类型，不是指的js的基本类型，大牛不要喷我···】

接下来就是分离object那个里面的类型了。方法提供两个：

1. 转化为字符串形式
2. 检测原型

第一种方法：

先将获得对象的字符串表示形式，获得字符串形式的方法有几种：

```javascript
var obj = 'xesam';
obj = ''+obj;
obj = String(obj);
obj = obj.toString();
```
对于 alert 和 console 这样的输出方法，输出对象的时候，都调用了对象的toString()方法。按理来说，这样没什么问题，但是Date,RegExp,Array等都是重写了从Object继承过来的toString的方法的，因此到底返回什么就无法预测了。

所以要调用，必须使用最原始的Object.prototype.toString。

使用最原始的Object.prototype.toString的局限就是无法判断自定义的类，除非自定义类重写了自己的toString方法，但是重写自定义类的toString方法之后又会引起枚举（in）的问题（Object第一部分提到过），所以这个需要仔细考虑一下。

具体的实现如下：

```javascript
   (function(){
        function objectType(obj){
            obj = Object.prototype.toString.call(obj);
            return obj;
        }
        for(var i in varArray_2){
            console.log(objectType(varArray_2[i]));
        }
    })();
```
运行结果：

    [object Function]
    [object String]
    [object Number]
    [object Boolean]
    [object Object]
    [object Array]
    [object RegExp]
    [object Error]
    [object Date]

第二种方法就是调用instanceof操作符

比如：

```javascript
console.log([] instanceof Array);
```
这就是 variable instanceof constructor 的形式。

或者直接判断constructor。

具体实现：

```javascript
    (function(){
        function objectType(obj){
            obj = obj.constructor;
            return obj === Array   ? '[object Array]':
                   obj === Boolean ? '[object Boolean]':
                   obj === Date    ? '[object Date]':
                   obj === RegExp  ? '[object RegExp]':
                   obj === String  ? '[object String]':
                   obj === Function? '[object Function]':
                   obj === Error   ? '[object Error]':
                   obj === Number  ? '[object Number]':'[object Object]'
        }
        for(var i in varArray_2){
            console.log(objectType(varArray_2[i]));
        }
    })();
```
运行结果：

    [object Function]
    [object String]
    [object Number]
    [object Boolean]
    [object Object]
    [object Array]
    [object RegExp]
    [object Error]
    [object Date]

这个对于自定义的类，也可以获得相应的结果，只是稍微变通一下代码而已。
