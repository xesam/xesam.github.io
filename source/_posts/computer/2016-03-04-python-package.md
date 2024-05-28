---
layout: post
title:  "Python 包小结"
date:   2016-03-05 09:00:00 +0800
categories: computer
tag: [computer]
---
## 如何导入本地库

为了能够导入本地库，我们需要将本地库所在的目录添加到PYTHONPATH环境变量中。PYTHONPATH 是一个包含多个目录的列表，Pyton解释器会在这些目录中查找要导入的模块。

### 设置临时PYTHONPATH

通过在Python脚本中设置PYTHONPATH环境变量来临时添加本地库的路径。

```python
import sys
sys.path.append('/path/to/mylib')
```

### 设置永久PYTHONPATH

在Linux或Mac系统上，我们可以通过在编辑 ~/.bashrc （具体的文件需要参照具体的系统）文件中添加如下行来设置永久的PYTHONPATH:

```shell
export PYTHONPATH="/path/to/mylib:$PYTHONPATH"
```

在Windows系统上，我们可以通过以下步骤设置永久的PYTHONPATH:

1. 右键点击“我的电脑"（注意不是磁盘驱动符），选择”属性”；
2. 点击"高级系统设置"；
3. 点击“环境变量”；
4. 在"系统变量"中，找到名为"PYTHONPATH"的变量，如果不存在则创建；
5. 编辑"PYTHONPATH"变量，将本地库的路径添加到其中，多个路径之间用分号(;)分隔。
6. 点击“确定”关闭窗口。
7. 如果没生效，可能需要重启你的命令终端。