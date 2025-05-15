---
layout: post
title: "Python环境管理-uv"
date: 2016-03-04 12:01:00 +0800
categories: computer
tag: [computer]
---

`UV` 号称是 超快、超强大的 `Python` 依赖管理工具，用 `Rust` 语言开发的，这使得它比传统工具快得多，能让你的 `Python` 开发体验更加流畅。

<!-- more -->

它可以用来：

- 管理 `Python` 版本（类似 `PyEnv`）
- 创建和管理虚拟环境（类似 `VirtualEnv` 和 `PyEnv`）
- 管理 `Python` 依赖（类似 `Pip` 和 `Poetry`）

## 安装

1. 使用 Pip 安装：

```shell
pip install uv
```

2. 使用 Homebrew 安装：

```shell
brew install uv
```

3. 使用 curl ：

```shell
curl -fsSL https://astro.sh/uv/install.sh | sh
```

4. 使用 Cargo ：

```shell
cargo install uv --git https://github.com/astral-sh/uv
```

验证 UV 是否安装成功：

```shell
uv --version
```

## 使用

### 常用命令

- `uv init` —— 初始化一个新的 `Python` 项目
- `uv add` —— 添加依赖（类似 `pip install`）
- `uv remove` —— 移除依赖
- `uv sync` —— 同步依赖（类似 `poetry install`）
- `uv run` —— 运行 `Python` 文件或命令

### 创建项目

```shell
uv init project0
```

该命令会在当前目录下创建一个名为 `project0` 的目录，并初始化一个 `Python` 项目。目录结构如下：

```text
project0/
├── .git/
├── .gitignore
├── .python-version        # Python 版本控制文件
├── pyproject.toml         # 项目的配置文件
├── README.md
├── main.py
└── .venv/                 # 虚拟环境目录
```

### 管理依赖

#### 安装依赖

```shell
uv add fastapi sqlalchemy
```

UV 会同时安装 `FastAPI` 和 `SQLAlchemy，并自动更新` `pyproject.toml`.

#### 移除依赖

```shell
uv remove sqlalchemy
```

卸载 `SQLAlchemy` ，还会自动从 `pyproject.toml` 中移除对应的依赖项。

#### 同步依赖

有时候，我们的虚拟环境可能和 pyproject.toml 里的依赖不同步。这时，只需运行：

```shell
uv sync
```

UV 会自动检查并修复依赖，类似于 `poetry install`.

#### 查看依赖树

```shell
uv tree
```

#### 运行 Python 代码

```shell
uv run main.py
```

这个命令会：

- 自动创建虚拟环境（如果尚未创建）
- 安装缺失的依赖
- 运行脚本

### 管理 `Python` 版本

`UV` 内置了 `Python` 版本管理，并且更加智能。

当你运行 `uv init project` 时，`UV` 会：

- 自动检测系统上的 Python 版本
- 优先选择当前 Python 版本
- 如果没有合适的版本，会自动下载

查看 UV 识别到的 Python 版本：

```shell
uv python list
```

如果你想安装某个 Python 版本（比如 3.12.1），可以直接执行：

```shell
uv python install 3.12.1
```

如果我们希望某个项目始终使用特定的 `Python` 版本（比如 3.12），可以执行：

```shell
uv venv --python 3.12
```

`UV` 会自动创建 基于 `Python 3.12` 的虚拟环境，并将信息写入 `.python-version` 文件。
