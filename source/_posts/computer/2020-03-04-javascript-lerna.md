---
layout: post
title: "monorepo之lerna"
date: 2020-03-04 09:00:00 +0800
categories: computer
tag: [computer]
---

`Lerna` 是一个多包（参考 monorepo）管理工具。

> Lerna is a fast modern build system for managing and publishing multiple JavaScript/TypeScript packages from the same repository.

<!-- more -->

### 初始化项目

转到目标文件夹：

```shell
lerna init
```

默认工程结构：

    ├── lerna.json
    ├── package.json
    └── packages

lerna.json 里的版本号默认是 0.0.0，可以改成其他的。

### 创建模块

```shell
lerna create {pkg_name} [pkg_path]
```

比如：

```shell
lerna create @xesam/api
lerna create @xesam/spi-1
lerna create @xesam/spi-2
lerna create @xesam/spi-3
```

### 为模块增加依赖

```shell
lerna create {dependency_name}
```

比如：

```shell
lerna add axios # 给所有模块增加 axios 依赖
lerna add axios --scope=@xesam/api # 给 @xesam/api 模块增加 axios 依赖
```

### 安装依赖

```
lerna bootstrap
```

如果无效，就直接手动执行：

```
lerna exec npm install
lerna link
```

### 其他参考文章

[https://juejin.cn/post/6844903856153821198](https://juejin.cn/post/6844903856153821198)
[https://blog.51cto.com/u_14115828/3733816](https://blog.51cto.com/u_14115828/3733816)
[https://lerna.js.org/](https://lerna.js.org/)
