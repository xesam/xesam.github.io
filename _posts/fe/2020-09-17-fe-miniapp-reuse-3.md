---
layout: post
title: "小程序复用-函数构造器"
date: 2020-09-17 08:00:00 +0800
categories: fe
tag: [fe]
---

小程序App、Page 和 Component 是通过函数调用的方式来实现创建的，通过函数参数 option 来定义数据和行为，通过 Behavior 来实现复用。
但是在抽象组件的时候，会面临几个问题：

1. 小程序没有继承体系。
2. 部分 option 的属性无法通过 Behavior 来组合/混入。

<!-- more -->

**没有继承体系**导致的问题是自定义组件难以扩展。

比如我们使用了一个第三方的组件，如果对方没有提供完全满足需求的 properties，那使用者就只能把源码复制过来，然后修改源码。
但是更理想的方式是我们能直接继承第三方组件，然后扩展它的自定义 properties、覆盖默认行为以及增加新的方法。

而且，大部分时候，我们已经定义了一部分组件，自然希望在不修改已有组件的情况下，能够支持继承。

**无法通过 Behavior 来组合/混入**的一个典型例子就是 externalClasses ，这个属性只对当前组件有效，无法继承。一个示例（以下代码不可运行，仅做说明）：

```javascript
Parent = Component({externalClasses:['common-class']});

Child extends Parent；
```
我们期望的是 Child 能够支持 externalClasses:['common-class']，但实际上并没有这种内置支持。
当然，小程序团队有自己的考虑，不过我们完全可以自己来实现这一套逻辑。

实现的原则：

1. 不改变小程序的调用方式。
2. 不改变小程序的字段定义与原有逻辑。

#### 不改变小程序的调用方式

这条原则的意思是，原本小程序是这样的调用方式：

```javascript
Component({
    properties:{},
    data:{}
})
```

增强之后也沿用类似的调用：

```javascript
const {_Component as Component} = require('xxxx');
Component({
    properties:{},
    data:{}
})
```

但是有部分框架却采取自定义一套写法的方案，比如同样实现上述调用，需要这么写：

```javascript
const {NiubiComponent} = require('xxxx');
class NiubiComponent({
    constructor(){
        this.properties = {};
        this.data = {};
    }
})
```
这么些确实更适合表达意图，要是这个框架一直维护还好，如果一旦烂尾了，以后想升级或者想移除框架，要修改的内容可就不止一丁半点了，所以，我个人非常不建议在一个长期项目中使用这类框架，完美印证“开发一时爽，维护火葬场”。

#### 不改变小程序的字段定义与原有逻辑

这个原则的意思就是不在框架中引入会被使用者引用的“元数据”，比如有的框架会引入 state 字段来管理状态。其次，也不改变小程序原有的复用逻辑（比如 behaviours 的优先级顺序），否则会误导使用者，也会导致应用与框架的强耦合，由于小程序框架迭代较快，这种耦合越紧，就越拉跨。

### 一个实现案例

基于这个原则，提供了一个实现案例：[view-support](https://github.com/miniapp-develop/view-support)

使用示例

```javascript
const {presets} = require("@mini-dev/view-support");

//定义父组件
const ParentComponent = presets.Component({
    externalClasses: ['parent-class'],
    options: {
        styleIsolation: 'isolated',
        multipleSlots: true,
        pureDataPattern: /^_mini/
    }
});

//定义子组件
const ChildComponent = presets.Component({
    externalClasses: ['child-class'],
}, ParentComponent); // 会继承 ParentComponent 的配置、属性和行为

```

页面中调用，最终应用的 externalClasses 为 ['parent-class', 'child-class', 'option-class']

```javascript
const ChildComponent = require("ChildComponent");

ChildComponent({
    externalClasses: ['option-class'], 
})

```

如果已经有成熟的标准组件（按照小程序官方框架定义的），也可以直接复用：

```javascript
const ChildComponent = require("ChildComponent");

ChildComponent({
    externalClasses: ['option-class'], 
}, ExistComponent)

```

### 相关链接

[小程序复用](./2020-09-16-fe-miniapp-reuse.md)
[小程序复用-Behavior](./2020-09-16-fe-miniapp-reuse-2.md)
[小程序复用-函数构造器](./2020-09-16-fe-miniapp-reuse-3.md)