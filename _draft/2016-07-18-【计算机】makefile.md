---
layout: post
title:  "【计算机】makefile"
date:   2016-07-18 14:46:04 +0800
categories: computer
tag: [computer]
---

## Basic

```shell
    target_1,target_2,target_3: prerequisite_1 prerequisite_2
    <TAB>command_1
    <TAB>command_2
    <TAB>command_3
```

注意：commands 前面需要有一个 tab 制表符

```shell
hello : hello.c -lfl
    gcc 
```
make 对 -l<NAME> 形式的依赖提供了支持，表示会搜索 libNAME.so 形式的文件，或者 libNAME.a 

```shell
make --just-print
```

打印出将要执行的命令，但是并不执行。

```shell
.PHONY clean
```
指定一个假想的工作目标

```shell
$(variable-name)
```
变量名，如果是单个字符的变量名，括号可以省略

核心自动改变量：

$@ 

表示规则的目标文件名。如果目标是一个文档文件（Linux中，一般称.a 文件为
文档文件，也称为静态库文件），那么它代表这个文档的文件名。在多目标模式
规则中，它代表的是哪个触发规则被执行的目标文件名。 

$% 

当规则的目标文件是一个静态库文件时，代表静态库的一个成员名。例如，规则
的目标是“foo.a(bar.o)”，那么，“ $%”的值就为“bar.o”，“ $@ ”的值为“foo.a”。
如果目标不是静态库文件，其值为空。 

$< 

规则的第一个依赖文件名。如果是一个目标文件使用隐含规则来重建，则它代表
由隐含规则加入的第一个依赖文件。 

$? 

所有比目标文件更新的依赖文件列表，空格分割。如果目标是静态库文件名，代
表的是库成员（.o 文件）。 

$^ 

规则的所有依赖文件列表，使用空格分隔。如果目标是静态库文件，它所代表的
只能是所有库成员（.o 文件）名。一个文件可重复的出现在目标的依赖中，变量
“$^”只记录它的一次引用情况。就是说变量“$^”会去掉重复的依赖文件。 

$+ 

类似“$^”，但是它保留了依赖文件中重复出现的文件。主要用在程序链接时库
的交叉引用场合。 

$* 

工作目标的主文件名，一个文件名由两部分组成： 主文件名(stem) + 扩展名(suffix)


找不到文件按就去 VPATH 中找
```shell
VPATH = src include
```
更精确的模式指定 vpath：

```shell
vpath *.c src
vpath *.h include
```

打印所有的默认规则与变量
```shell
make --print-data-base
```

## 模式

% 大体相当于 shell 中的 *，但是只能出现一次。

























