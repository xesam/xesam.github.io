---
layout: post
title: "Function Calling & MCP & A2A"
date: 2025-04-27 00:00:00 +0800
categories: computer
tag: [computer]
---

Function Calling 与 MCP 以及 A2A 之间有什么联系和区别？

<!-- more -->

- Function Calling；
- MCP：Modal Conntext Protocol；
- A2A：Agent-to-Agent；

三者之间没有明显的边界，只是抽象程度存在差异，每一个概念都是通过增加一层抽象，隐藏下层差异和细节，使得上层结构可以更方便的使用大模型。
参考类比：

| 概念             | 类比          |
| ---------------- | ------------- |
| Function Calling | API           |
| MCP              | SDK           |
| A2A              | Proxy/Service |

只要整个概念的实现还是依赖于大模型的文本输出，那么所做的事就是在`文本雕花`，始终绕不过`解析大模型的输出，根据解析结果，然后进行一些特定操作`的流程。
即是说：

- 某个大模型不支持 `Function Calling`，开发者也可以自定义文本协议，手动实现`Function Calling`。
- 如果某个大模型不支持 `MCP`，开发者也可以自定义文本协议，手动实现`MCP`，而且在实现过程中，大概率会复用`Function Calling`。
- 如果某个大模型不支持 `A2A`，开发者也可以自定义文本协议，手动实现`A2A`，而且在实现过程中，大概率会复用`Function Calling` 和 `MCP`。

后续肯定还会有更多的协议出现，但是并没有全新的概念出现，协议的设计和实现方案对从业者对启发和参考作用，比协议所宣传的能力更有价值。
