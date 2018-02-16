---
layout: post
title:  "命令记录-cat"
date:   2013-04-01 12:46:04 +0800
categories: computer
tag: [computer]
---
# cat

来源单词：catenate（连接） 

## 用途

主要包括下列用途： 

1. 将文本文件显示到屏幕 
2. 复制文本文件 
3. 连接文本文件 
4. 创建新的文本文件 

## 语法

```shell
cat filename 
cat options filename 
cat file1 file2 
cat file1 file2 > newcombinedfile 
```

### 显示文件内容

```shell
$ cat /etc/passwd
```

上面的命令显示了文件/etc/passwd的内容。默认情况下，cat将输出显示到屏幕上面，同样，可以用“>”将输出重定向到另外的命令输入或者文件。 

```shell
$ cat /etc/passwd > /tmp/test.txt
```

看看下面的例子： 

```shell
cat file1 - file2
```

'-' 表示从键盘获取输入，因此上面的例子就是先显示file1的内容，然后显示用户输入的内容，最后现实file2的内容(按下CTRL+D可以终止用户输入）。 
如果cat不加任何参数，那么默认从键盘获取输入，然后将结果输出到屏幕，例子如下： 

```shell
cat
1
1
hello
hello
```

### 连接文件

Concatenation意味着将多个文件内容连接到一起，同时原始的文件不会被修改或者被删除。下面的例子是将 /etc/hosts, /etc/resolv.conf, and /etc/fstab这三个文件的内容连接在一起然后输出到标准输出里面（默认是屏幕） 

```shell
cat /etc/hosts /etc/resolv.conf /etc/fstab
```
同样可以重定向到别的地方 

```shell
$ cat /etc/hosts /etc/resolv.conf /etc/fstab > /tmp/outputs.txt

$ cat /tmp/outputs.txt
```

或者通过管道来过滤数据： 

```shell
cat /etc/passwd | less
```

### 创建文件

下面的例子创建了一个foo.txt文件 

```shell
$ cat > foo.txt
```
没有指定输入源时，默认从键盘获取输入。 
你可以键入 

```shell
This is a test.
```
然后按CTRL + D来保存输入。注意，如果目标目录中原本就存在foo.txt目录，cat会一声不吭的覆盖掉原有的foo.txt，如果你想在原有的foo.txt后面追加内容，按照惯例，可以将‘>’替换为">>"： 

```shell
$ cat >> foo.txt
```

### 复制文件

cat可以创建一个新文件并将现有文件的数据传递给新文件，从而实现copy 

```shell
$ cat oldfile.txt > newfile.txt
```
创建一个新文件并从键盘获取输入： 

```shell
cat > newfile.txt
```
如果要同时从键盘和文件获取输入，可以参照上文的'-'符号： 

```shell
cat - file1 > file2
```
表示先从键盘读取输入，然后从file1获取输入，最后输出到file2中 

### 命令参数

    --help  显示帮助，几乎所有的GNU软件都有这么个同意的参数，另一个就是--version。
    
其他几个比较重要的是： 

    -b, --number-nonblank    对非空输出行编号
    -E, --show-ends          在每行结束处显示"$"
    -n, --number             对输出的所有行编号
    -s, --squeeze-blank      不输出多行空行
    -T, --show-tabs          将跳格字符显示为^I
    -v, --show-nonprinting   使用^ 和M- 引用，除了LFD和 TAB 之外
    
    -A, --show-all           等于-vET
    -e                       等于-vE
    -t                       与-vT 等价

### cat最佳实践【争议】

cat最主要的作用是连接文件，如果只有一个文件，使用cat只是增加无端的消耗而已，比如 

```shell
$ cat /proc/cpuinfo | grep model
```
可以用下面的命令代替： 

```shell
$ grep model /proc/cpuinfo
```
再看一个： 

```shell
cat filename | sed -e 'commands' -e 'commands2'
```
可以用命令 

```shell
sed sed -e 'commands' -e 'commands2' filename
```
代替。再者，cat显示大文件也比较吃力。


来源：http://www.cyberciti.biz/faq/howto-use-cat-command-in-unix-linux-shell-script/
