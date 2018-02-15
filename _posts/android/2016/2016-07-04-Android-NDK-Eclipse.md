---
layout: post
title:  "Android NDK与Eclipse"
date:   2016-07-04 14:46:04 +0800
categories: android
tag: [android]
---
AS 对 NDK 的支持一直不太好，所以基本所有关于的 NDK 的书籍都是基于 Eclipse 开发的，不过 Eclipse 已经放弃支持了，
AS 支持 NDK 的实验版 gradle 插件已经出来了，可以试试。 
本文简单记录《Android.NDK.Beginner's.Guide》的 Eclipse 配置而已。

## 环境

    ubuntu: 14.04
    eclipse: Mars.2 Release (4.5.2) 安装 ADT，CDT

## 准备工作

添加环境变量：

    JAVA_HOME
    ANDROID_HOME
    ANDROID_NDK

## javah 生成头文件

主要使用 External Tools：

    Run --> External Tools --> External Tools Configurations 

新建一个 Configuration：

![ndk-eclipse-1]({{ site.baseurl }}/image/ndk-eclipse-1.png)

    ${system_path:javah}

javah 命令的路径，前提是 javah 已经加入到 $PATH 中，不然需要指定 javah 的完整路径。

    ${project_loc}/jni

生成的 *.h 文件目录，${project_loc} 表示工程目录

    -cp "${project_classpath}:${env_var:ANDROID_HOME}/platforms/android-23/android.jar" ${java_type_name}

指定 classpath，javah 命令需要用到。由于 javah 是从 class 文件中生成对应的 *.h 文件，因此，src 中改动之后需要先 build 一下，javah 才能正确生成。
所以，最好是开启 Build Automatically。

如果要生成对应的 .h 文件，先在 src 中选择要生成的 .java 源文件，然后运行

    Run --> External Tools --> ndk_header(这里是刚添加的，也可以是其他的名字)
    
## ndk-build

将 ndk-build 命令集成到 eclipse 中：

1. 先将 Android 工程转成 C/C++ 工程,
    
        New --> Other --> C/C++ --> Convert to a C/C++ Project

2. 工程上右键 Properties

    C/C++ Build： 配置编译选项
    
            --> Builder Settings --> Build command 改为 ndk-build
        
    ![ndk-eclipse-2]({{ site.baseurl }}/image/ndk-eclipse-2.png)

            --> Behaviour --> Build on resource save .每次修改保存的时候即时编译
        
    ![ndk-eclipse-3]({{ site.baseurl }}/image/ndk-eclipse-3.png)
     
    C/C++ General： 添加各种头文件
      
            --> Paths and Symbols 具体位置视情况而定
            /apps/android-sdk-linux/ndk-bundle/platforms/android-9/arch-arm/usr/include
            /apps/android-sdk-linux/ndk-bundle/toolchains/arm-linux-androideabi-4.9/prebuilt/linux-x86_64/lib/gcc/arm-linux-androideabi/4.9.x/include
            
    ![ndk-eclipse-4]({{ site.baseurl }}/image/ndk-eclipse-4.png)
    
    每种语言都加上，所以添加的时候选择 all 就行。
    
    ![ndk-eclipse-4]({{ site.baseurl }}/image/ndk-eclipse-4-2.png)

    Builders ：配置 build 顺序，将 CDT Builder 调整到 Android Package Builder 的正上方：
    
    ![ndk-eclipse-5]({{ site.baseurl }}/image/ndk-eclipse-5.png)
    
3. 自动运行 javah 

    这个其实没必要，因为没必要每次都生成 .h 文件，就算生成了，也没有可用的实现，所以个人觉得还是手动调用比较靠谱。
    操作就是添加一个 Builder 放到 CDT Builder 的正上方：
    
        Builders --> New --> Program
        
    所有参数配置与 “javah生成头文件的配置”一样即可，

一切完成之后，每次 Run 的时候，都会将最新的 so 文件打包编译打包进去。

## 调试

上面的的  ndk-build 命令需要添加参数 

    ndk-build NDK_DEBUG=1

Google 官方的 ADT 只更新到 23.0.7，如果你的 ndk 比较新，那么，调试的时候会出现各种乱七八糟的 bug ，比如，找不到 gdb 之类。
所以，先把 ADT 更新到最新，野生版本参见[https://github.com/khaledev/ADT](https://github.com/khaledev/ADT)。

然后直接 Debug AS “Android Native Application” 就行了，也不需要像书中那般配置，因为书的配置已经过时了。

