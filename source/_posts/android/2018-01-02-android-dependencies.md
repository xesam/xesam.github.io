---
layout: post
title:  "android dependencies 简记"
date:   2018-01-01 08:00:00 +0800
categories: android
tag: [android]
---

Android 添加 build 依赖项。

<!-- more -->

工程结构：

```plain

project
    ----libA
    ----app
```

| 配置           | 行为                                                                                    |
| -------------- | --------------------------------------------------------------------------------------- |
| implementation | 将依赖项添加到编译类路径，并将依赖项打包到 build 输出，但是不会将该依赖项导出到其他模块 |
| api            | 将依赖项添加到编译类路径，并将依赖项打包到 build 输出，同时将该依赖项导出到其他模块     |
| compileOnly    | 将依赖项添加到编译类路径，但是不会将其添加到 build 输出                                 |
| runtimeOnly    | 只会将依赖项添加到 build 输出，但不会将其添加到编译类路径                               |
| apk            | 已废弃，相当于 runtimeOnly                                                              |
| compile        | 已废弃，相当于 api                                                                      |
| provided       | 已废弃，相当于 compileOnly                                                              |

如何理解？

将依赖项添加到编译类路径：编译的时候可以找到；

并将依赖项打包到 build 输出：运行的时候可以找到（比如使用 反射 的方式）；

示例：

| libA 配置             | 编译时表现                                                                                                |
| --------------------- | --------------------------------------------------------------------------------------------------------- |
| implementation 'jarA' | libA 编译或者运行时都可以找到 jarA；app 编译的时候找不到 jarA，自然也不存在运行了                         |
| api 'jarA'            | libA 编译或者运行时都可以找到 jarA；app 编译或者运行时也都可以找到 jarA                                   |
| compileOnly 'jarA'    | libA 编译的时候可以找到 jarA，运行时找不到；app 编译的时候找不到 jarA，因此，app 需要单独配置 jarA 的依赖 |
| runtimeOnly 'jarA'    | libA 编译的时候找不到 jarA，运行时可以找到；app 编译的时候也找不到 jarA，运行时可以找到                   |

使用 implementation 的好处：加快重新编译的速度，实现方式就是“不传导”。
对于含有多个 library 的工程，比如我们更新了 libA 的 implementation，由于 implementation 的依赖不会导出，因此只需要单独编译 libA 模块就行。
如果使用的是 api 配置，由于 app 也有可能使用了 'jarA'，所以 app 也需要重新编译。


