---
layout: post
title:  "Android 简单的日志工具"
date:   2015-10-20 13:46:04 +0800
categories: android
tag: [android]
---

地址 ： [https://github.com/xesam/AndroidLogTools](https://github.com/xesam/AndroidLogTools)

现在包含两个类：

1. 打印日志
1. 崩溃记录

# 使用方式

    compile 'dev.xesam.android:AndroidLogTools:0.1.2'

# 打印日志 L
对 android.util.Log 的简单封装，支持 d(Object... content) 的调用形式，避免对 String 的硬性要求，使用示例：

开启日志（默认不打印）：

    L.enable(true);

打印日志：

    L.d();
    L.d(null);
    L.d(null, null);
    L.d(this);
    L.d(this, this);
    L.d(1);
    L.d(1, 2);
    L.d("a");
    L.d("a", "b");
    
结果如下：

    D/L[empty_tag]: L[empty_content]
    D/L[null]: L[null]
    D/L[null]: L[null]
    D/MainActivity: L[empty_content]
    D/MainActivity: dev.xesam.android.logtools.demo.MainActivity@32dd3da6
    D/1: L[empty_content]
    D/1: 2
    D/a: L[empty_content]
    D/a: b
    
# 崩溃记录 CrashLog

将崩溃记录写入外部文件中，便于检查。（注意，只在测试的时候才使用），使用示例:

在 Application 中注册:

    CrashLog.register(this);
    
即可。

记录日志保存在 XXX/sdcard/Android/data/#{package_name}/files/目录之下，比如：

    crash.2015-10-06T12:03:24.txt
