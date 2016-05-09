---
layout: post
title:  "【Javascript】有关IE版本检测"
date:   2012-01-01 08:36:04 +0800
categories: Javascript
---
PS：检测浏览器虽然不是一个什么好的做法，但是有时候还是很必要的。

见得最多的就是检测navigator.userAgent(这个可以面向所有浏览器，略过)。

另外一种就是IE的条件注释，这篇有个比较详细的说明

[http://www.cnblogs.com/JustinYoung/archive/2009/03/02/ie-jiaojianzhushi.html](http://www.cnblogs.com/JustinYoung/archive/2009/03/02/ie-jiaojianzhushi.html)，注意看它下面的回复

```html
<!--[if !IE]><!-->
<script type="text/javascript">
 alert('非IE')
</ script>
<!--<![endif]-->
```

我测试的结果是这种形式是可用的。唯一需要注意的是<!-- [if IE 8]> 中'IE'和'8'中间的这个空白符是必须的，掉了就悲剧了。

基于IE的条件注释，变种版本就有几种，

第一、类似下面的形式：

```javascript
    <!--[if IE 6]>
    <input type="hidden" id="ieVersion" value="6" />
    <![endif]-->
    <!--[if IE 7]>
    <input type="hidden" id="ieVersion" value="7" />
    <![endif]-->
var ieVersion = (function(){ return document.getElementById('ieVersion')})();
```
以此类推，可以获得各个版本的信息，甚至可以添加gt，gte等，从而一次判定一类版本。

关于这种写法，有个例子就是：

```javascript
    <!--[if IE 6]>
    <html class="ie6">
    <![endif]-->
    <!--[if IE 7]>
    <html class="ie7">
    <![endif]-->    
<!--[if !IE]><!-->
    <html><!--<![endif]-->
```
于是在CSS里面就可以不用别的hack了,从而避免在IE里面多加载一次CSS，

直接

```css
.ie6 xx{}

.ie7 xx{}

.ie8 xx{}

xx{}
 
```

第二、既然可以写在页面内，当然也可以JS来动态生成。我google了一把，发现还真有人这么做的。

文章地址如下：http://www.cnblogs.com/bruceli/archive/2011/04/11/2012470.html，写得还比较详细，原理也很简单。

不过这样的缺憾就是把条件注释限定到JS上了，于CSS就是鸡肋了。

继续，既然可以动态生成条件注释来辨明IE版本，基于IE的CSS hack，应该也可以动态生成一段html片段，用样式值来判定版本。

下面是最容易想到的形式，我测试发现这么确实可以，不过也发现了一个问题，看下面的一段代码：

```html
<div id="test_1"><span style="color: red; color: #ff6600\0; color: yellow\9\0;  *color:green; _color:blue;">测试</span></div>
<script type="text/javascript">
    var test_1 = document.getElementById('test_1');
    var test_2 = document.createElement('div');
    test_2.innerHTML = '<span style="color: red; color: #ff6600\\0; color: yellow\\9\\0;  *color:green; _color:blue;">测试</span>';
    console.log('test_1:' + test_1.firstChild.style.color + '----' + 'test_2:' + test_2.firstChild.style.color);
</script>
```

    在IE9下结果：LOG: test_1:yellow----test_2:yellow 
    在IE8下结果：LOG: test_1:#ff6600----test_2:#ff6600 
    在IE7下结果：LOG: test_1:green----test_2:blue 
    在IE6下结果：test_1:blue ----test_2:blue （IE6没有console.log，所以上面的console.log需要换成alert）

上面的问题大家应该看出来了，IE7下两种情况不一致，不知道是我的IE7兼容模式的问题还是别的什么原因，知道的请指教。

确认代码：

```html
<div><span style="*color:red; _color:blue;">原始</span></div>
<script>
var test = document.createElement('div');
test.innerHTML = '<span style="*color:red; _color:blue;">动态生成</span>';
document.body.appendChild(test);
</script>
```

    IE7结果："原始"显示为红色
    IE6结果："原始"显示为蓝色

基本原理和IE的条件注释差不多，我们一次检测color值就可以了，所以改变一下上面的例子就是：

```html
<div id="test_1"><span style="color: red; color: #ff6600\0; color: yellow\9\0;  *color:green; _color:blue;">测试</span></div>
<script type="text/javascript">
    var test_1 = document.getElementById('test_1');
    //var test_2 = document.createElement('div');
    //test_2.innerHTML = '<span style="color: red; color: #ff6600\\0; color: yellow\\9\\0;  *color:green; _color:blue;">测试</span>';
    var c = test_1.firstChild.style.color;
    alert(c=='red'?'other':c=='yellow'?'IE9':c=='#ff6600'?'IE8':c=='green'?'IE7':'IE6');
</script>
```
    在IE9下结果：IE9
    在IE8下结果：IE8
    在IE7下结果：IE7
    在IE6下结果：IE6

按理来说，对于FF,Chrome/Safari、opera都可以利用-moz、-webkit、-o等私有前缀来辨别，不过对于属性的选取要斟酌，类似color是不行的。

这个检测方法旁门左道而已，未来版本或者其他浏览器是不是有这个bug也不确定，而且IE7的那个bug我还没有弄清楚，所以也就暂时知道可以这么做就可以了。
