---
layout: post
title:  "【Javascript】Prototype源码浅析—Number部分"
date:   2012-01-14 11:46:04 +0800
categories: Javascript
---
Prototype在原生对象的基础上扩展，分别是 Object，Function，String，Number，Array，Date，前面分析了 Object，Function，String，还剩下Number，Array，Date。
  
Number部分方法比较少，一共有8个：
  
    toColorPart: 将 Number 对象转换为具有两位数字的十六进制形式
    succ:  返回当前 Number 对象的下一个值，即当前值加一         
    times: 采用 Ruby 的风格来封装一个标准的 [0...n] 循环
    toPaddedString:将当前 Number 对象转换为字符串，如果转换后的字符串长度小于 length 指定的值，则用 0 在左边补足其余的位数 
    abs:   返回当前 Number 对象的绝对值。        
    round: 返回当前 Number 对象四舍五入后的整数值。
    ceil:  返回大于等于当前 Number 对象的最小整数值。
    floor: 返回小于等于当前 Number 对象的最大整数值。
  
其中一个重要的方法是toPaddedString。Number对象重写了toString方法：

```javascript  
  NumberObject.toString(radix)
```
radix	可选。规定表示数字的基数，使 2 ~ 36 之间的整数。若省略该参数，则使用基数 10。但是要注意，如果该参数是 10 以外的其他值，则 ECMAScript 标准允许实现返回任意值。
  
```javascript
    function toPaddedString(length,radix){
        var string = this.toString(radix || 10);//先将数字转换成相应的进制
        return '0'.times(length - string.length) + string;//times方法在String中扩展的，将一个字符重复n遍
    }
```
有了这个方法，就有一个比较有用的延伸就是toColorPart，可用于CSS中的颜色转换：
  
```javascript
    function toColorPart() {
        return this.toPaddedString(2, 16);
    }
```
既然是CSS颜色转换，因此数字就要求在[0-255]范围内。
  
```javascript
    console.log((10).toColorPart());//0a
```
有一个和String中同名的方法succ，作用也差不多，String中是按照字符表来递加的，Number中是按照自然数的顺序来的。
  
```javascript
    function succ() {
        return this + 1;
    }
    console.log((10).succ());//11
```
从这个方法出发，来一个简单的0-n的数组
  
```javascript
    function range(){
        var ret = [0];
        for(var i = 0; i < this - 1; i++){
            ret.push(i.succ());
        }
        return ret;
    }
    console.log((10).range());//[0, 1, 2, 3, 4, 5, 6, 7, 8, 9]
```
暂时用这个range函数来得到times函数：

```javascript  
    function times(iterator, context){
        this.range().forEach(iterator, context);//源码中使用的是R()方法
        return this;
    }
    var s = '';
    (5).times(function(item){
        s += item;
    });
    console.log(s);//01234
```  
  
除去上面几个方法，其他的方法就是将Math的静态方法扩展到Number对象上【说法不准确，意会··=。=】

```javascript
    function abs() {
        return Math.abs(this);
    }
    function round() {
        return Math.round(this);
    }
    function ceil() {
        return Math.ceil(this);
    }
    function floor() {
        return Math.floor(this);
    }
```