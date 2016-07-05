---
layout: post
title:  "【Android】NDK与SWIG"
date:   2016-07-06 01:00:00 +0800
categories: Android
---

本文主要是《Android C++ 高级编程——使用 NDK》的笔记。
国内专门讲 NDK 的书籍寥寥无几，这本貌似是唯一一本翻译的，当然，国外还是有好几本关注 NDK 的书籍，但是都没有中文译本而已。

因为偷懒，实践的时候从网上拷贝的代码，结果某些作者太不靠谱，抄写的代码都是错的，坑死我了。

## SWIG 基础

可以参考：

1. [开发人员 SWIG 快速入门](http://www.ibm.com/developerworks/cn/aix/library/au-swig/)
2. [swig 官网](http://www.swig.org/)

## 在 Android 中的使用

ubuntu 14.04 + eclipse 

在 jni 文件夹中定义接口文件，SWIG 会基于此接口文件来生成相应的集成代码：

下面是接口文件 Unix.i：

```shell
%module Unix

/* unistd.h 是 C 和 C++ 中提供对 POSIX API 支持的头文件 */

%{
#include <unistd.h>	
%}

typedef unsigned int uid_t;

extern uid_t getuid(void);

```

这个时候可以直接调用 swig 来生成集成代码，

```shell
swig -java -package dev.xesam.ndk -outdir dev/xesam/ndk Unix.i
```

注意：outdir 一定要事先就存在


不过为了方便，还是直接与 eclipse 整合比较好。在 jni 文件夹定义一个 swig.mk，将 swig 处理单独出来，swig.mk 内容如下：

```shell
# 定义包名，对应 -package 参数
ifndef MY_SWIG_PACKAGE
	$(error MY_SWIG_PACKAGE is not defined.)
endif

# 定义输出目录，对应 -outdir 参数
# subst 表示替换，即用 "/" 替换 包名中的 "."
MY_SWIG_OUTDIR :=$(NDK_PROJECT_PATH)/src/$(subst .,/,$(MY_SWIG_PACKAGE))

# 定义生成文件类型，这里默认是 c
ifndef MY_SWIG_TYPE
	MY_SWIG_TYPE := c
endif

# 如果目标源文件是 c++，那么在执行 swig 命令的时候就需要加上 −c++ 参数
ifeq ($(MY_SWIG_TYPE),cxx)
	MY_SWIG_MODE := −c++
else
	MY_SWIG_MODE :=
endif

# 将生成的 .c 文件加入编译文件中
LOCAL_SRC_FILES += $(foreach MY_SWIG_INTERFACE,$(MY_SWIG_INTERFACES),$(basename $(MY_SWIG_INTERFACE))_wrap.$(MY_SWIG_TYPE))

# 定义 target，每个待生成的 XXX_wrap.c 源文件都依赖与之对应的 XXX.i 接口文件 
# 由于 outdir 一定要存在，所以先创建 outdir 目录结构
# $< 表示第一个依赖文件，也就是对应的 XXX.i 接口文件 
%_wrap.$(MY_SWIG_TYPE) : %.i
	$(call host-mkdir, $(MY_SWIG_OUTDIR))
	swig \
	-java \
	$(MY_SWIG_MODE) \
	-package $(MY_SWIG_PACKAGE) \
	-outdir $(MY_SWIG_OUTDIR) \
	$<
```
注意，按照 Makefile 的规范来写，特别是空格与 TAB 的区别。

上面定义的 MY_SWIG_PACKAGE 等变量都定义在 Android.mk 中，将 swig.mk 加入到 Android.mk 即可。Android.mk 内容如下；

```shell
LOCAL_PATH := $(call my-dir)

include $(CLEAR_VARS) # 清除除了 LOCAL_PATH 之外的 LOCAL_* 变量

LOCAL_MODULE    := hello-ndk # 设定一个唯一的名称

MY_SWIG_PACKAGE := dev.xesam.ndk
MY_SWIG_INTERFACES := Unix.i
MY_SWIG_TYPE := c

include $(LOCAL_PATH)/swig.mk

include $(BUILD_SHARED_LIBRARY)
```

定义完毕之后，工程大致结构如下：

	project_dir
		|--src
		|--jni
			|--Android.mk
			|--Application.mk
			|--swig.mk
			|--Unix.i
		
在项目根目录运行 

```shell
ndk-build
```
输入大致如下：

```
mkdir -p  ./src/dev/xesam/ndk
swig \
	-java \
	 \
	-package dev.xesam.ndk \
	-outdir ./src/dev/xesam/ndk \
	jni/Unix.i
[armeabi] Compile thumb  : hello-ndk <= Unix_wrap.c
[armeabi] SharedLibrary  : libhello-ndk.so
[armeabi] Install        : libhello-ndk.so => libs/armeabi/libhello-ndk.so

```
运行完毕之后，工程大致结构如下：

	project_dir
		|--src
			|--dev
				|--xesam
					|--ndk
						|--Unix.java
						|--UnixJNI.java
		|--jni
			|--Android.mk
			|--Application.mk
			|--swig.mk
			|--Unix.i
			|--Unix_wrap.c
		|--libs
			|--armeabi
				|--libhello-ndk.so
				

libhello-ndk.so 可以在工程代码直接使用，当然，生成的 UnixJNI.java 需要补充 loadLibrary 调用：

```java
public class UnixJNI {
  ...
  static{
	  System.loadLibrary("hello-ndk");
  }
}
```

测试Activity：
 
```java

import dev.xesam.ndk.Unix;

public class MainActivity extends Activity {

	@Override
	protected void onCreate(Bundle savedInstanceState) {
		super.onCreate(savedInstanceState);
		setContentView(R.layout.activity_main);
		TextView tv = (TextView) findViewById(R.id.tv);
		tv.setText(Unix.getuid() + "");
	}
}

```