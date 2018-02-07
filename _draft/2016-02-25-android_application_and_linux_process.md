---
layout: post
title:  "Android Application与Linux Process"
date:   2016-02-25 13:46:04 +0800
categories: Android
---
##Application启动


##同一个 Application 运行在不同的 Process 中

###多次调用 Application#onCreate()

###android:process=":remote" 与 android:process="remote" 的区别

http://aijiawang-126-com.iteye.com/blog/1880135

也就是说android:process=":remote"，代表在应用程序里，当需要该service时，会自动创建新的进程。
而如果是android:process="remote"，没有“:”分号的，则创建全局进程，不同的应用程序共享该进程。 

##不同的 Application 运行在同一个的 Process 中

http://blog.sina.com.cn/s/blog_86d3fabb0100xom9.html

