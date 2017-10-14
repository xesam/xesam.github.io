---
layout: post
title:  "【AndroidSupport】RoundedBitmapDrawable 创建圆角图片"
date:   2015-11-12 13:46:04 +0800
categories: android
tag: [android]
---

#【AndroidSupport】RoundedBitmapDrawable 创建圆角图片

## 简介
RoundedBitmapDrawable 是 android.support.v4.graphics.drawable 里面的一个类，用来创建简单的圆角图片。
如果只是简单的圆角展示,比如展示一个圆角头像，这个类完全可以胜任。

## 简单使用

1. 获取 RoundedBitmapDrawable。RoundedBitmapDrawable 是一个抽象类，无法直接获取。所以提供了 RoundedBitmapDrawableFactory 来操作:

    RoundedBitmapDrawableFactory的静态签名:

        static RoundedBitmapDrawable	create(Resources res, InputStream is)
        static RoundedBitmapDrawable	create(Resources res, String filepath)
        static RoundedBitmapDrawable	create(Resources res, Bitmap bitmap)
        
    没有提供直接从 resId 获取的方法，但是是一样的:
    
        RoundedBitmapDrawable roundedBitmapDrawable = RoundedBitmapDrawableFactory.create(getResources(), BitmapFactory.decodeResource(getResources(), R.drawable.xxx));

2. 设置属性。几个重要的属性:

    1. cornerRadius：圆角半径
    1. alpha：透明度
    
    如果想得到一个圆形，那么可以直接调用 RoundedBitmapDrawable#setCircular(true)，
    
    不过这样需要注意点是，如果原始的图形不是圆形，那么图形会变形。
    
    当然，结果还与 scaleType 有关，这里有点复杂，暂无需关心。所以，如果你想要一个圆形，你就给一个正方形。
    
    不要同时设置 cornerRadius 和 setCircular(true)，因为两者是冲突的。

3. 设置 Drawable。 ImageView#setImageDrawable(roundedBitmapDrawable);

## 原理

RoundedBitmapDrawable 内部使用 BitmapShader 来处理图形渲染，无他。

# 第三方开源控件

RoundedBitmapDrawable 的局限性还是比较大，如果想要实现一写些自由度更大的圆角，边框等等，可以考虑使用第三方空间，比如：

[CircularImageView](https://github.com/lopspower/CircularImageView)
[RoundedImageView](https://github.com/vinc3m1/RoundedImageView)
