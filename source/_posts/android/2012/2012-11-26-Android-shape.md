---
layout: post
title:  "Android中的shape"
date:   2012-11-26 13:46:04 +0800
categories: android
tag: [android]
---
shape类似CSS，用于背景，边框，便于兼容各种屏幕和分辨率

```xml
<?xml version="1.0" encoding="utf-8"?>
<shape xmlns:android="http://schemas.android.com/apk/res/android" 
    android:shape="rectangle">
    <!-- 填充色 -->
    <solid android:color="#e4e4e4"/>
    <!-- 描边 -->
    <stroke android:color="#e4e4e4" />
    <!-- 圆角半径 -->
    <corners android:radius="4dip" />
    <!-- 渐变 -->
    <gradient 
        android:angle="45"
        android:centerX="20dip"
        android:centerColor="#ff0000"
        android:startColor="#ffffff"
        android:endColor="#000000"/>
    <padding 
        android:left="10dip"/>
    <size android:width="60dip"
        android:height="30dip"/>
</shape>
```

shape属性：

    rectangle：矩形 
    oval：椭圆 
    line：线，需要 stroke 来设置宽度 
    ring：环形 

solid属性：

    color：填充颜色 

stroke属性：

    color：边框颜色 
    width：边框宽度 
    dashWidth：虚线框的宽度 
    dashGap：虚线框的间隔 
    
corners属性：

    radius：四个角的半径 
    topRightRadius：右上角的半径 
    bottomLeftRadius：右下角的半径 
    opLeftRadius：左上角的半径 
    bottomRightRadius：左下角的半径 
    
gradient属性：

    startColor：其实颜色 
    centerColor：中间颜色 
    endColor：结束颜色 
    centerX：中间颜色的相对X坐标（0 -- 1） 
    centerY：中间颜色的相对Y坐标（0 -- 1） 
    useLevel：（true/false）， 是否用作LevelListDrawable的标志 
    angle是渐变角度，必须为45的整数倍。0从左到右，90从下到上，180从右到左，270从上到下 
    type：渐变模式。 默认线性渐变，可以指定渐变为radial（径向渐变）或者sweep（类似雷达扫描的形式） 
    gradientRadius：渐变半径，径向渐变需指定半径。 
    
padding属性：

    left：左内边距 
    top：上内边距 
    right：右内边距 
    bottom：下内边距 
    
size属性:

    width：宽 
    height：高
