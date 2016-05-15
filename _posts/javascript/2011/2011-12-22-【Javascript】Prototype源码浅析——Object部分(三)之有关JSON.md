---
layout: post
title:  "2011-12-22-【Javascript】Prototype源码浅析——Object部分(三)之有关JSON"
date:   2011-12-22 08:36:04 +0800
categories: Javascript
---
对JSON的操作主要是解析JSON字符串为一个对象和将一个对象转换成JSON字符串。

网上搜一下JSON解析，就会发现一堆文章和方法，当然这篇文章主要不是讨论JSON的解析，不过也可以大致回顾一下：

1. eval。eval('(' + jsonStr + ')');加个括号是为了强制表达式运算，不然直接eval('{}'),具体原因可以去翻看一下《JS语言精髓与编程实践》
2. Function
3. 另外有一个JSON解析的库，这个可以自己去下载
4. 除了IE6,7之外，现代浏览器基本都内置了JSON解析器

【说明，prototype本身也实现了一个evalJSON方法，不过也脱离不了上面几种情况】

实例如下（没有用JSON解析库）：

```javascript
    (function(){
        var obj = "{\"name\":\"xesam\"}";
        console.log('eval:',eval('(' + obj + ')'));
        console.log('Function',(new Function('return' + obj))());
        console.log('JSON:',JSON.parse(obj));
    })();
    //结果：{name:'xesam'}
```

现在将上面的过程反过来，将一个对象编码为一个JSON字符串。同样，如果浏览器带有原生的JSON方法，有一个与parse对应的方法stringify

```javascript
    (function(){
        var obj = {name:'xesam'};
        console.log('obj:',JSON.stringify(obj));//'{"name":"xesam"}'
    })();
```
这种操作就不像解析那样有那么多方法，因此需要自己来写。

写之前，先来探讨一下目标对象可能出现的情况,然后把它转换成字符串的形式。

```javascript
    var object_1 = null;
    var object_2 = undefined;
    var object_3 = 12;
    var object_4 = '12';
    var object_5 = true;
    var object_6 = [1,2,3];
    var object_7 = {name :'xesam'};
    var object_8 = {name : function(){}};
```
先硬性规定一下，null、undefined、true、false返回对应的'null'、'undefined'、'true'、'false'。数字直接量和字符串直接量返回对应的数值。

下面主要是区分出Array类型和Function，主要操作就是遍历每一项，碰到数组或者一般对象就依次展开，所以可以得到一个初始的版本：

```javascript
    (function(){
        function object2Str(object){
            if(arguments.length != 0 && typeof object == 'undefined'){
                return 'undefined';
            }
            switch (object) {
                case null : return 'null';
                case true : return 'true';
                case false: return 'false';
            }
            var type = Object.prototype.toString.call(object);
            switch(type){
                case '[object Number]' : return String(object);
                case '[object String]' : return String(object);
                case '[object Array]'  : {
                    var ret = [];
                    for(var i = 0,len = object.length; i < len; i++){
                        ret.push(object2Str(object[i]));
                    }
                    return '[' + ret.join(',') + ']';
                }
                case '[object Object]' :{
                    var ret = [];
                    for(var key in object){
                        if(object.hasOwnProperty(key)){
                            if(typeof object2Str(object[key]) != 'undefined'){
                                ret.push(String(key) + ':' + object2Str(object[key]));
                            }
                        }
                    }
                    return '{' + ret.join(',') + '}';
                }
            }
        }
        console.log(object2Str(null));
        console.log(object2Str(undefined));
        console.log(object2Str(true));
        console.log(object2Str(12));
        console.log(object2Str('34'));
        console.log(object2Str({name : function(){}}));
        var object = [1,2,3,4,[5,6,7,8,9],6];
        console.log(object2Str(object));
        var object = {
            name:'xesam',
            age : 24,
            books:{
                key_1 : 'book_1',
                key_2 : 'book_2'
            }
        };
        console.log(object2Str(object));
    })();
```
看这个实现，{name:function(){}} 这个并没有显式的提到，因为在默认情况下 

```javascript
if(typeof object2Str(object[key]) != 'undefined')
```
这一步就被处理了。

基本的框架得到了，我们的实现中还包括了 undefined 的处理，Prototype 的实现中并没有这一步，需要注意。

下面要做的就是一些修缮工作，继续补充：

在上面的例子中，我们忽略了 

```javascript
var number_1 = 12 
```
与 

```javascript
var number_2 = new Number(12)
```
的区别，我们先填补这两者之间的区别。

于是在处理每一个值之前先直接调用valueOf获得变量的原始值。于是上面的例子变为：

```javascript
    (function(){
        function object2Str(object){
            if(arguments.length != 0 && typeof object == 'undefined'){
                return 'undefined';
            }
            var type = Object.prototype.toString.call(object);
            switch (type) {
                case '[object Number]' :
                case '[object String]' :
                case '[object Boolean]':
                    object = object.valueOf();
            }
            switch (object) {
                case null : return 'null';
                case true : return 'true';
                case false: return 'false';
            }
            type = typeof object;
            switch(type){
                case 'number'  : return String(object);
                case 'string'  : return String(object);
                case 'object'  : {
                    var ret = [];
                    if(Object.prototype.toString.call(object) == '[object Array]'){
                        for(var i = 0,len = object.length; i < len; i++){
                            ret.push(object2Str(object[i]));
                        }
                        return '[' + ret.join(',') + ']';
                    }else if(Object.prototype.toString.call(object) == '[object Function]'){
                        return '{}';
                    }else{
                        for(var key in object){
                            if(object.hasOwnProperty(key)){
                                if(typeof object2Str(object[key]) != 'undefined'){
                                    ret.push(String(key) + ':' + object2Str(object[key]));
                                }
                            }
                        }
                        return '{' + ret.join(',') + '}';
                    }
                }
            }
        }
        console.log(object2Str(null));
        console.log(object2Str(undefined));
        console.log(object2Str(true));
        console.log(object2Str(12));
        console.log(object2Str('34'));
        console.log(object2Str({name : function(){}}));
        var object = [1,2,3,4,[5,6,7,8,9],6];
        console.log(object2Str(object));
        var object = {
            name:'xesam',
            age : 24,
            books:{
                key_1 : 'book_1',
                key_2 : 'book_2'
            }
        };
        console.log(object2Str(object));
    })();
```

