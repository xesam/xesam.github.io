---
layout: post
title:  "aar依赖"
date:   2017-05-07 13:46:04 +0800
categories: android
tag: [android]
---
问题记录。

今天添加 aar 依赖之后，一直提示找不到 aar 中的定义类，然后发现甚至都没有生成 build/intermediates/exploded-aar 文件夹，原因就是新的 as 版本添加了 aar 缓存，在 .android/build-cache 中，手工添加或者更新 aar 文件之后，缓存并没有刷新，因此导致找不到类或者其他类似问题。

简单的解决办法就是禁止掉 aar 缓存，在 gradle.properties 中添加一行内容：

    android.enableBuildCache=false

重新 build 一下，就可以看到 exploded-aar 出现了，也更新了。