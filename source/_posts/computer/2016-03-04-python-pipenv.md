---
layout: post
title: "Python环境管理-pipenv"
date: 2016-03-04 12:00:00 +0800
categories: computer
tag: [computer]
---

Pipenv 官网：[https://pipenv.pypa.io/en/latest/](https://pipenv.pypa.io/en/latest/)

## 基本使用

1. 安装 pipenv：`pip install pipenv`
2. 创建/激活虚拟环境：`pipenv shell`
3. 安装依赖：`pipenv install requests`
4. 卸载依赖：`pipenv uninstall requests`
5. 退出虚拟环境：`exit`

<!-- more -->

## 示例

初始目录结构：

    --myapp
    |-- main.py

- 进入 `myapp` 目录，运行 `pipenv shell`，进入虚拟环境。
- 运行 `pipenv install requests`，安装依赖。
- 运行 `python main.py`，运行项目。
- 运行 `exit`，退出虚拟环境。

最终目录结构：

    --myapp
    |-- main.py
    |-- Pipfile # 依赖管理文件
    |-- Pipfile.lock # 依赖锁定文件

使用 `pipenv graph` 可以查看包之间的依赖关系。

## 相关问题

### 将虚拟环境建立在项目文件夹中

`pipenv` 默认将虚拟环境建立在 `<user_home>/.virtualenvs/` 目录下，但是也可以将虚拟环境建立在项目文件夹中。两类方式：

- 方式一：设置环境变量：`PIPENV_VENV_IN_PROJECT=1`

  - 在命令行设置：`set PIPENV_VENV_IN_PROJECT=1`
  - 在 `.bashrc` 文件中设置：`export PIPENV_VENV_IN_PROJECT=1`
  - 在项目根目录创建一个 `.env` 文件，配置 `PIPENV_VENV_IN_PROJECT=1`，`pipenv` 会在运行命令时自动加载项目根目录下的 `.env` 文件，无需额外配置。

- 方式二：在项目根目录创建一个 `.venv` 文件夹，运行`pipenv shell`或者`pipenv install`，`pipenv`会检测并使用该目录;

可以使用 `pipenv --venv` 查看当前的虚拟环境。

### 依赖的 python 版本与本机的 python 版本不一致

如果出现这种状况，可能会导致问题：

```
Warning: Python 3.12.0 was not found on your system...
Neither 'pyenv' nor 'asdf' could be found to install Python.
You can specify specific versions of Python with:
```

此时有可以通过 `pipenv --python <python_version>` 指定 python 版本，例如：`pipenv --python 3.9.6`。也可以修改 `Pipfile` 中的 `python_version` 字段，例如： `python_version = "3.9.6"`。还有一种方法就是在本机安装 python 的 `3.12.0` 版本。

都挺麻烦，还是 `conda` 最便捷，建议使用 `conda` 创建对应的 `python` 版本虚拟环境，然后使用 `pipenv` 进行独立的依赖管理。

### 在开发环境中安装

添加 `--dev`(或者`-d`)，在开发环境中安装:

```bash
pipenv install --dev requests
pipenv install -d requests
```

### 与 `requirements.txt` 的兼容性

通过 `requirements.txt` 安装依赖：

```bash
pipenv install -r `requirements.txt`
```

导出依赖到 `requirements.txt` 文件：

```bash
pipenv requirements > requirements-pro.txt # 生产环境的依赖导出
pipenv requirements --dev > `requirements.txt` # 生产环境+开发环境的依赖导出
pipenv requirements --dev-only > requirements-dev.txt # 开发环境的依赖导出
```

## 配合 Docker 部署

在使用 `pipenv` 管理 Python 项目并通过 Docker 部署到生产环境时，需结合 `Pipfile` 和 `Pipfile.lock` 的特性确保依赖的一致性，并通过 Docker 的隔离性优化部署流程。以下是详细配置步骤和最佳实践：

---

### **1. 基础 Dockerfile 配置**

#### **步骤说明**

1. **选择基础镜像**  
   使用官方 Python 镜像作为基础，例如 `python:3.9-slim`：

   ```dockerfile
   FROM python:3.9-slim
   ```

2. **安装 pipenv**  
   在 Docker 中全局安装 `pipenv`，确保依赖管理工具可用：

   ```dockerfile
   RUN pip install --no-cache-dir pipenv
   ```

3. **复制依赖文件**  
   将 `Pipfile` 和 `Pipfile.lock` 复制到镜像中，优先利用 Docker 的缓存机制加速构建：

   ```dockerfile
   COPY Pipfile Pipfile.lock /app/
   WORKDIR /app
   ```

4. **安装生产依赖**  
   使用 `pipenv install --deploy --system` 安装依赖到系统路径（跳过虚拟环境，直接安装到容器全局环境）：

   ```dockerfile
   RUN pipenv install --deploy --system
   ```

   - `--deploy`：强制检查 `Pipfile.lock` 是否与 `Pipfile` 同步，确保依赖版本锁定。
   - `--system`：直接安装到系统 Python 环境，避免容器内创建虚拟环境。

5. **复制应用代码**  
   将项目代码复制到镜像中：

   ```dockerfile
   COPY . /app
   ```

6. **设置启动命令**  
   定义容器启动时执行的命令：
   ```dockerfile
   CMD ["gunicorn", "app:app", "--bind", "0.0.0.0:8000"]
   ```

---

### **2. 优化依赖安装**

#### **缓存与多阶段构建**

- **利用缓存**  
  将依赖安装步骤放在代码复制之前，确保在代码变动时不会重复安装依赖：

  ```dockerfile
  COPY Pipfile Pipfile.lock /app/
  WORKDIR /app
  RUN pipenv install --deploy --system
  COPY . /app
  ```

- **多阶段构建（可选）**  
  减少最终镜像体积，例如先构建依赖层，再复制到运行镜像：

  ```dockerfile
  # 第一阶段：构建依赖
  FROM python:3.9-slim as builder
  RUN pip install pipenv
  COPY Pipfile Pipfile.lock /app/
  WORKDIR /app
  RUN pipenv install --deploy --system

  # 第二阶段：运行镜像
  FROM python:3.9-slim
  COPY --from=builder /usr/local/lib/python3.9/site-packages /usr/local/lib/python3.9/site-packages
  COPY . /app
  WORKDIR /app
  CMD ["gunicorn", "app:app", "--bind", "0.0.0.0:8000"]
  ```

---

### **3. 生产环境注意事项**

#### **依赖安全性与一致性**

- **强制锁定依赖版本**  
  确保 `Pipfile.lock` 提交到版本控制，并在构建时使用 `--deploy` 参数，避免依赖版本漂移。
- **禁用开发依赖**  
  生产环境中默认不安装 `[dev-packages]` 中的依赖，若需安装需显式指定 `--dev` 参数。

#### **镜像优化**

- **精简依赖**  
  使用 `slim` 或 `alpine` 版本的基础镜像减少体积。
- **清理缓存**  
  在安装依赖后清理不必要的缓存文件：
  ```dockerfile
  RUN apt-get clean && rm -rf /var/lib/apt/lists/*
  ```

---

### **4. 示例 Dockerfile**

```dockerfile
# 使用官方 Python 基础镜像
FROM python:3.9-slim

# 安装系统依赖（按需添加）
RUN apt-get update && apt-get install -y --no-install-recommends gcc

# 安装 pipenv
RUN pip install --no-cache-dir pipenv

# 设置工作目录并复制依赖文件
WORKDIR /app
COPY Pipfile Pipfile.lock ./

# 安装生产依赖到系统路径
RUN pipenv install --deploy --system

# 复制应用代码
COPY . .

# 暴露端口并启动应用
EXPOSE 8000
CMD ["gunicorn", "app:app", "--bind", "0.0.0.0:8000"]
```

---

### **5. 部署验证与调试**

- **检查依赖树**  
  进入容器执行 `pipenv graph` 确认依赖版本与预期一致。
- **日志与监控**  
  配置日志挂载和监控工具（如 Prometheus），确保容器运行状态可观测。

---

### **总结**

通过结合 `pipenv` 的依赖锁定和 Docker 的容器化隔离，可以实现高效、安全的生产环境部署。关键点包括：

1. 使用 `--deploy` 和 `--system` 参数确保依赖一致性。
2. 优化 Dockerfile 结构以利用缓存机制。
3. 管理敏感信息（如 `.env` 文件）时注意安全性。
