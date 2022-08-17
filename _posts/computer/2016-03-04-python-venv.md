---
layout: post
title:  "venv 常用"
date:   2016-01-04 09:00:00 +0800
categories: computer
tag: [computer]
---

从Python 3.4开始，pip与venv模块会在安装Python时一起默认安装。

### 创建虚拟环境

```shell
python -m venv {project name}
```
如果是当前目录，直接使用 

```shell
python -m venv .
```
就行了。此时在 {project name} 文件夹下创建下述文件夹：

    Include
    Lib
    Scripts（也有可能是 bin 之类的名称）
    pyvenv.cfg

用 venv 工具创建出的虚拟环境，初始只装有pip与setuptools模块，除此之外，没有预装其他的软件包。

### 激活虚拟环境

```shell
./Scripts/activate
```
不同的操作系统脚本文件可能不一致，比如 windows 下面是 activate.bat 。
如果在linux 环境下，可以使用：

```shell
source ./Scripts/activate
```

执行脚本之后，就会激活虚拟环境，此时执行：


```shell
which python 
```
可以查看相关的 python 或者 pip 信息。


### 安装依赖

在激活的终端里面，可以使用 pip 安装对应的模块。比如：

```shell
pip install json5
```
通过

```shell
pip show json5
```
可以验证 json5 的安装路径以及其他信息。


### 退出虚拟环境

通过与 activate 相反的 deactivate 操作，即可回到默认环境。

### 重建依赖

用 python3 -m pip freeze 命令把当前环境所依赖的包明确地保存到一份文件之中（按照惯例，这个文件命名为 requirements.txt）。

```shell
python3 -m pip freeze > requirements.txt
```
或者：

```shell
pip freeze > requirements.txt
```
就会在执行目录生成一份 requirements.txt 文件，内容如下：

```plain
json5==0.9.6
```
如果对版本规则比较熟悉，也可以手写这份文件。

假设要用 {project name} 环境之中的配置来构建另外一套相似虚拟环境。我们先用venv工具把那套环境创建出来，然后用activate激活它。具体命令可以参见 上文。

我们可以执行python3 -m pip install命令，把刚才用 python3 -m pip freeze 所保存的 requirements.txt 文件通过-r选项传给它，这样就能够将那份文件所记录的软件包安装到这套环境里面了。

```shell
python3 -m pip install -r /a/b/c/d/requirements.txt
```
或者：

```shell
pip install -r requirements.txt
```

#### 哈希值检查

要实现哈希检查模式，只需在需求文件中写入带有包名的摘要:

```plain
json5==0.9.6 --hash=sha256:{hash digest}
```
支持的哈希算法包括 md5、sha1、sha224、sha224、sha384、sha256 和 sha512。

### 需要注意的问题

1. Python本身的版本并不包含在requirements.txt之中，所以必须单独管理。
2. 虚拟环境有个很容易出错的地方，就是不能直接把它移动到其他路径下面，因为它里面的一些命令（例如python3）所指向的位置都是固定写好的，其中用到了这套环境的安装路径，假如移动到别处，那么这些路径就会失效。


参考《Effective Python》，纯做记录用。