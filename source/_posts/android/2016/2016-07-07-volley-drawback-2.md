---
layout: post
title:  "Volley缺陷"
date:   2016-07-07 13:46:04 +0800
categories: android
tag: [volley]
---

#### 1. 解析 内部直接使用 Memory buffers 来缓存响应

在 BasicNetwork 实现中，从服务器获取到 Entity 之后，会将 Entity 转换成 byte 数组，缓存在 ByteArrayPool 中。
本来 ByteArrayPool 的出发点是为了减少虚拟机在堆上动态分配内存的开销。但是，如果响应本身就比较大（比如一张大图），这个时候就会有问题了。
一次性向 ByteArrayPool 申请较大内存，不仅引起内存占用量上升，甚至可能引起 OOM 错误。

#### 2. 内部依赖 Apache HttpClient

从 Android 6 开始，Apache HttpClient 被废弃了，这就导致如果想要使用 Volley，要么将 Compile SDK 修改为 23 以下，要么使用

```gradle
    android {
        useLibrary 'org.apache.http.legacy'
    }
```    
来增加 HttpClient 支持。

#### 3. 粗暴的 Retry Policy

默认超时事件 2.5s，基本算是鸡肋的配置，因为除了 wifi 环境，没可能在 2.5s 之内拿到响应，所以每次都得重新设置。

 