---
layout: post
title: "小程序复用-Behavior"
date: 2020-09-15 08:00:00 +0800
categories: fe
tag: [fe]
---

虽然小程序提供了基于 Behavior 的复用机制，但 Behavior 对 Component 和 Page 的支持程度不一样，有必要详细区分一下。

<!-- more -->

## Behavior 的构成

再次回顾一下 Behavior 支持的属性：

    properties
    data
    relations
    methods

    observers
    created
    attached
    ready
    moved
    detached
    
    lifetimes
    pageLifetimes

    behaviors
    definitionFilter

其中

    created
    attached
    ready
    moved
    detached

已经标记为废弃，以后不应该再在实际开发中使用，因此，这个列表可以简化一下：

    properties
    data
    relations
    methods

    observers
    lifetimes
    pageLifetimes

    behaviors
    definitionFilter

## Page 与 Component 的差异

Page 可以认为是一个 特殊的 Component，但是与 Component 不同的是，Page 作为基础的视图容器，承担了与显示相关的控制。因此，Page 比 Component 多了几个与视图相关的生命周期方法：

| Page     | Component  |         
| ----     | ----       |       
| onLoad   | created, attached|
| onShow   | 无对应     |              
| onReady  | ready      |              
| 无对应    | moved     |              
| onHide   | 无对应     |                  
| onUnload | detached   |                  
| onResize | 无对应     |                  

以上对应生命周期方法在 lifetimes 字段里配置，不过这些方法都没有参数：

    lifetimes: {
        created: function() {},
        attached: function() {},
        ready: function() {},
        moved: function() {},
        detached: function() {}
    }

*注意：lifetimes 的方法会覆盖外层的同名方法，而不会依次执行*

为了填补 Component 的缺失，Component 新增了 pageLifetimes 字段，用来监听 onShow、onHide、onResize 对应的生命周期。pageLifetimes 的构成：

    pageLifetimes: {
        show: function() {},
        hide: function() {},
        resize: function(size) {}
    }


同理，由于 Page 是基础容器，因此，Page 不支持*模板数据绑定*，也就没有 properties 和 relations 字段。有一点需要注意，Page 也不支持 observers，至于原因则未知，**可能**小程序基础库的后续版本会逐步支持。

总结一下，Page 与 Component 的配置字段对比：

| Behavior 属性    | Page   | Component  |
| ----             | ----   | ----       |
| properties       | 不生效 | 生效 |
| data             | 生效   | 生效 |
| relations        | 不生效 | 生效 |
| methods          | 生效   | 生效 |
| observers        | 不生效 | 生效 |
| lifetimes        | 生效   | 生效 |
| pageLifetimes    | 不生效 | 生效 |
| behaviors        | 生效   | 生效 |
| definitionFilter | 生效   | 生效 |

因此，可以引出一个结论：虽然 Page 与 Component 都支持 behaviors 属性，但是由于存在以上差异，能够生效的 behavior 配置会略有不同，在使用过程中需要注意。


### 相关链接

[小程序复用](./2020-09-16-fe-miniapp-reuse.md)
[小程序复用-Behavior](./2020-09-16-fe-miniapp-reuse-2.md)
[小程序复用-函数构造器](./2020-09-16-fe-miniapp-reuse-3.md)