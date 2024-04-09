---
layout: post
title: "npm 记录"
date: 2018-09-13 08:00:00 +0800
categories: computer
tag: [computer]
---

`npm link` 特性支持开发者将本地还未发布的 npm 包链接到项目中进行调试。

<!-- more -->

## npm link

大致的步骤是：

1. 在本地 npm 包目录执行 `npm link` 将本地的 npm 包链接（挂载）到全局 npm 模块目录中；
2. 在项目目录中执行 `npm link <package-name>` 命令，将全局 npm 模块目录中的 <package-name> 包链接到项目中；
3. 当完成调试后，在项目目录中执行 `npm unlink <package-name>` 命令取消与本地 npm 包的链接；

### 查看 npm 包

`npm ls -g --depth=0` 将列出全局 npm 模块目录中的所有包，包括已经通过 npm link 连接的包。--depth=0 选项用于只显示顶级包，而不显示其依赖关系。

在项目目录中执行 `npm ls --depth=0` 命令将仅列出项目中安装的所有包。

### 从全局解除链接（取消挂载）

```shell
npm remove -g <packge-name>

# 或者更暴力的：

cd $(npm root -g)
rm -rf <package-name>
```

## .npmrc 文件

.npmrc，可以理解成 `npm runtime configuration` , 即 npm 运行时配置文件。在电脑上，通常存在不止一个 `.npmrc` 文件，而是有多个 `.npmrc` 文件。在我们安装包的时候，npm 按照如下顺序读取这些配置文件：

1. 项目配置文件：你可以在项目的根目录下创建一个.npmrc 文件，只用于管理这个项目的 npm 安装。
2. 用户配置文件：系统当前用户目录下的 .npmrc 文件，可以通过 `npm config get userconfig` 来获取该文件的位置；
3. 全局配置文件：多个用户公共的 .npmrc 文件。该文件的路径为：`<prefix>/etc/npmrc`，使用 `npm config get prefix` 获取 `<prefix>`，如果你不曾配置过全局文件，该文件不存在；
4. npm 内嵌配置文件：最后还有 npm 内置配置文件；

.npmrc 文件以 `key=value` 的格式进行配置。比如把 npm 的源配置为淘宝源：

```shell
registry=https://registry.npm.taobao.org
```

如果想删除一些配置，直接在 `.npmrc` 文件中把对应的代码行给删除即可。
