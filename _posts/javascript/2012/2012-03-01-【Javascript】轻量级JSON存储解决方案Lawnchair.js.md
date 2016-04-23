---
layout: post
title:  "【Javascript】轻量级JSON存储解决方案Lawnchair.js"
date:   2012-03-01 10:46:04 +0800
categories: Javascript
---

## Lawnchair

Lawnchair是一个轻量级的移动应用程序数据持久化存储方案，同时也是客户端JSON文档存储方法，优点是短小，语法简洁，扩展性比较好。

现在做HTML5移动应用除了LocalStorage的兼容性比较好之外，SQL web database以及IndexedDB都处在僵局中，虽然有人叫嚣着“我们应该干掉 LocalStorage API”，但那是后话，现在也没得选择。

Lawnchair有个曾经的官网：[http://westcoastlogic.com/lawnchair/](http://westcoastlogic.com/lawnchair/)，不过这个站点提供的源码版本过时了，而且还有错误。

需要下载的话，最新版本在 [https://github.com/brianleroux/lawnchair](https://github.com/brianleroux/lawnchair)

应用示例【应用的是dom Storage】：

```javascript
    var store = new Lawnchair({name:'testing'}, function(store) {
    // 需要保存的对象
    var me = {key:'brian'};
    // 保存
    store.save(me);

    store.get('brian', function(me) {
        console.log(me);
    });
});
```
或者：

```javascript
    var store = Lawnchair({name:'testing'}, function(store) {
    // 需要保存的对象
    var me = {key:'brian'};
    // 保存
    store.save(me);

    store.get('brian', function(me) {
        console.log(me);
    });
});
```
因为使用了安全的构造函数，因此两种方法的效果一致。回调函数的第一个参数与返回的的store是同一个对象，在回调函数内部也可以用this代替。

初始化：

```javascript
var store = new Lawnchair(option,callback);
```
option默认为空对象，有三个可选属性：

```javascript
option = {
    name://相当于表名
    record://
    adapter://存储类型
}
```
callback的第一个参数是当前对象，在回调函数内部也可以用this代替。

## API

    keys (callback) //返回存储对象的所有keys
    save (obj, callback)//保存一个对象
    batch(array, callback)//保存一组对象
    get (key|array, callback)//获取一个或者一组对象，然后调用callback处理
    exists (key, callback)//检查是否存在key，并将结果的布尔值（true/false）传递给callback函数
    each(callback)//遍历集合，将（对象，对象索引）传递给callback函数
    all (callback)//将所有对象放在一个数组返回
    remove (key|array, callback)//移除一个或者一组元素。
    nuke (callback)//销毁所有
    
初始化：

```javascript
    var store = new Lawnchair({name:'test'}, function() {});
```

或者

```javascript
    var store = new Lawnchair(function() {});
```

参数中必须有一个函数作为回调函数，哪怕是空。

```javascript
    save (obj, callback)//保存一个对象
    var store = Lawnchair({name:'table'}, function(store) {
    });
    store.save({
        key:'hust',
        name:'xesam_1'
    })
    store.save({
        key:'whu',
        name:'xesam_2'
    })
```

创建 Lawnchair 对象的时候，如果传入的 option 参数含有 name 属性，那么会创建一个类似 table._index_的数组用来保存索引值。

保存形式为对象，如果传入的对象有key属性，那么key会作为索引值保存，如果没有key属性，则自动生成一个key值，然后保存在table._index_中，上面的例子的操作结果如下图：

![1]({{ site.baseurl }}/image/Lawnchair_1.jpg)

batch(array, callback)//保存一组对象

上面的例子改用batch方法就是：

```javascript
    var store = Lawnchair({name:'table'}, function(store) {
    });
    store.batch([{
        key:'hust',
        name:'xesam_1'
    },{
        key:'whu',
        name:'xesam_2'
    }])
```

exists (key, callback)//检查是否存在key，并将结果的布尔值（true/false）传递给callback函数

```javascript
    store.exists('whu',function(result){
        console.log(result);//true
    })
    store.exists('test',function(result){
        console.log(result);//false
    })
```
get (key|array, callback)//获取一个或者一组对象，然后调用callback处理

```javascript
    store.get('hust',function(result){
        console.log(result);//{key:'hust',name:'xesam_1'}
    })
```
all (callback)//将所有对象放在一个数组返回

```javascript
    store.all(function(result){
        console.log(result);//[{key:'hust',name:'xesam_1'},{key:'whu',name:'xesam_2'}]
    })
```
each(callback)//遍历集合，将（对象，对象索引）传递给callback函数

```javascript
    store.each(function(result){
        console.log(result);
        //{key:'hust',name:'xesam_1'}
        // {key:'whu',name:'xesam_2'}
    })
```
remove (key|array, callback)//移除一个或者一组元素。

```javascript
    store.remove('whu',function(){
        store.all(function(result){
            console.log(result)//[{key:'hust',name:'xesam_1'}]
        });
    })
```
nuke (callback)//销毁所有

```javascript
    store.nuke(function(){
        store.all(function(result){
            console.log(result)//[]
        });
    })
```
keys (callback) //返回存储对象的所有keys

```javascript
    store.keys(function(result){
        console.log(result)//['hust','whu']
    })
```

lawnchair.js的核心很小，然后有完善的扩展和插件机制，可以按需加载。
自己编写也比较方便，只需要在自己的代码中实现

    adapter 
    valid 
    init 
    keys 
    save 
    batch 
    get 
    exists 
    all 
    remove 
    nuke

方法即可。
