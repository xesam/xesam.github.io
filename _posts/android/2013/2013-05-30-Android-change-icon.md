---
layout: post
title:  "Android 能否动态修改App的桌面名称或者图标"
date:   2013-05-30 12:46:04 +0800
categories: android
tag: [android]
---

目前的目测是不行的。 

本来想想也是，如果这都可以修改的话，很容易在安装之后变成一个山寨的QQ或者支付宝，完全的不稳定因素。 
但是有要求没办法，还是先调查一下。 

1. app name是在manifest文件中指定的，没有办法修改。 
2. Launcher可能会缓存应用图标，这种情况下，就算图标被修改了也只会在下次重启之后生效 
3. 使用activity-alias可以创建不同的app name和app_icon的别称，但是只是假象而已，真正的app还是按照原本的显示。 
4. 可以创建widget来在home动态展示内容，制造修改icon的假象 
5. 除非重写Launcher，没有找到其他的方法。 


另外提到最多的是setTitle，这个是修改 Activity 的。
