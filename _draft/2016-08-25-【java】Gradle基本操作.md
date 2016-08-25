---
layout: post
title:  "【java】Gradle基本操作"
date:   2016-08-25 08:00:00 +0800
categories: java
tag: [java]
---

gradle 官网的网友翻译：[https://github.com/msdx/gradledoc/tree/1.12](https://github.com/msdx/gradledoc/tree/1.12)

## 目录字段

projectDir

    The directory containing the project build file.

rootDir

    The root directory of this project. The root directory is the project directory of the root project.
    
buildDir

    The build directory of this project. The build directory is the directory which all artifacts are generated into. 
    The default value for the build directory is projectDir/build

## 获取系统的环境变量
    
```groovy
System.getenv()['ANDROID_HOME']
```
或者 

```
System.getenv('ANDROID_HOME)
```

