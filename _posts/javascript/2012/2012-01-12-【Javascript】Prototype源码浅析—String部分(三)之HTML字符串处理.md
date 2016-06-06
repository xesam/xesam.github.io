---
layout: post
title:  "【Javascript】Prototype源码浅析—String部分(三)之HTML字符串处理"
date:   2012-01-13 11:36:04 +0800
categories: javascript
tag: [javascript]
---

    HTML处理	stripTags    |  escapeHTML      |  unescapeHTML 	 
    JSON处理	unfilterJSON |  isJSON          |  evalJSON     |  parseJSON
    脚本处理	stripScripts |  extractScripts  |  evalScripts

现在，String部分转入具体的关联应用，分别对应 HTML字符串，JSON字符串和HTML中的脚本字符串。

【乱入一句，有关JSON的一点东西，可以看看[http://www.cnblogs.com/TomXu/archive/2012/01/11/2311956.html](http://www.cnblogs.com/TomXu/archive/2012/01/11/2311956.html)】

下面分别叙述：

### 一、HTML字符串 

    stripTags  ：移除字符串中所有的 HTML 标签。
    escapeHTML ： 将 HTML 特殊字符转换为它们的等价实体。（&对应&amp; <对应&lt; >对应&gt; ）
    unescapeHTML ：移除字符串中的标签，并将用实体表示的 HTML 特殊字符转换为它们的正常形式。（escapeHTML 的逆操作）


stripTags  中的一段正则
    
    /<\w+(\s+("[^"]*"|'[^']*'|[^>])+)?>|<\/\w+>/gi
    
用来匹配标签中的内容，注意不能换行，不过换行的话就有语法错误了。

【这个方法唯一需要注意的位置是，stripTags会移除<script>标签，但是不会移除里面的内容，所以可能将<script>里面的内容暴露出来，影响页面结构】


### 二、脚本字符串

    stripScripts ： 移除字符串中所有的 HTML script 块。弥补stripTags方法对script标签的缺陷
    extractScripts ：提取出字符串中包含的所有 script 的内容，并将之返回作为一个字符串数组。
    evalScripts ：执行字符串中包含的所有 script 块的内容。返回一个数组，该数组包含每个 script 执行后返回的值。  

stripScripts中的正则是对stripTags中一个正则的发展

```javascript
    function stripScripts() {
        var pattern = new RegExp('<script[^>]*>([\\S\\s]*?)<\/script>', 'img');//i忽略大小写，m换行，g全局
        return this.replace(pattern , '');
    }
 

    function extractScripts() {
        var matchAll = new RegExp('<script[^>]*>([\\S\\s]*?)<\/script>', 'img'),
        matchOne = new RegExp('<script[^>]*>([\\S\\s]*?)<\/script>', 'im');
        return (this.match(matchAll) || []).map(function(scriptTag) { 
            return (scriptTag.match(matchOne) || ['', ''])[1];
        });
    }
```
map是对数组的一个扩展，某些浏览器有这个原生方法，参见《chrome原生方法之数组》
最后获得的是一个所有script标签内部内容的一个数组，因此evalScripts 的做法就很自然的可以想出来——循环遍历获得的数组，然后依次执行（eval），存储每一项执行的结果。

```javascript
    function evalScripts() {
        return this.extractScripts().map(function(script) { return eval(script) });
    }
```

### 三、JSON处理

    unfilterJSON：移除 Ajax JSON 或 JavaScript 响应内容周围的安全注释界定符。
    isJSON：使用正则表达式检测字符串是否是合法的 JSON 格式
    evalJSON：执行一个 JSON 格式的字符串，并返回结果对象

其中isJSON和evalJSON就是JSON.js中的parseJSON，而且代码也差不多，参见《从字符串中解析出JSON》

顺便说一点unfilterJSON中的安全注释界定符，这是一种安全机制，对于自家的数据，可以在返回值两端加上特殊的字符（界定符）来表明数据的来源，客户端解析的时候用unfilterJSON来处理掉添加的界定符，借此可以在一定程度上减少一些XSS的攻击。

Prototype中默认的形式是：

```javascript
'/*-secure-\n{"name": "小西山子","age": 24}\n*/'
```

其中界定符号是 /*-secure-\n'和'\n*/'


