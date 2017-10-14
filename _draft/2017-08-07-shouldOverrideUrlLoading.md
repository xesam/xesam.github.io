---
layout: post
title:  "【Android】WebView与shouldOverrideUrlLoading"
date:   2017-08-07 13:46:04 +0800
categories: android
tag: [android]
---
涉及到 WebView 的开发，基本绕不开对 onPageStarted/shouldOverrideUrlLoading/onPageFinished 的使用，本文仅总结一下 WebView 的这几个方法的常用点。

## 调用时机
onPageStarted

onPageFinished

shouldOverrideUrlLoading

## 处理不同的 scheme

http://blog.csdn.net/a0407240134/article/details/51482021