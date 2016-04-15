---
layout: post
title:  "【Android】AndroidStduio错误记录"
date:   2016-02-23 13:46:04 +0800
categories: android
---

系统：Ubuntu

java本版：1.7

## 1. 启动的时候“Plugin com.intellij failed to initialize and will be disabled null” 

解决办法：将java的安装位置更改到/usr/java或者/opt/java就行了，注意同时修改原本的JAVA_HOME系统变量。 

## 2. 下载的Android Studio自带了SDK，但是系统原本安装有SDK，所以删除新的SDK之后报错 “Your Android SDK is out of date or is missing templates. Please ensure you are using SDK version 22 or later.” 

解决办法：在SDK Manager中将tools(包括sdk tools,platform tools,build tools)更新到最新的版本。然后

    Configure -> Project Defaults -> Project Structure
    
在Project 设定Project SDK。在SDKs设定Buildtarget。 保存之后就可以“New Project”了

## 3. 修改包名之后 Activity class does not exist

问题描述：

修改了 applicationId 之后，无法从 As 界面 launcher Activity 。提示错误：

    Activity class {package/xxxxx} does not exist
    
这个应该是 As 自身的问题，没有刷新缓存，把 .idea *.iml 什么都删除一下，重新打开基本就可以了。