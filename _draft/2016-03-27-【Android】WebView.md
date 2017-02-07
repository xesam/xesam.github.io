---
layout: post
title:  "2016-03-27-【Android】WebView"
date:   2016-03-27 14:46:04 +0800
categories: Android
---

## 1. 无法弹出输入框

一般来说，动态添加的 WebView 会出现这个问题，设置

```
setFocusableInTouchMode(true);
```
就行了


## 关闭之后，Js 还在运行

在页面关闭的时候， 禁用 Js 就行了.

```java
getSettings().setJavaScriptEnabled(false);
```

退出 WebView 的时候需要关闭 js，
同时销毁 WebView 本身

## shouldOverrideUrlLoading 的区别
