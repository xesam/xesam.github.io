---
layout: post
title:  "Android 无限滚动的图片"
date:   2015-09-08 12:46:04 +0800
categories: android
tag: [android]
---

github 地址[InfiniteImageView](https://github.com/xesam/InfiniteImageView)

参考 [AndroidScrollingImageView](https://github.com/Q42/AndroidScrollingImageView) 

## 特性
1. 支持 Android 2.3
2. 支持竖直滚动
3. 支持 drawable

## 使用

xml形式：

    <dev.xesam.android.widgets.InfiniteImageView
        android:id="@+id/ifi"
        android:layout_width="match_parent"
        android:layout_height="wrap_content"
        InfiniteImageView:speed="-2dp"
        InfiniteImageView:src="@drawable/a_2" />

java代码：

```java
    InfiniteImageView.setDrawable(new AzDrawable());
```

## demo

![输入图片说明](https://static.oschina.net/uploads/img/201509/09095034_8WHB.gif "在这里输入图片标题")
