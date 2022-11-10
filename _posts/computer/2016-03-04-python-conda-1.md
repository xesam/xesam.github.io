---
layout: post
title:  "conda 常用"
date:   2016-01-04 08:00:00 +0800
categories: computer
tag: [computer]
---

conda是一款软件管理软件，相当于应用商店，在使用 Python 的过程中，可以用来管理 Python 版本。

## 常用的命令

### 1. 查看安装了哪些包


```bash
    conda list
```

### 2. 查看当前存在哪些虚拟环境

```bash
    conda env list 
    conda info -e
```

### 3. 检查更新当前conda


```bash
    conda update conda
```

### 4. Python创建虚拟环境


```bash
    conda create -n your_env_name python=x.x
```

create 命令创建 python 版本为 x.x，名字为 your_env_name 的虚拟环境。your_env_name 文件可以在 conda 安装目录的 envs 文件下找到。

### 5. 激活或者切换虚拟环境

打开命令行，输入 python --version 检查当前 python 版本。

```bash
    Linux:  source activate your_env_nam
    Windows: activate your_env_name
```

### 6. 在虚拟环境中安装额外的包

```bash
    conda install -n your_env_name [package]
```

### 7. 关闭虚拟环境(即从当前环境退出返回使用PATH环境中的默认python版本)

```bash
    deactivate env_name
```

或者`activate root`切回root环境，Linux下：source deactivate 

### 8. 删除虚拟环境

```bash
    conda remove -n your_env_name --all
```

### 9. 删除环境中的某个包

```bash
    conda remove --name $your_env_name  $package_name
```

## 镜像配置

## 查看 conda 的配置：

```shell
conda config --show
```

查看或者直接查看 channels：

```shell
conda config --show channels
```

### 添加镜像

比如添加中科大的源：

```shell
conda config --add channels https://mirrors.ustc.edu.cn/anaconda/pkgs/free/
conda config --set show_channel_urls yes
```

*conda config --set show_channel_urls yes的意思是从channel中安装包时显示channel的 url，这样在搜索或者安装的时候可知来源*

### 移除镜像
```shell
conda config --remove channels defaults
conda config --remove channels https://mirrors.ustc.edu.cn/anaconda/pkgs/free/
```

## Jupyter

如果 conda 环境不出现在 jupyter 选项中，可以按照如下方法处理：

```bash
    nb_conda_kernels
```

 should be installed in the environment from which you run Jupyter Notebook or JupyterLab. This might be your base conda environment, but it need not be. For instance, if the environment notebook_env contains the notebook package, then you would run

```bash
    conda install -n notebook_env nb_conda_kernels
```

Any other environments you wish to access in your notebooks must have an appropriate kernel package installed. For instance, to access a Python environment, it must have the ipykernel package; e.g.

```bash
    conda install -n python_env ipykernel
```

To utilize an R environment, it must have the r-irkernel package; e.g.

```bash
    conda install -n r_env r-irkernel
```

For other languages, their corresponding kernels must be installed.

参考

1. [https://stackoverflow.com/questions/39604271/conda-environments-not-showing-up-in-jupyter-notebook](https://stackoverflow.com/questions/39604271/conda-environments-not-showing-up-in-jupyter-notebook)
