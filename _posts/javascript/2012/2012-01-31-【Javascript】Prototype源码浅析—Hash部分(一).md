---
layout: post
title:  "【Javascript】Prototype源码浅析—Hash部分(一)"
date:   2012-01-31 11:46:04 +0800
categories: javascript
tag: [javascript]
---
## Hash

Hash是Prototype作者扩展出来的一个数据类型。
本质上他就是一个普通的javascript对象（注：不要纠结什么javascript变量都是对象，这里说new Object()那种），然后在这个对象上面扩展出来一些其他的方法。

## 基本原理

基本的原理的代码说明就是：

```javascript
    function Hash(object){
        this._object = object;
    }
    Hash.prototype = {
        constructor : Hash,
        method_1 : function(){//this._object},
        method_2 : function(){//this._object}
        //...
    }
    var hash_1 = new Hash({name : 'xesam'});
```
不过在源码中肯定不是这样的咯，创建类的形式就不是这样，因此我们换成Paototype中创建类的形式（注：Prototype源码浅析——Class部分(一)之类）：

```javascript
var Hash = Class.create(Enumerable, (function() {
        function initialize() {
            //this._object
        }
        return {
            initialize : initialize
        }
    })())
```
Hash里面也混入了Enumerable对象，借此给Hash增加更多的方法。

（在这里我们有个区别可以留意一下：尽管Hash和Array都混入了Enumerable，但是与Array不同的是，Array是js原生的一个数据类型，只能用extend的方式，Hash是作者自己创建的一个数据类型，因此,Hash采用的方式是Class.create的方式。）

既然混入了Enumerable对象，那么肯定有一个_each方法，对于Hash对象，_each方法的iterator参数的参数是一个pair，这个pair比较特别一点
既是一个数组[key,pair]，也是一个对象：

```javascript
    {
        key   : key,
        value : value
    }
```
因此pair[0]和pair.key的结果是一致的。

基本操作：

看下创建类时的initialize方法，每一个hash对象内部都维护着一个内部的对象，变量名叫做_object，因此原则上不能通过直接操作实例的属性来读取或者设置实例的属性。所以作者提供了单独的方法，现在有三个基本的方法：get,set,unset。

```javascript
  function set(key, value) {
    return this._object[key] = value;
  }

  function get(key) {
    if (this._object[key] !== Object.prototype[key])
      return this._object[key];
  }

  function unset(key) {
    var value = this._object[key];
    delete this._object[key];
    return value;
  }
```
（注：Prototype的类很基础，封装基本没有，因此虽然内部维护了一个_object变量，但是并不是真正意义上的私有变量，访问hash的某个属性可以用上面的get,set,unset，也可以直接修改_object对象：


```javascript
hash.set('name','new name')

hash._object.name = 'new name'
```
上面操作没区别，靠自觉而已。）


复制hash：

第一：
克隆当前hash对象(hash)——clone。克隆内部的对象（_object）——toObject.

toObject调用的是Object.clone方法，现在回顾一个下Object.clone方法

```javascript
    function clone(object) {
        return extend({ }, object);
    }
```
就是把this._object复制到一个空对象里面，然后返回。

```javascript
    function clone() {
      return new Hash(this);
    }
```
现在看一看创建Hash类的时候的initialize函数，先前忽略了this._object的初始化过程：

```javascript
    function initialize(object) {
        this._object = Object.isHash(object) ? object.toObject() : Object.clone(object);
    }
```
看看实现：如果object是一个普通对象，那么直接调用Object.clone方法。如果object是一个Hash实例，那么调用object.toObject，注意object.toObject的本质。间接调用的还是Object.clone方法，不过最终返回的类型是Hash类型，享有Hash的各种方法。

取得Hash对象的keys和values数组

方法名就是keys和values。这里使用的是父对象的一个方法——plunk（注：plunk是Enumerable中定义的一个方法Prototype源码浅析——Enumerable部分(三)）：

```javascript
  function keys() {
    return this.pluck('key');
  }

  function values() {
    return this.pluck('value');
  }
```
与plunk关系最密切的一个方法是each，回去看下each，each函数的iterator的参数是pair，是一个对象。

更新（合并）一个Hash实例：

这样的操作有两种：

    一种是破坏性的update（会修改原始对象）
    一种是非破坏性的merge（不会修改原始对象的）

update使用的是inject方法（注：Prototype源码浅析——Enumerable部分(三)），第一个参数是this（当前Hash实例），因此当前对象会被修改。

merge使用的也是update方法，不过先执行了一次clone操作，因此原始的Hash实例被保留下来了。

```javascript
  function merge(object) {
    return this.clone().update(object);//先拷贝了内部变量_object
  }

  function update(object) {
    return new Hash(object).inject(this, function(result, pair) {
      result.set(pair.key, pair.value);
      return result;
    });
  }
```

格式转换：

toQueryPair 和 toQueryString

toQueryPair是一个内部使用的方法，主要作用是检测value的值。如果value没为undefined，那么只保留key值，如果value值为null，那么保留“key=”形式否则转换为key=encodeURIComponent(value)的形式。

```javascript
  function toQueryPair(key, value) {
    if (Object.isUndefined(value)) return key;
    return key + '=' + encodeURIComponent(String.interpret(value));
  }
```
toQueryString主要涉及到一个处理values是数组的情况，values为数组就使用concat展开，values为字符串就直接push，然后再展开。

这里和Object.toQueryString方法是一样的，应该是可以相互代替的。
这里回头去看Object里面的Str方法，那个清楚了，这个就不在话下了（注：Prototype源码浅析——Object部分(三)之有关JSON）。

inspect就没什么好说的了。很常见了。
