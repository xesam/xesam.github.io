---
layout: post
title:  "【Android】使用 dalvikvm 命令"
date:   2015-08-27 12:46:04 +0800
categories: android
---
# 【Android】使用 dalvikvm 命令

整理版本.原文地址: [http://bbs.pediy.com/showthread.php?t=184592](http://bbs.pediy.com/showthread.php?t=184592)

# 步骤

1. 编写 .java 源文件,编译为 .class
2. 使用 dx(在sdk 目录的 build-tools 下面)将 .class 编译为 .dex 文件
3. 将 .dex 文件载入 android 设备, 使用 dalvikvm 运行

# 具体操作

## 创建 java 源文件

    public class Hello{
        public static void main(String[] argc){
            System.out.println("Hello, Android!");
        }
    }

## 编译 java 源文件
    
    javac Hello.java

生成 Hello.class 文件 

## 编译成 dex 文件 
    
    dx --dex --output=Hello.dex Hello.class 

编译正常会生成 Hello.dex 文件 。

## 使用 ADB 运行测试
    
    adb root
    adb push Hello.dex  /sdcard/
    adb shell

    dalvikvm -cp /sdcard/Hello.dex Hello  

得到输出如下:
           
    Hello, Android!

# 重要说明 

1. Android4.4 的官方模拟器和自己的手机上测试都提示找不到 Class 路径 ，在Android 老的版本4.3(以及 4.0 模拟器)上测试还是有输出的 。
2. 因为命令在执行时 ， dalvikvm 会在 /data/dalvik-cache/  目录下创建 .dex 文件 ，因此要求 ADB 的执行 Shell 对目录 /data/dalvik-cache/  有读、写和执行的权限 ，否则无法达到预期效果 。 
