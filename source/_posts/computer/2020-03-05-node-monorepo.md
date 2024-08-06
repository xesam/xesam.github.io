---
layout: post
title: "monorepo的工具使用"
date: 2021-03-04 09:00:00 +0800
categories: computer
tag: [computer]
---

用工具支持 monorepo 模式。

<!-- more -->

## pnpm

pnpm 支持 monorepo 模式的工作机制叫做 workspace(工作空间)。

它要求在代码仓的根目录下存有 pnpm-workspace.yaml 文件指定哪些目录作为独立的工作空间，这个工作空间可以理解为一个子模块或者 npm 包。
pnpm 通过工作空间下 package.json 文件的 name 字段来识别仓库内的包。

```yaml
packages:
  - a
  - b
  - packages/*
```

大部分用法与 npm 一致，至于内部的存储细节则通常无需深究。

```shell
pnpm init -y
pnpm install
...
```

不过由于存在 workspace 模式，因此部分命令需要稍作调整。

### -w 选项

-w(--workspace-root) 选项代表在 monorepo 模式下的根目录进行操作。

```shell
# 安装  -D(-devDependencies) -w(--workspace-root)
pnpm install -wD xxx
# 卸载
pnpm uninstall -w xxx
...
```

### 过滤子模块

在 workspace 模式下，pnpm 主要通过 --filter 选项过滤子模块，实现对各个工作空间的操作。

```shell
# 为 a 包安装 lodash
pnpm --filter a i -S lodash // 生产依赖
pnpm --filter a i -D lodash // 开发依赖
```

### Workspace 协议

pnpm workspace 对内部依赖关系约定了一套 Workspace 协议 (workspace:)。下面给出一个内部模块 a 依赖同是内部模块 b 的例子。

```json
{
  "name": "a",
  // ...
  "dependencies": {
    "b": "workspace:^"
  }
}
```

在实际发布 npm 包时，workspace:^ 会被替换成内部模块 b 的对应版本号(对应 package.json 中的 version 字段)。替换规律如下所示：

```json
{
  "dependencies": {
    "a": "workspace:*", // 固定版本依赖，被转换成 x.x.x
    "b": "workspace:~", // minor 版本依赖，将被转换成 ~x.x.x
    "c": "workspace:^" // major 版本依赖，将被转换成 ^x.x.x
  }
}
```

#### 指定模块间的依赖

如果需要指定模块间的依赖，直接在对应的 package.json 中使用 workspace:^ 语法来添加就好了，也别用命令方式了，不太稳定。
