---
layout: post
title:  "Android 墙内操作"
date:   2015-11-11 13:46:04 +0800
categories: android
tag: [android]
---
## 一，更新 SDK
各种工具参考 [androiddevtools](http://www.androiddevtools.cn/index.html)

<del>腾讯 Bugly 使用比较流畅，推荐。 </del>

还是 中国科学院开源协会镜像站 的比较靠谱。。

## 二，编译 Android 源码

编译环境：

操作系统 Ubuntu 14.04.1 x86_64

#### 更换源。ubuntu 自带的源容易发生版本不匹配的问题。

替换源(/etc/apt/source-list)为：

    deb http://mirrors.163.com/ubuntu/ trusty main restricted universe multiverse
    deb http://mirrors.163.com/ubuntu/ trusty-security main restricted universe multiverse
    deb http://mirrors.163.com/ubuntu/ trusty-updates main restricted universe multiverse
    deb http://mirrors.163.com/ubuntu/ trusty-proposed main restricted universe multiverse
    deb http://mirrors.163.com/ubuntu/ trusty-backports main restricted universe multiverse
    deb-src http://mirrors.163.com/ubuntu/ trusty main restricted universe multiverse
    deb-src http://mirrors.163.com/ubuntu/ trusty-security main restricted universe multiverse
    deb-src http://mirrors.163.com/ubuntu/ trusty-updates main restricted universe multiverse
    deb-src http://mirrors.163.com/ubuntu/ trusty-proposed main restricted universe multiverse
    deb-src http://mirrors.163.com/ubuntu/ trusty-backports main restricted universe multiverse
    
更新一下：

```shell
    $ sudo apt-get updata
```

#### 配置编译环境

```shell
    $ sudo apt-get install git-core gnupg flex bison gperf build-essential \
      zip curl zlib1g-dev gcc-multilib g++-multilib libc6-dev-i386 \
      lib32ncurses5-dev x11proto-core-dev libx11-dev lib32z-dev ccache \
      libgl1-mesa-dev libxml2-utils xsltproc unzip
```

各种安装依赖冲突的情况，都可以通过更换源解决。

#### 安装 java

这个需要根据编译的源码版本而定，比如编译 Android 6.0 需要 OpenJDK 8。但是编译 Android 4.0 需要 Oracle Java 6.
具体安装过程略过。

#### 下载源码

这里使用清华大学的镜像。

参考文章 [清华大学 TUNA 镜像源,Android 镜像使用帮助](https://mirrors.tuna.tsinghua.edu.cn/help/AOSP/)

参考文章 [同步、更新、下载Android Source & SDK from 国内镜像站](http://www.cnblogs.com/baizx/p/4442723.html)

安装 Repo，

1, 添加 PATH

```shell
    $ mkdir ~/bin
    $ PATH=~/bin:$PATH
```

2, 下载 Repo

```shell
    $ curl https://storage.googleapis.com/git-repo-downloads/repo > ~/bin/repo
    $ chmod a+x ~/bin/repo
```

3., 修改repo

修改环境变量或者直接修改 /git-repo/repo 文件。

将 google 的地址

    REPO_URL= 'https://gerrit.googlesource.com/git-repo'

改为清华大学的地址

    REPO_URL= 'https://gerrit-google.tuna.tsinghua.edu.cn/git-repo'

4, 下载 manifest

```shell
    $ repo init -u git://aosp.tuna.tsinghua.edu.cn/android/platform/manifest
```

或者选择版本
    
```shell
    $ repo init -u git://aosp.tuna.tsinghua.edu.cn/android/platform/manifest -b android-4.0.1_r1
    
```

5, 同步

```shell
    $ repo sync
```

#### 编译

建立环境

```shell
    $ source build/envsetup.sh
```

这个时候就可以使用 lunch，mmm等命令了

```shell
    $ lunch 
```
lunch负责设置一些环境变量，比如 TARGET_PRODUCT 等等。
结果中 full 表示完全编译，eng表示工程版本，full-eng就是模拟器版本。

开始编译，指定4线程。

```shell
    $ make -j4

```
注意编译过程中的 java 版本问题。

## 三，更新各种依赖库

暂时没有 jcenter 镜像，也别瞎折腾了，还是搞个 vpn 吧，毕竟党国无耻。





