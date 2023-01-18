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

Behavior 能够包含的属性是预定义的，是 Component 配置项的一个子集，且无法自行扩展，比如，无法在 Behavior 中指定 options 或者 externalClasses 属性。
而且，Behavior 无法自定义名称，只能由框架自主生成。不能像官方组件那样定义 wx://form-field、wx://form-field-button 之类的语义化名称。

Behavior 的有效属性根据用途可以分三类：

第一类；数据属性；

    properties
    data
    relations
    methods

第二类：生命周期属性

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

由于 Behavior 支持嵌套，因此两种组合引用方式：

1. 组件直接引用 behaviors；
2. 被引用的 Behavior 自身也引用 behaviors。

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

由于被引用者 behaviors 是个序列，对于不同的属性，对应的操作顺序不一样，因此，定义了一个引用优先级。优先级的基本原则是：

1. “引用者”的优先级高于“被引用者“
2. “被引用者”中越靠后的引用，优先级越高。

我们根据这个原则，将上述示例组件按照优先级从低到高排个序：

 ```javascript
    BehaviorA < BehaviorB < BehaviorC < ComponentA

    BehaviorB1 < BehaviorB2 < BehaviorB
```   

具体说来，就是“引用者”的优先级最高，于是把“引用者”放在“被引用者”的最右边，**从左到右** 优先级依次升高。去掉嵌套之后，优先级从低到高排列顺序如下：

 ```javascript
    BehaviorA < BehaviorB1 < BehaviorB2 < BehaviorB < BehaviorC < ComponentA
```

### 对象合并

对象的合并遵循基本的*对象合并*规则：

1. 如果“合并对象”本身有这个属性，则忽略“被合并对象”的同名属性；
2. 如果“合并对象”本身无这个属性，则将“被合并对象”的属性（包括属性值）拷贝至“合并对象”；

假如对象 A 要合并对象 B，合并结果等同于：

```javascript
    objA = Object.assign({}，objB, objA);
```

补充说明 ：

1. 这里的“对象类型”不够清晰，毕竟在 js 中，Array 也是一个对象，准确一点的表述应该是“映射/散列类型”，文档中叫“ObjectMap”。
2. 属性拷贝不是“深拷贝”。

### 合并数据属性

根据属性的不同，会有不同的合并方式，合并原则：**优先级高的数据属性覆盖优先级低的数据属性**。（相当于继承体系里面子类屏蔽了父类属性）

#### data 属性

官方框架对 data 进行了一个特别的处理，并不是简单合并 Behavior 的 data，而是合并每一个 “data 的属性”。
比如：

```javascript
const behavior2 = Behavior({
    data:{
        items:{
            behavior2:'behavior2'
        },
        name:'behavior2'
    }
});
const behavior1 = Behavior({
    data:{
        items:{
            behavior1:'behavior1'
        },
        name:'behavior1'
    }，
    behaviors:[behavior2]
});
```

这两个合并之后，data 为：

```javascript
data = {
    items:{
        behavior1:'behavior1'，
        behavior2:'behavior2'
    },
    name:'behavior2'
}

```
即先检测 data 的每一个直接属性的值类型，根据值类型的不同，采取不同的合并方式。对于某个属性 key：

1. 如果“高优先级引用”与“低优先级引用”的值类型的**都是**“对象类型”，则根据“对象合并”规则合并这个属性值。
2. 其他情况下，直接用“高优先级引用”的值覆盖“低优先级引用”的值。

一个示例：

```javascript
[{key:{name1:'val1'}},{key:{name2:'val2'}}] // 合并结果是 {key:{name1:'val1', {name2:'val2'}}
[{key:{name1:'val1'}},{key:200}] // 合并结果是 {key:200}
[{key:200},{key:{name2:'val2'}}] // 合并结果是 {key:{name2:'val2'}}
```

代码描述如下：

```javascript
const items = [BehaviorA , BehaviorB1 , BehaviorB2 , BehaviorB , BehaviorC , ComponentA];
let finalValue = {};
for(const i = 0; i < items.length; i++){
    if (items[i].data.hasOwnProperty(key)){
        if(typeof(finalValue[key]) === 'object map' && typeof(items[i].data[key]) === 'ObjectMap'){ // 并不存在 typeof 这个方法，也不存在 'object map' 这个类型，仅用作说明。
            finalValue[key] = Object.assign({}, finalValue[key], items[i].data[key]);
        }else{
            finalValue[key] = items[i].data[key];
        }
    }
}
ComponentA.data = finalValue;

```

