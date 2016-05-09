---
layout: post
title:  "【Javascript】从字符串中解析出JSON"
date:   2012-01-01 10:36:04 +0800
categories: Javascript
---

JSON介绍[http://json.org/](http://json.org/)

这个解析JSON，也是Prototype源码浅析的一个铺垫。

下面是一个开篇例子，其中response是从服务器获得的JSON字符串：

```javascript
    var response_1 = "{\"user\":\"xesam\",\"info\":{\"age\":\"24\"}}";
    var response_2 = "{'user' : 'xesam'}";
    var response_3 = "console.log('xss')";

    var obj_1_1 = eval('(' + response_1 + ')');
    console.log('obj_1_1',obj_1_1);
    var obj_1_2 = eval('(' + response_2 + ')');
    console.log('obj_1_2',obj_1_2);
    var obj_1_3 = eval('(' + response_3 + ')');
    console.log('obj_1_3',obj_1_3);

    var obj_2_1 = (new Function('return ' + response_1))();
    console.log('obj_2_1',obj_2_1);
    var obj_2_2 = (new Function('return ' + response_2))();
    console.log('obj_2_2',obj_2_2);
    var obj_2_3 = (new Function('return ' + response_3))();
    console.log('obj_2_3',obj_2_3);

    var obj_3_1 = JSON.parse(response_1);
    console.log('obj_3_1',obj_3_1);
    try{
        var obj_3_2 = JSON.parse(response_2);
        console.log('obj_3_2',obj_3_2);
    }catch(e){
        console.log('obj_3_2','error');
    }
    try{
        var obj_3_3 = JSON.parse(response_3);
        console.log('obj_3_3',obj_3_3);
    }catch(e){
        console.log('obj_3_3','error');
    }
```

结果：

```javascript
obj_1_1 Object 
obj_1_2 Object
xss
obj_1_3 undefined
obj_2_1 Object
obj_2_2 Object
xss
obj_2_3 undefined
obj_3_1 Object
obj_3_2 error
obj_3_3 error
```

可见，对于浏览器自带的标准JSON解析器来说，response_2和response_3是非法的。因此，我们可以更进一步的了解到JSON的几点主要的地方。

第一、对于key/value的形式，每一个key都需要有引号（这个和javascript原生对象可有可无的引号不同），需要是字符串（这种字符串形式上更类似于C语言里面的字符串，必须是双引号，这个和javascript原生对象引号可以使双引号也可以是单引号不同）。

![1](http://json.org/string.gif)

上面的图示是对JSON中string的要求

第二、JSON本来就是一种交换数据的格式，因此，里面是不应该包含需要执行的javascript代码的。

所以，只有严格符合标准的JSON字符串形式，才能通过JSON.parse的解析。

对于大部分现代浏览器而言，window.JSON 是一个内置的对象，但是对于IE6/7来说，这个对象是缺失的，所以，需要借助例子中的前两种形式eval和new Function。

平常而言，eval用的比较多，但是eval够强大，所以够危险。

response_2 被解析成对象是eval本身的功能，跟JSON无关。如果服务器返回的是类似response_2的形式，八成是一开始的传值就有问题，我就犯过这种错误。不过如果是服务端生成的，一般倒不会有什么问题。

response_3 被解析成可执行代码页是eval本身的功能，是危险的来源，不过好像平时也没怎么注意。

不过，对于IE6/7来说，要从字符串中解析出来JSON对象，又必须借助于eval（依稀听说新的ECMAScript标准抛弃了eval？不过这跟IE6/7半毛钱的关系都没有）。

因此，这一部分可以参考JSON.js的String.prototype.parseJSON

对于

```javascript
var response_1 = "{\"user\":\"xesam\",\"info\":{\"age\":\"24\"}}";
```

这段，String.prototype.parseJSON的转换流程如下：

第一，先检测待转换字符串的合法性

第二，eval字符串

所以response_1的解析情况大致如下：

```javascript
    (function(){
        var responseTemp = response_1.replace(/\\./g, '@').replace(/"[^"\\\n\r]*"/g, '');
        var correct = /^[,:{}\[\]0-9.\-+Eaeflnr-u \n\r\t]*$/.test(responseTemp);
        if(correct){
            var j = eval('(' + response_1+ ')');
            return j;
        }
        throw new SyntaxError('parseJSON');
    })()
```

```javascript
replace(/\\./g, '@')
```
先把一些转义字符替换掉，那个“@”并没有什么特殊意思，至于为什么@，估计是因为正则里面没有这个元字符，所以避免冲突，想换做其他的，应该也可以。

```javascript
replace(/"[^"\\\n\r]*"/g, '')
```
这一步替换掉了所有引号包含的内容，于是，字符串中剩下的部分就是除去string外可以存在的字符。

看这个，

```javascript
/^[,:{}\[\]0-9.\-+Eaeflnr-u \n\r\t]*$/
```
其实好理解，JSON的value值可以是string，object，array，number，false，true，null等7种，需要引号包含string的内容都处理掉了，所以除了这些，JSON格式还有

    {}表示对象结构，对应,:{}
    []表示数组结构，对应\[\]
    0-9 . E e表示数字类型，对应0-9.\-+Ee
    true 和 false 对应aflsrtu
    null 对应n
    其他一些特殊字符对应 \n\r\t
    
这些组合起来就是上面的一段正则。

下面是完整的JSON.js的源码，无非是添加了一个递归而已，从而可以安全的解析整个嵌套的部分。

```javascript
    (function(s){
        s.parseJSON = function (filter) {
          var j;
          function walk(k, v) {
            var i;
            if (v && typeof v === 'object') {
              for (i in v) {
                if (Object.prototype.hasOwnProperty.apply(v, [i])) {
                  v[i] = walk(i, v[i]);
                }
              }
            }
            return filter(k, v);
          }
          if (/^[,:{}\[\]0-9.\-+Eaeflnr-u \n\r\t]*$/.test(this.replace(/\\./g, '@').replace(/"[^"\\\n\r]*"/g, ''))) {
            j = eval('(' + this + ')');
            return typeof filter === 'function' ? walk('', j) : j;
          }
          throw new SyntaxError('parseJSON');
        };
    })(String.prototype);
```