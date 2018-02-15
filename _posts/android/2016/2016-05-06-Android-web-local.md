---
layout: post
title:  "Android 远程网页访问本地资源"
date:   2016-05-06 08:00:00 +0800
categories: android
tag: [android]
---
WebView 打开网页的时候，如果网页里面包含较多的 CSS， JS，图片等资源，可能需要非常长的时间。
为了提高加载速度，我们可以将各个网页通用的资源预先内置到 App 中，在网页从远程服务器加载资源之前，先检查本地是否已经有对应的预置或者预下载资源。
如果根据规则命中本地资源，则让 WebView 直接加载本地资源，当没有找到本地资源的时候，再将控制让渡给 WebView 默认的加载机制。

详见 [https://github.com/xesam/WebLocalResource](https://github.com/xesam/WebLocalResource)
