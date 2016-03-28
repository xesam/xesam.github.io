---
layout: post
title:  "【Android】AndroidStduio错误记录"
date:   2016-02-23 13:46:04 +0800
categories: android
---

系统：Ubuntu

java本版：1.7

### 问题一：启动的时候“Plugin com.intellij failed to initialize and will be disabled null” 

解决办法：将java的安装位置更改到/usr/java或者/opt/java就行了，注意同时修改原本的JAVA_HOME系统变量。 

### 问题二：下载的Android Studio自带了SDK，但是系统原本安装有SDK，所以删除新的SDK之后报错 “Your Android SDK is out of date or is missing templates. Please ensure you are using SDK version 22 or later.” 

解决办法：在SDK Manager中将tools(包括sdk tools,platform tools,build tools)更新到最新的版本。然后

    Configure -> Project Defaults -> Project Structure
    
在Project 设定Project SDK。在SDKs设定Buildtarget。 保存之后就可以“New Project”了