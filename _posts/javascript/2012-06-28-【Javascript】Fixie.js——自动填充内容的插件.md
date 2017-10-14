---
layout: post
title:  "【Javascript】Fixie.js——自动填充内容的插件"
date:   2012-06-28 13:46:04 +0800
categories: javascript
tag: [javascript]
---
## Fixie.js说明

Fixie.js是一个自动填充HTML文档内容的开源工具

官方网址地址：[http://fixiejs.com/](http://fixiejs.com/)

## 为什么使用Fixie？

当我们设计网站的时候，由于无法确定最终填充的内容，经常需要添加一些lorem ipsum（关于Lorem ipsum）到文档以便预览一下文档的展现效果。

问题来了，添加过多无聊的内容，使得我们的HTML文档变得臃肿，并且陷入复制-粘贴，手工编辑的毅种循环中。

Fixie.js就是为解决这个问题而诞生的——通过解析语义化的HTML5标签，Fixie可以自动填充匹配标签元素类型的内容，使得我们的HTML文档简洁，测试高效。

## 使用说明

第一步：添加fixie.js 到文档中

在body结束标签之前添加

```javascript
<script type="text/javascript" src="fixie.js"></script>
```

第二步：填充内容，这里有两种方法：

1. 任何需要填充内容的位置，设置`class="fixie"`，比如，如果先填充p标签的内容，直接设置`<p class="fixie"></p>`就行了，over，就这么简单。
2. 通过`fixie.init`填充内容

通过CSS选择器选择待填充的元素，在console（控制台啊，亲）或者script标签里面执行

```javascript
fixie.init([".array", "#of > .selectors", ".that", ".should", "#be > .populated", ".with", ".lorem"]) 
```
或者

```javascript
fixie.init(".string, #of > .comma, .separated, .selectors, .that, .should, #be > .populated, .with, .lorem")
```
命令，就可以自动填充了

PS：执行

```javascript
fixie.init(':empty')
```
可以填充文档里所有的空元素；

## 支持的元素

Fixie是通过标签类型来决定填充的内容的（语义化的体现），这里有几类是需要了解的。

    - `<h1 class="fixie"></h1>` - 添加几个单词的文本，`h2 - h6`亦然。
    - `<p class="fixie"></p>` - 填充一段文字
    - `<article class="fixie"></article>` - 填充几段文本（几个段落）
    - `<section class="fixie"></section>` - 同上
    - `<img class="fixie"></img>` - 填充一张注明了尺寸的图片
    - `<a class="fixie"></a>` - 填充一个随机的链接（做广告嫌疑？）

## 提示

修改默认的图片填充

执行 `fixie.setImagePlaceholder(source)`.

比如，如果你想从Flickr下载图片来填充，可以执行

```javascript
fixie.setImagePlaceholder('http://flickholdr.com/${w}/${h}/canon').init();
```

给容器添加 class="fixie"

容器内部所有的非空后代元素（注意后代与子代的区别）都会受到影响

看下面的说明

```html
<div class="fixie">
    <p>Hello <a></a></p>
</div>
```

Fixie会保留P标签里面的"Hello"文本，但是会填充a标签里面的内容

### Fixie for Rails
[fixie-rails](https://github.com/csexton/fixie-rails)

突出填充内容,可以添加

```html
.fixie{ border:4px solid red; }
```

到CSS里面，以便区分填充内容与真实内容。

## 授权
废话，不翻译了。


示例说明：

```html
<!DOCTYPE html>
<html>
<head>
    <title>Fixie.js Sample</title>

    <style>
        body{
            font-family: Helvetica, arial, sans-serif;
            width:800px;
            margin:150px auto;
        }
        img{
            width:400px;
            height:300px;
            float:right;
            margin:20px;
        }
        .fixie{ color: red;}
    </style>

</head>
<body>
    <article>
        <h1 class="fixie"></h1><!--这里会填充标题-->
        <p> Check us out at <a class="fixie"></a>,<!--这里会填充连接，但是外部的P标签因为非空，所以不会受影响-->
            and don't forget to view source.</p>
        <section class="fixie"><!--section的后代元素都会填充-->
            <p></p>
            <img/>
            <ul></ul>
            <p></p>
            <ol></ol>
        </section>
        <h2 class="fixie"></h2>
        <section class="fixie"></section>
    </article>

    <script type="text/javascript" src="fixie.js"></script>
    <script>
        // Changes default image source to Flickr
        fixie.setImagePlaceholder('http://flickholdr.com/${w}/${h}/fixie').init();
    </script>
</body>
</html>
```

显示效果

![1](http://pic002.cnblogs.com/images/2012/317534/2012062800022568.png)

