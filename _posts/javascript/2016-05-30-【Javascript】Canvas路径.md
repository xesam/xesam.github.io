---
layout: post
title:  "【Javascript】Canvas路径"
date:   2016-05-30 12:46:04 +0800
categories: javascript
tag: [javascript]
---
## 理解路径
Javascript 中的 Canvas 是基于路径的，同一时刻时能有一条路径而且肯定会有一条路径。
路径中可以包含很多条子路径，即 N 条子路径构成了一条路径。与路径相关的操作：

    Context#beginPath() 用于创建一条新的路径，这也就意味着先前的路径丢失了，因为只能有一条路径。
    moveTo/lineTo/... 之类的命令用于创建子路径。

说到 beginPath，就不得不提到 closePath，两者是不是有很“紧”的联系呢？答案是几乎没有关系。
closePath 的意思不是结束路径，而是闭合路径，它会试图从当前路径的终点连一条子路径到起点，让当前整个路径闭合起来。
但是，这并不意味着它之后的路径就是新路径了！

绘图指令有两种：

1. 保留绘图指令（retained draw command），即不产生直接效果的指令，比如 moveTo, lineTo, (Curve)To, arc, rect。
2. 直接绘图指令（direct draw command），这些指令既不需要创建新路径，也不对当前路径产生影响，比如 fill/strokeRect, fill/strokeText, drawImage, get/putImageData.

所以，关于路径的规则就是：

1. 如果你使用 retained draw command，则需要 beginPath
2. 如果你使用 direct draw command，则无需 beginPath

## save() & restore()

save() & restore() 不会影响路径，影响的是什么？影响各种设置：

1. 渲染设置 : strokeStyle / fillStyle / globalCompositeOperation / globalAlpha / lineWidth / font / textAlign/ shadow / ...
2. 变换（transform）设置 translate/scale/rotate/...
3. 区域（clip）设置


[Immediate Mode](https://en.wikipedia.org/wiki/Immediate_mode_(computer_graphics))
[Retained Mode](https://en.wikipedia.org/wiki/Retained_mode)

