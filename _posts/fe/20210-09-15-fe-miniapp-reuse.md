---
layout: post
title: "小程序复用"
date: 2020-09-15 08:00:00 +0800
categories: fe
tag: [fe]
---
由于小程序没有使用“组件类”的构造方式，无法使用继承，因此，小程序框架提供了“混入”（mixins）方式的复用机制，“混入”主要通过 Behavior 来实现。
根据官方的定义：

每个 behavior 可以包含一组属性、数据、生命周期函数和方法。组件引用它时，它的属性、数据和方法会被合并到组件中，生命周期函数也会在对应时机被调用。每个组件可以引用多个 behavior ，behavior 也可以引用其它 behavior 。

<!-- more -->

## Behavior 的构成

Behavior 能够包含的属性是预定义的，无法自行扩展，比如，无法在 Behavior 中指定 options 或者 externalClasses 属性。

Behavior 的有效属性根据用途可以分三类：

第一类；数据属性；

    properties
    data
    relations
    methods

第二类：函数属性

    observers
    created
    attached
    ready
    moved
    detached
    lifetimes
    pageLifetimes

第三类：扩展属性

    behaviors
    definitionFilter

不同的属性对应不同的混入规则。

*其中只有 behaviors 是一个数组，可以把 behaviors 这个类比 Js 中的原型链（Prototype Chain），definitionFilter 类比 js 中的构造函数。* 

## Behavior 的混入规则

由于 Behavior 支持嵌套，因此规则适用于两种类型：

1. 组件与 被引用 behaviors 之间的规则；
2. Behavior 与 被引用 behaviors 之间的规则。

这两类在其实没什么本质区别，因此，可以统一为 **引用者** 与 **被引用者** 之间的规则。

一个示例组件的配置如下：

```js
    ComponentA
        behaviors:[BehaviorA, BehaviorB, BehaviorC]

    BehaviorB
        behaviors:[BehaviorB1, BehaviorB2]
```

在上面的结构中，存在两组关系：

1. ComponentA 是引用者，[BehaviorA, BehaviorB, BehaviorC] 这个数组整体（序列）是被引用者；
2. BehaviorB 是引用者，[BehaviorB1, BehaviorB2] 这个数组整体（序列）是被引用者。

由于被引用者 behaviors 是个序列，对于不同的属性，对应的操作顺序还不一样。
对于数据属性，可以理解为执行一个查找操作；对于函数属性，可以理解为执行一个遍历操作。

### 查找数据属性

查找“引用者”数据属性的规则是：

1. 如果在 “引用者” 自身找到此属性，则结束查找，返回此属性值；
2. 如果在 “引用者” 没有找到此属性，则在“被引用者”查找此属性，返回查找结果。

查找“被引用者”数据属性的规则是：

1. 根据 behaviors 的数组顺序，**从右往左** 执行查找。
2. 此时每个 Behavior 都是一个“引用者”，执行“引用者”数据属性的查找规则。

对于上面的示例组件结构，数据属性的查找顺序是：

    ComponentA -> BehaviorC -> BehaviorB -> BehaviorB2 -> BehaviorB1 -> BehaviorA

### 遍历函数属性

遍历“引用者”函数属性的规则：

1. 遍历“被引用者”自身的函数属性；
2. 操作“引用者”的函数属性。

遍历“被引用者”函数属性的规则是：

1. 根据 behaviors 的数组顺序，**从左往右** 遍历；
2. 此时每个 Behavior 都是一个“引用者”，执行“引用者”函数属性的遍历规则。

对于上面的示例组件结构，函数属性的遍历顺序是：

    BehaviorA -> BehaviorB1 -> BehaviorB2 -> BehaviorB -> BehaviorC -> ComponentA

### 总结

查找数据的时候**先己后人，从右到左**；遍历数据的时候**先人后己，从左到右**，其实这两条规则遵循的原则是一致的：*越晚定义的数据，优先级越高*。

### 对象合并规则

数据属性的合并遵循基本的*对象合并规则*，对于单个属性：

1. 如果“合并对象”本身有这个属性，则忽略“被合并对象”的同名属性；
2. 如果“合并对象”本身无这个属性，则将“被合并对象”的属性（包括属性值）拷贝至“合并对象”；

假如对象 A 要合并对象 B，合并结果等同于：

```javascript
    objA = Object.assign({}，objB, objA);
```

### data 属性

data 是“数据属性”，因此执行“数据属性”的查找规则。具体的合并规则如下：

1. 若“引用者”本身有这个属性，且这个属性值是“对象类型”，则按照“对象合并规则”合并**对象的属性值**。
2. 对于其他属性，则按照“对象合并规则”合并**对象属性**。

代码描述即为：

如果属性 key 是个对象类型，则合并效果如下：

```javascript
    BehaviorB.data.key = Object.assign({}, BehaviorB1.data.key, BehaviorB2.data.key, BehaviorB.data.key);
```

如果属性 key 不是对象类型，则合并效果如下：

```javascript
    if (BehaviorB.data.hasOwnProperty(key)){
        //donothing
    }else if (BehaviorB2.data.hasOwnProperty(key)){
        BehaviorB.data.key = BehaviorB2.data.key;
    }else if (BehaviorB1.data.hasOwnProperty(key)){
        BehaviorB.data.key = BehaviorB1.data.key;
    }
```
补充说明 ：

1. 这里的“对象类型”不够清晰，毕竟在 js 中，Array 也是一个对象，准确一点的表述应该是“映射/散列类型”。
2. 属性拷贝不是“深拷贝”。
3. 合并操作要求所有同名字段的值都是“对象类型”，如果某个“被引用者”同名字段的值类型不是“对象类型”，就会导致合并失败。 

### properties、methods 属性

遵循“对象合并规则”。如果我们把 properties 和 methods 看作是 data 的两个特殊属性，就更容易理解：

```javascript
{
    data:{
        properties:{
        },
        methods:{
        },
        ...
    }
}
```

此时可以发现，properties 是 data 的一个“对象类型”属性，methods 也是 data 的一个“对象类型”属性，最终使用的都是 data 所描述的规则。

### 生命周期函数和 observers

*可以把生命周期函数看作是对生命周期事件进行监听的 observers，因此可以与 observers一起理解，这一段属于个人补充，不属于官方文档的内容*。

此类属性属于“函数属性”，因此执行“函数属性”的查找规则。函数属性不会相互覆盖，而是在对应触发时机被逐个调用。

*官方文档特别指出：如果同一个 behavior 被一个组件多次引用，它定义的生命周期函数和 observers 不会重复执行。*

### relations 和 definitionFilter

官方文档中没有提到 relations 和 definitionFilter。
其中 definitionFilter 像是构造函数，因此单独定义了，并且，definitionFilter 的机制有些麻烦，可以单独再讨论。
至于 relations，根据实际验证，发现规则与 properties 一致。

https://developers.weixin.qq.com/miniprogram/dev/framework/custom-component/behaviors.html
