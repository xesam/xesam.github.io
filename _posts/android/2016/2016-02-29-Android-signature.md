---
layout: post
title:  "Android Android签名相关"
date:   2016-02-29 12:46:04 +0800
categories: android
tag: [android]
---

#### 替换默认的 debug.keystore

新生成一个 debug.keystore，关键配置如下：

    alias :androiddebugkey
    keystore密码:android
    alias密码:android
    
替换 ./.android 目录下面的 debug.keystore 即可。



