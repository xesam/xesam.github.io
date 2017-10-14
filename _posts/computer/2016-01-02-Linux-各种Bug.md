---
layout: post
title:  "【Linux】各种Bug"
date:   2016-01-02 13:46:04 +0800
categories: computer
tag: [computer]
---
# 【Linux】各种Bug

# jd-gui 错误

系统 ubuntu 14.04

```shell
$ ./jd-gui 
./jd-gui: error while loading shared libraries: libgtk-x11-2.0.so.0: cannot open shared object file: No such file or directory

$ sudo apt-get install libgtk2.0-0:i386
$ ./jd-gui 
./jd-gui: error while loading shared libraries: libXxf86vm.so.1: cannot open shared object file: No such file or directory

$ sudo apt-get install libxxf86vm1:i386
$ ./jd-gui 

./jd-gui: error while loading shared libraries: libSM.so.6: cannot open shared object file: No such file or directory

$ sudo apt-get install libsm6:i386
$ ./jd-gui 

./jd-gui: error while loading shared libraries: libstdc++.so.6: cannot open shared object file: No such file or directory

$ sudo apt-get install lib32stdc++6
$ ./jd-gui 

Gtk-Message: Failed to load module "overlay-scrollbar"
Gtk-Message: Failed to load module "unity-gtk-module"
(jd-gui:4746): Gtk-WARNING **: Unable to locate theme engine in module_path: "murrine",
...
```

