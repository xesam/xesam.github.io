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
    pip venv {project name}
```
或者
```shell
    python -m pip venv {project name}
```

此时在 {project name} 文件夹下创建：

    Include
    Lib
    Scripts（也有可能是 bin 之类的名称）
    pyvenv.cfg

等文件夹

### 激活虚拟环境

```shell
    ./Scripts/activate
```
不同的操作系统脚本文件可能不一致，比如 windows 下面是 activate.bat 