#### properties 与 methods 属性

遵循“合并数据属性”的方式。

合并 properties 代码描述如下：

```javascript
const items = [BehaviorA , BehaviorB1 , BehaviorB2 , BehaviorB , BehaviorC , ComponentA];
let finalAttr = {};
for(const i = 0; i < items.length; i++){
    if (items[i].data.hasOwnProperty(key)){
        finalAttr = Object.assign(finalAttr, items[i].properties);
    }
}
ComponentA.properties = finalAttr;
```

同理，合并 methods 代码描述如下：

```javascript
const items = [BehaviorA , BehaviorB1 , BehaviorB2 , BehaviorB , BehaviorC , ComponentA];
let finalAttr = {};
for(const i = 0; i < items.length; i++){
    if (items[i].data.hasOwnProperty(key)){
        finalAttr = Object.assign(finalAttr, items[i].methods);
    }
}
ComponentA.methods = finalAttr;
```

如果我们把 properties 和 methods 看作是 data 的两个特殊属性，就更容易理解：

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

与数据属性不同，生命周期方法不会相互覆盖，而是在对应触发时机被逐个调用（相当于继承体系里面先调用父类方法）。官方文档特别指出：如果同一个 behavior 被一个组件多次引用，它定义的生命周期函数和 observers 不会重复执行。

调用原则：**先调用优先级低的生命周期方法，后调用优先级高的生命周期方法**。

代码描述如下：

```javascript
const items = [BehaviorA , BehaviorB1 , BehaviorB2 , BehaviorB , BehaviorC , ComponentA];
for(const i = 0; i < items.length; i++){
    const item = items[i];
    if(!item.lifecycle.invoked){
        item.lifecycle();
    }
}
```

*可以把生命周期函数看作是对生命周期事件进行监听的 observers，因此可以与 observers 一起理解，这一段属于个人补充，不属于官方文档的内容*。

### relations 和 definitionFilter

官方文档中没有提到 relations 和 definitionFilter。
其中 definitionFilter 像是构造函数，因此单独定义了，并且，definitionFilter 的机制有些麻烦，可以单独再讨论。
至于 relations，根据验证，规则与 properties 一致。


### 另一视角

对于数据属性，可以理解为执行一个查找操作；对于生命周期方法，可以理解为执行一个遍历操作。

#### 查找数据属性

查找“引用者”数据属性的规则是：

1. 如果在 “引用者” 自身找到此属性，则结束查找，返回此属性值；
2. 如果在 “引用者” 没有找到此属性，则在“被引用者”查找此属性，返回查找结果。

查找“被引用者”数据属性的规则是：

1. 根据 behaviors 的数组顺序，**从右往左** 执行查找。
2. 此时每个 Behavior 都是一个“引用者”，执行“引用者”数据属性的查找规则。

对于上面的示例组件结构，数据属性的查找顺序是：

    ComponentA -> BehaviorC -> BehaviorB -> BehaviorB2 -> BehaviorB1 -> BehaviorA

#### 遍历生命周期方法

遍历“引用者”生命周期方法的规则：

1. 遍历“被引用者”自身的生命周期方法；
2. 执行“引用者”的生命周期方法。

遍历“被引用者”生命周期方法的规则是：

1. 根据 behaviors 的数组顺序，**从左往右** 遍历；
2. 此时每个 Behavior 都是一个“引用者”，执行“引用者”生命周期方法的遍历规则。

对于上面的示例组件结构，生命周期方法的遍历顺序是：

    BehaviorA -> BehaviorB1 -> BehaviorB2 -> BehaviorB -> BehaviorC -> ComponentA

#### 总结

查找的时候**先己后人，从右到左**；遍历的时候**先人后己，从左到右**，其实这两条规则遵循的原则是一致的：*越晚定义的数据，优先级越高*。


### 相关链接

[小程序复用](./2020-09-16-fe-miniapp-reuse.md)
[小程序复用-Behavior](./2020-09-16-fe-miniapp-reuse-2.md)
[小程序复用-函数构造器](./2020-09-16-fe-miniapp-reuse-3.md)