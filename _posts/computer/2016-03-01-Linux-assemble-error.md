---
layout: post
title:  "linux 汇编错误记录"
date:   2016-03-01 16:46:04 +0800
categories: computer
tag: [computer]
---

#### insight 安装

```shell
variable 'errcount' set but not used
```

解决办法：

```shell
./configure --disable-werror
```

参考阅读： [http://www.tuicool.com/articles/VRJf6v](http://www.tuicool.com/articles/VRJf6v)

#### 32/64 位问题

编译一个简单的汇编文件，然后链接出现的时候这个问题。

```shell
    $nasm -f elf -g -F stabs easy.asm
    $ld -o easy easy.o 
```

错误结果：

    ld: i386 architecture of input file `eatsyscall.o' is incompatible with i386:x86-64 output

解决方案：

指定 64 位


```shell
    $nasm -f elf64 -g -F stabs easy.asm
    $ld -o easy easy.o 
```