【说明：上面的实现中并未转义",/,\和还有一些控制符在Prototype中，调用的是string.inspect这个方法来实现的，不过这一部分在后面的String部分，所以暂且这么实现，了解即可】

现在回到Prototype中，在Prototype里面，相似的方法叫做Str【这个函数是大写开头，说明是一个局部函数，另一个大写开头的是Type，这两个方法并未对外公开】

对比 object2Str 和 Str，除了上面说的特殊字符转义之外，Str的实现还多了两个参数就是key和stack。

这个 stack 的作用是什么呢？为了避免循环使用导致栈溢出。

比如我有一个对象：

```javascript
var obj = {name : this}。
```

去调用Prototype里面的Str方法，就会报错（typeError），如果直接调用object2Str就会报栈溢出。所以这是一个必要的检测。

所以我们仿写最终的版本是：

```javascript
    (function(){
        function object2Str(object,stack){
            stack = stack || [];
            if(arguments.length != 0 && typeof object == 'undefined'){
                return 'undefined';
            }
            var type = Object.prototype.toString.call(object);
            switch (type) {
                case '[object Number]' :
                case '[object String]' :
                case '[object Boolean]':
                    object = object.valueOf();
            }
            switch (object) {
                case null : return 'null';
                case true : return 'true';
                case false: return 'false';
            }
            type = typeof object;
            switch(type){
                case 'number'  : return String(object);
                case 'string'  : return String(object);
                case 'object'  : {
                    for (var i = 0, length = stack.length; i < length; i++) {
                        if (stack[i] === object){
                            console.log('error');
                            throw new TypeError();
                        }
                    }
                    stack.push(object);

                    var ret = [];
                    if(Object.prototype.toString.call(object) == '[object Array]'){
                        for(var i = 0,len = object.length; i < len; i++){
                            ret.push(object2Str(object[i]));
                        }
                        ret = '[' + ret.join(',') + ']';
                    }else{
                        for(var key in object){
                            if(object.hasOwnProperty(key)){
                                if(typeof object2Str(object[key],stack) != 'undefined'){
                                    ret.push(String(key) + ':' + object2Str(object[key],stack));
                                }
                            }
                        }
                        ret ='{' + ret.join(',') + '}';
                    }
                    stack.pop();
                    return ret;
                }
            }
        }
        console.log(object2Str(null));
        console.log(object2Str(undefined));
        console.log(object2Str(true));
        console.log(object2Str(12));
        console.log(object2Str('34'));
        console.log(object2Str({name : function(){}}));
        var object = [1,2,3,4,[5,6,7,8,9],6];
        console.log(object2Str(object));
        var object = {
            name:'xesam',
            age : 24,
            books:{
                key_1 : 'book_1',
                key_2 : 'book_2'
            }
        };
        console.log(object2Str(object));
        var object = {
            name : this
        }
        console.log(object2Str(object));
    })();
```

另外，在Object中，Str是为toJSON来服务的，因此这个调用方法也是特别处理了的，其参数形式是Str(key, holder, stack)

由于在Prototype的Object中是实现了一个keys方法和一个values方法，所以在类似下面的代码中

```javascript
    for(var key in object){
        if(object.hasOwnProperty(key)){
            if(typeof object2Str(object[key]) != 'undefined'){
                ret.push(String(key) + ':' + object2Str(object[key]));
            }
        }
    }
```
直接使用了keys函数，Prototype中的 具体实现是：

```javascript
    var keys = Object.keys(value);
    for (var i = 0, length = keys.length; i < length; i++) {
        var key = keys[i], str = Str(key, value, stack);
        if (typeof str !== "undefined") {
            partial.push(key.inspect(true)+ ':' + str);
        }
    }
```
所以这么一来，toJSON的调用形式也变成了：

```javascript
    function toJSON(value) {
        return Str('', { '': value }, []);
    }
```
如果按照我们在例子中的写法，可以直接是

```javascript
    function toJSON(value) {
        return object2Str(value, []);
    }
```

说完Str，另一个用的多的就是inspect方法，顾名思义啊·检查作用，可以用来调试。

一个最简单的实现：

```javascript
    (function(){
        function inspect(object){
            return object.toString();
        }
    })();
```
null和undefined没有toString方法，这里顺便说明一下，typeof null == 'object'，但是null又没有toString方法，因此不能人为null是一个简单的object

所以这个讨论在前面已经讨论过了，一次跳过。其他就是一些检测，优化的机制。就不算重点了。

至于keys（values）两个方法是很简单的，就是抄袭python，遍历一个对象的key（value），然后装到一个数组里返回。

【toHTML,isHash,toQueryString】的具体实现跟后面关联比较紧，因此在这里就暂时不说。
