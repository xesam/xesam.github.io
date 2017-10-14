---
layout: post
title:  "【Javascript】Prototype源码浅析—String部分(一)有关indexOf优化"
date:   2012-01-10 11:36:04 +0800
categories: javascript
tag: [javascript]
---

添加到String.prototype中的方法比较多，不过归结起来，大致分为下面几类：

    原始能力增强 strip |  include  |  startsWith  |  endsWith |  empty |  blank
    格式	camelize | capitalize |  underscore |  dasherize  | inspect          
    变形	toArray |  succ  | times
    替换	interpolate  | sub |  scan |  truncate | gsub
    HTML处理	stripTags  | escapeHTML |  unescapeHTML
    参数序列化	toQueryParams
    JSON处理	unfilterJSON |  isJSON |  evalJSON |  parseJSON
    脚本处理	stripScripts |  extractScripts  | evalScripts

（我自己分的，不妥之处请指出）

从基本的原始能力增强开始，下面是具体的实现，这一段很好理解的：

```javascript   
    (function(s){
        function strip(){
            return this.replace(/^\s+/,'').replace(/\s+$/,'');
        }
        function include(pattern){
            return this.indexOf(pattern) > -1;//split
        }
        function startsWith(pattern) {
            return this.lastIndexOf(pattern, 0) === 0;
        }
        function endsWith(pattern) {
            var d = this.length - pattern.length;
            return d >= 0 && this.indexOf(pattern, d) === d; 
        }
        function empty() {
            return this == '';
        }
        function blank() {
            return /^\s*$/.test(this);
        }
        s.strip = String.prototype.trim || strip;
        s.include = include;
        s.startsWith = startsWith;
        s.endsWith = endsWith;
        s.empty = empty;
        s.blank = blank;
    })(String.prototype);
```
上面的strip在jquery里面是$.trim,而且大部分貌似都是trim。这里直接扩展原生原型的悲剧之处就显现出来了，因为后面的JS实现中(比如chrome)就实现了trim方法，那就弄巧成拙了。

```javascript
    function strip(){
        return this.replace(/^\s+/,'').replace(/\s+$/,'');
    }
```
这里面的 replace(/^\s+/,'') 就是 trimLeft，replace(/\s+$/,'') 是 trimRight，不过 Prototype.String 中没有这两个方法。

下面是这一部分比较有意思的地方：

当时看这段的时候，对其中的startsWith和endsWith甚是不解，按理来说，startsWith用indexOf就可以了，这里却是用的lastIndexOf。后来去翻了一下Prototype1.6版本的实现：

```javascript
    function startsWith(pattern) {
        return this.indexOf(pattern) === 0;
    }
    
    function endsWith(pattern) {
        var d = this.length - pattern.length;
        return d >= 0 && this.lastIndexOf(pattern) === d;
    }
```
可见，以前版本中startsWith用的就是indexOf，不过1.7版本修改了startsWith的实现。在1.7版本中：

    startsWith 实现中lastIndexOf从后向前查找，不过起点（fromindex）设置为0，因此，只需要检测开头一次就可以了。
    endsWith 实现中indexOf从前向后查找，由于字符串长度不定，因此这里计算了一下长度，然后再确定了起点（fromindex），因此也只需要检测结尾一次就可以了。

这里的性能优化之处在于，1.6的实现中，如果开头没有匹配（就是startsWith不成立），但是indexOf依旧会向后查找，直到找到一个匹配的或者字符串结尾，这样就浪费了。
举个例子，对于下面的一个操作：

```javascript
'abcdefgabcdefg'.startsWith('abc')
```

在1.6版本和1.7版本的实现中，没有任何区别，但是我们转换一下：

```javascript
'abcdefgabcdefg'.startsWith('xesam')
```
在1.6实现中，startsWith内部的 indexOf 操作会在开头的 a 没有和 x 匹配后，虽然没有必要再继续了，但是 indexOf 依旧会继续向后查找，直到找到匹配的‘xesam’或者字符串末尾。

在1.7实现中，startsWith内部的lastIndexOf是反向查找的（fromIndex=0），因此在开头的a没有和x匹配后，操作就停止了，因为lastIndexOf已经到头了。

这么一对比，如果待检测的字符串非常长的话，两种实现方式的效率会有明显的区别。

endsWith的原理也是一样的。


